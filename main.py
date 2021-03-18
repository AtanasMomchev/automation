from flask import Flask, render_template, request
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/create_image')
def provisioning_platform():
    return render_template('Provisioners.html')


@app.route('/create_image/ova', methods=['GET', 'POST'])
def create_ova():
    if request == 'POST':
        is_trunk = request
    return render_template('ova.html')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app.run(debug=True)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
