from flask import render_template, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from models import User,Appointment
from forms import RegistrationForm, LoginForm, AppointmentForm
from extensions import db
from flask import Blueprint

bp = Blueprint("main", __name__)

@bp.route("/register",methods=["GET","POST"]) 
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
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
                flash("This email is already registered","warning")
        else: 
            flash("Username is already taken","warning") 
    return render_template("Register.html", form= form,title = "Patient Registration")


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
            return redirect(url_for("main.admin_dashboard"))              
        if user:
            if check_password_hash(user.password,password):
                login_user(user) # data check krke user ko session me daal deta hai
                return redirect(url_for("main.home"))
            else:
                flash("Incorrect password","danger") 
        else:
            flash("User doesnot exist", "danger")   
    return render_template("login.html", form = form)


@bp.route("/")
def home():
    return render_template("home.html")


@bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "success")
    return redirect(url_for("main.login"))

@bp.route("/admin")
@login_required
def admin_dashboard():

    if current_user.role != "admin":
        flash("You are not authorized to access this page.","danger")
        return redirect(url_for("main.home"))

    total_doctors = User.query.filter_by(role="doctor").count()
    total_patients = User.query.filter_by(role="patient").count()
    total_appointments = Appointment.query.count()
    pending_appointments = Appointment.query.filter_by(status="pending").count()

    return render_template(
        "admin_dashboard.html",
        total_doctors=total_doctors,
        total_patients=total_patients,
        total_appointments=total_appointments,
        pending_appointments=pending_appointments
    )

@bp.route("/admin/doctors")
@login_required
def manage_doctors():

    if current_user.role != "admin":
        flash("You are not authorized to access this page.", "danger")
        return redirect(url_for("main.home"))
    
    doctors=User.query.filter_by(role = "doctor").all()
    return render_template("manage_doctors.html", doctors=doctors)


@bp.route("/admin/add_doctors", methods= ["GET","POST"])
@login_required
def add_doctors():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        password = generate_password_hash(form.password.data)
        email = form.email.data
        role = "doctor"

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
                flash("Registration successful","success")
                db.session.add(user) # add the given record in the database 
                db.session.commit() # commit the changes 
                return redirect(url_for("main.add_doctors")) 
            else:
                flash("Email already exists","warning")
        else: 
            flash("Username already exists","warning") 
    return render_template("Register.html", form= form, title = "Doctor Registration")


@bp.route("/admin/delete_doctor/<int:doctor_id>")
@login_required
def delete_doctor(doctor_id):

    if current_user.role != "admin":
        flash("You are not authorized to access this page.","danger")
        return redirect(url_for("main.home"))

    doctor = db.session.get(User, doctor_id)

    if doctor is None:
        flash("Doctor not found.","danger")
        return redirect(url_for("main.manage_doctors"))

    if doctor.role != "doctor":
        flash("Selected user is not a doctor.","warning")
        return redirect(url_for("main.manage_doctors"))

    if doctor.doctor_appointment:
        flash("Cannot delete a doctor who has appointments.","warning")
        return redirect(url_for("main.manage_doctors"))

    db.session.delete(doctor)
    db.session.commit()

    flash("Doctor deleted successfully.","success")
    return redirect(url_for("main.manage_doctors"))


@bp.route("/book_appointment", methods=["GET","POST"])
@login_required
def book_appointment():
    form = AppointmentForm()
    doctors = User.query.filter_by(role = "doctor").all()
    form.doctor.choices = [(doctor.id, doctor.username) for doctor in doctors]
    if form.validate_on_submit():
        appointment = Appointment(
                            patient_id=current_user.id,
                            doctor_id=form.doctor.data,
                            appointment_date=form.appointment_date.data,
                            appointment_time=form.appointment_time.data,
                            reason=form.reason.data
                            )

        db.session.add(appointment)
        db.session.commit()
        flash("Appointment successful!","success")
        return redirect(url_for("main.home"))
    return render_template("book_appointment.html", form=form)

@bp.route("/my_appointments")
@login_required
def my_appointments():
    if current_user.role=="patient":
        appointment= current_user.patient_appointment
    elif current_user.role=="doctor":
        pending= Appointment.query.filter_by(doctor_id=current_user.id,status="pending").count()
        approved= Appointment.query.filter_by(doctor_id=current_user.id,status="approved").count()
        completed= Appointment.query.filter_by(doctor_id=current_user.id,status="completed").count()
        appointment= current_user.doctor_appointment
    else:
        flash("Unauthorized","danger")
        return redirect(url_for("main.home"))
    return render_template("appointment.html",appointments=appointment, role=current_user.role, pending=pending,approved=approved,completed=completed )


@bp.route("/cancel/<int:appointment_id>")
@login_required
def cancel_appointment(appointment_id):
    appointment= db.session.get(Appointment,appointment_id)
    if appointment is None:
        flash("appointment not found","danger")
        return redirect(url_for("main.my_appointments"))
    
    if appointment.patient_id != current_user.id and appointment.doctor_id != current_user.id :
        flash("You cannot cancel this","danger")
        return redirect(url_for("main.my_appointments"))
    
    if appointment.status != "pending" and current_user.role == "patient":
        flash("Only pending appointments can be cancelled.", "warning")
        return redirect(url_for("main.my_appointments"))

    appointment.status= "cancelled"
    db.session.commit()
    flash("Appointment cancelled successfully.","success")
    return redirect(url_for("main.my_appointments"))
    
@bp.route("/update_status/<int:appointment_id>/<status>")    
@login_required
def update_status(appointment_id, status):

    if current_user.role != "doctor":
        flash("Access denied","danger")
        return redirect(url_for("main.home"))

    appointment = db.session.get(Appointment, appointment_id)

    if appointment is None:
        flash("appointment not found","danger")
        return redirect(url_for("main.my_appointments"))


    if appointment.doctor_id != current_user.id:
        flash("You are not assigned to this appointment.","danger")
        return redirect(url_for("main.home"))
    

    allowed_status=["rejected","approved","completed"]
    if status in allowed_status:
        appointment.status = status
        db.session.commit()
        flash("Status updated","success")
    
    else:
        flash("Invalid status","danger")

    return redirect(url_for("main.my_appointments"))