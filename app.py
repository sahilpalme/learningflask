from flask import Flask, render_template,redirect, request,url_for,flash,session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from form import RegistrationForm, LoginForm
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user


app= Flask(__name__)

app.secret_key= "my-secret-key"


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"  # database path
db = SQLAlchemy(app) # object that will connect sql with flask
login_manager= LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

class User(db.Model): # table in database
    id = db.Column(db.Integer, primary_key= True)
    username= db.Column(db.String(100), unique=True, nullable = False)
    email= db.Column(db.String(100),unique=True, nullable = False)
    password = db.Column(db.String(100), nullable = False)

with app.app_context():
        db.create_all()

@app.route("/",methods=["GET","POST"]) 
def Register():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        password = generate_password_hash(form.password.data)
        email = form.email.data


        user = User(   # object of User
                    username=username,
                    email=email,
                    password=password
                    )
        db.session.add(user)  # add the given record in the database
        db.session.commit() # commit the changes

        return redirect(url_for("login"))
    return render_template("Register.html", form= form)    
    
@app.route("/login", methods= ["GET","POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.query.filter_by(username= username).first()
        if user:
            if check_password_hash(user.password,password):
                session["username"]= username
                return redirect(url_for("success"))
            else:
                flash("Incorrect password") 
        else:
            flash("User doesnot exist")             
    return render_template("login.html", form = form)

@app.route("/success")
def success():
    if "username" in session:
        flash("Login successful!")
        return render_template("success.html")
    else:
        return redirect(url_for("login"))


if __name__ == "__main__":

    app.run(debug=True)