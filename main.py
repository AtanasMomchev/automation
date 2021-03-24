from flask import Flask, render_template, Request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ffs.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id =

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/create_image')
def provisioning_platform():
    return render_template('Provisioners.html')


@app.route('/create_image/ova', methods=['GET', 'POST'])
def create_ova():
    if Request.method == 'post':
        prod = Request.form['production']
        trunk = Request.form['trunk']
        branch = Request.form['branch']
        branch_number = Request.form['branch_number']
        return [prod, trunk , branch, branch_number]
    else:
        return render_template('ova.html')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app.run(debug=True)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
