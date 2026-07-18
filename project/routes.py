from flask import render_template, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from models import User
from forms import RegistrationForm, LoginForm, AppointmentForm
from extensions import db
from flask import Blueprint

bp = Blueprint("main", __name__)

print("before register route")
@bp.route("/",methods=["GET","POST"]) 
def Register():
    form = RegistrationForm()
    if form.validate_on_submit():
        print("form validated")
        username = form.username.data
        password = generate_password_hash(form.password.data)
        email = form.email.data
        role = "patient"

        user = User(  # object of User
                    username=username,
                    email=email,
                    password=password,
                    role = role
                    )
        existing_1 = User.query.filter_by(username=username).first() 
        existing_2 = User.query.filter_by(email=email).first() 
        if not existing_1: 
            if not existing_2:
                db.session.add(user) # add the given record in the database 
                db.session.commit() # commit the changes 
                return redirect(url_for("main.login")) 
            else:
                flash("Email already exists")
        else: 
            flash("Username already exists") 
    return render_template("Register.html", form= form)


@bp.route("/login", methods= ["GET","POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.query.filter_by(username= username).first()
        admin = User.query.filter_by(username= username,role= "admin").first()
        if admin:
            if check_password_hash(user.password,password):
                login_user(user)
            return redirect(url_for("main.admin"))              
        if user:
            if check_password_hash(user.password,password):
                login_user(user) # data check krke user ko session me daal deta hai
                return redirect(url_for("main.home"))
            else:
                flash("Incorrect password") 
        else:
            flash("User doesnot exist")   
    return render_template("login.html", form = form)


@bp.route("/home")
@login_required
def home():
    if current_user.role== "doctor":
        return render_template("success.html")
    elif current_user.role=="patient":
        return render_template("home.html")


@bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "success")
    return redirect(url_for("main.login"))


@bp.route("/admin90")
@login_required
def admin():
    return render_template("admin.html")

@bp.route("/book_appointment", methods=["GET","POST"])
@login_required
def book_appointment():
    form = AppointmentForm()
    return render_template("book_appointment.html", form=form)