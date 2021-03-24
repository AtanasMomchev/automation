import subprocess
import argparse
import configparser
import os
import shutil


class Args:
    branch = None
    production = None
    branch_number = None

    def __init__(self):
        args = self.set_arguments()
        self.branch = args["branch"]
        self.production = args["production"]
        self.branch_number = args["branch_number"]

    @staticmethod
    def set_arguments():
        """
        Add arguments the script accepts from command line.
        :return: dict Of the arguments parsed from command line
        """
        parser = argparse.ArgumentParser()
        # Boolean to indecate building from branch
        parser.add_argument("--branch", default=False)
        # Boolean indicating the build is for production
        parser.add_argument("--production", default=False)
        # String containing the branch number from which to build
        parser.add_argument("--branch-number", default=None)
        args = parser.parse_args()
        return vars(args)


class VersionManager:

    @staticmethod
    def get_current_version(key):
        """
        Method to get the current version from version file
        :param str key: The key value by which to look in version.txt [default]
        :return: str the value contained in version.txt
        """
        version_file = "/home/nasko/automation/version.txt"
        config = configparser.ConfigParser()
        try:
            config.read(version_file)
        except FileNotFoundError:
            raise FileNotFoundError

        return config['default'][key]

    @staticmethod
    def set_version(key, version):
        """
        Set a new version in the version file.
        :param str key: The key value by which to look in version.txt [default]
        :param version: the new version to be set
        :return: None
        """
        version_file = "/home/nasko/automation/version.txt"
        config = configparser.ConfigParser()
        try:
            config.read(version_file)
        except FileNotFoundError:
            raise FileNotFoundError

        config.set('default', key, str(version))
        with open(version_file, 'w') as configfile:
            config.write(configfile)

    @staticmethod
    def ova_production():
        """
        Method to increase ova version in version.txt.
        This method increases the second int in the version and sets the last int to 0.
        Ex 6.0.10 -> 6.1.0
        :return: str New version string
        """
        key = 'OVA'
        version = VersionManager.get_current_version(key)
        num1 = version.split(".")[0]
        num2 = int(version.split(".")[1]) + 1
        num3 = 0
        vm_version = f"{num1}.{num2}.{num3}"

        VersionManager.set_version(key, vm_version)
        return vm_version

    @staticmethod
    def ova_dev():
        """
        Method to increase ova version in version.txt.
        This method increases the last int in the version.
        Ex 6.0.0 -> 6.0.1
        :return: str New version string
        """
        key = 'OVA'
        version = VersionManager.get_current_version(key)
        num1 = version.split(".")[0]
        num2 = version.split(".")[1]
        num3 = int(version.split(".")[2]) + 1
        vm_version = f"{num1}.{num2}.{num3}"

        VersionManager.set_version(key, vm_version)
        return vm_version


class Builder:

    def __init__(self, args):
        self.args = args

    def build_ova(self):
        """
        Method to build OVA image.
        1.When executed the method updated version in version.txt.
        2.Generates build command depending on parsed args. Run command. If build command fails revert version.
        3.Move the new ova image to //fileserver/Resource/VM.
        4.Delete SVN downloaded files
        :return: None
        """
        args = self.args
        # Conf file for packer
        build_file = "/home/nasko/automation/packer/ffs_ova"
        key = 'OVA'
        # This is used to revert version in case of fail
        initial_version = VersionManager.get_current_version(key)
        # Get new version
        if args.production:
            version = VersionManager.ova_production()
        else:
            version = VersionManager.ova_dev()

        # Create packer build command
        if not args.branch:
            cmd = ["packer", "build", "--force",
                   "-var", f"vm_version={version}", "-var", f"branch={args.branch}", build_file]
        else:
            if not args.branch_number:
                raise TypeError("Please provide a branch number with --branch-number option")

            cmd = ["packer", "build", "--force", "-var", f"vm_version={version}", "-var", f"branch={args.branch}",
                   "-var", f"branch_number={args.branch_number}", build_file]

        res = subprocess.run(cmd)
        # If packer failed revert version number and throw exception
        if res.returncode != 0:
            print(f"Reverting to previous version {initial_version}")
            VersionManager.set_version(key, initial_version)
            raise ChildProcessError("Packer did not finish build")
        # Move new ova to fileserver
        shutil.move(f"/home/nasko/ova/{version}/FileFlex-{version}.ova",
                    f"/mnt/fileserver/FileFlex-{version}.ova")
        print(f"Moved ova to: filserver/VM/FileFlex-{version}.ova")
        if not args.branch:
            Util.delete_dir(f"/home/nasko/automation/ansible/SVN")
        else:
            Util.delete_dir(f"/home/nasko/automation/ansible/branches/")
        Util.delete_dir(f"/home/nasko/ova/{version}")


class Util:

    @staticmethod
    def delete_dir(path_dir, allow_symlink=False):
        """
        Delete dir on given path if exists.
        :param path_dir Path to dir to delete. Must be valid. Must point to a dir.
                    If point to symlink, allow_symlink=False, will not be deleted.
        :param allow_symlink: True to allow symlinks to be deleted too.
                                If False skip if there is symlink but trace warning.
        """
        if os.path.islink(path_dir):
            if os.path.isdir(path_dir):
                if allow_symlink:
                    os.unlink(path_dir)
                else:
                    print(f"Not allowed to unlink file {path_dir}")
            else:
                raise IOError(f"Try to delete dir as link: {path_dir}")
        else:
            if os.path.exists(path_dir):
                shutil.rmtree(path_dir, ignore_errors=True)
            else:
                print(f"File for delete not found: {path_dir}")


def main():
    args = Args()
    builder = Builder(args)
    builder.build_ova()


if __name__ == '__main__':
    main()
