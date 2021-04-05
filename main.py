from flask import Flask, render_template, Request, request
from database import db_session
from database import init_db
from models.User import User
from secrets import Secrets
from sqlalchemy.sql import text

app = Flask(__name__)
app.debug = True
init_db()
if not User.query.filter(User.name == 'admin').first():
    u = User("admin", "Q!w2e3r4")
    db_session.add(u)
    db_session.comit()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        secret = Secrets()
        username = request.form['username']
        password = request.form['password']
        print(username, password)
        pass_from_db = User.query.filter(User.name == 'admin')
        db_session.flush()
        print(pass_from_db, "\n")
        if secret.check_password(pass_from_db, password.encode('utf-8')):
            return render_template('index.html')
        else:
            return render_template('login.html')
    else:
        return render_template('login.html')


@app.route('/create_image/ova', methods=['GET', 'POST'])
def create_ova():
    if Request.method == 'post':
        prod = Request.form['production']
        trunk = Request.form['trunk']
        branch = Request.form['branch']
        branch_number = Request.form['branch_number']
        return [prod, trunk, branch, branch_number]
    else:
        return render_template('ova.html')


@app.route('/create_image')
def provisioning_platform():
    return render_template('Provisioners.html')


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app.run(debug=True)

