
from crypt import methods
from flask import Flask, render_template, redirect, url_for, flash
from passlib.hash import pbkdf2_sha256
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from wtforms_field import *
from models import *


# configure app
app = Flask(__name__)

# configure database
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:Promise2022@localhost/postgres'
db = SQLAlchemy(app)

# configure flask login
login = LoginManager(app)
login.init_app(app)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))

#keep clientside secured
app.secret_key = 'replace later'

@app.route("/", methods=['GET', 'POST'])
def index():

    # update database if validation success
    reg_form = RegistrationForm()
    if reg_form.validate_on_submit():
        username = reg_form.username.data
        password = reg_form.password.data
        
        # hash password
        hashed_password = pbkdf2_sha256.hash(password)


        # add user to db
        user = User(username=username, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        
        flash("Registration is successful. Please login.", 'success')
        
        return redirect(url_for('login'))

    return render_template("index.html", form=reg_form)

# login page

@app.route("/login", methods=['GET', 'POST'])
def login():

    login_form = LoginForm()

    # Allow login if validation is successful
    if login_form.validate_on_submit():
        user_object = User.query.filter_by(username=login_form.username.data).first()
        login_user(user_object)
        return redirect(url_for('chat'))
    
    return render_template("login.html", form=login_form)

@app.route("/chat", methods=['GET', 'POST'])

def chat():
    if not current_user.is_authenticated:
        flash("Please login.", 'danger')
        return redirect(url_for('login'))
    
    return "Chat with me"

@app.route("/logout", methods=['GET'])
def logout():
   logout_user()
   
   flash("You have logged out successfully.", 'success')
   return redirect(url_for('login'))
if __name__ == '__main__':
    app.run(debug=True)