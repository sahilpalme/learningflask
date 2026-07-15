from flask import Flask, render_template,redirect, request,url_for,flash,session
from werkzeug.security import generate_password_hash, check_password_hash
from form import RegistrationForm, LoginForm
from flask_login import LoginManager, UserMixin, current_user, login_user, logout_user, login_required
from model import User
from extensions import db, login_manager
app= Flask(__name__)

app.secret_key= "my-secret-key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"  # database path

db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = "login"




@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

with app.app_context():
        db.create_all()

@app.route("/",methods=["GET","POST"]) 
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
                return redirect(url_for("login")) 
            else:
                flash("Email already exists")
        else: 
            flash("Username already exists") 
    return render_template("Register.html", form= form)
@app.route("/login", methods= ["GET","POST"])
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
            return redirect(url_for("admin"))              
        if user:
            if check_password_hash(user.password,password):
                login_user(user) # data check krke user ko session me daal deta hai
                return redirect(url_for("home"))
            else:
                flash("Incorrect password") 
        else:
            flash("User doesnot exist")   
    return render_template("login.html", form = form)

@app.route("/home")
@login_required
def home():
    if current_user.role== "doctor":
        return render_template("success.html") # current_user.username shows the username of the user in session
    elif current_user.role=="patient":
        return render_template("home.html")
    



@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "success")
    return redirect(url_for("login"))


@app.route("/admin90")
@login_required
def admin():
    return render_template("admin.html")


if __name__ == "__main__":

    app.run(debug=True)
