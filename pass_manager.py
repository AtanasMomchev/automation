from flask_bcrypt import Bcrypt


class Secrets:

    bcrypt = Bcrypt()

    def hash_password(self, password, salt_level):
        pass_hash = self.bcrypt.generate_password_hash(password, salt_level)
        return pass_hash

    def check_password(self, pw_hash, password):
        #print(pw_hash, password)
        return self.bcrypt.check_password_hash(pw_hash, password)
