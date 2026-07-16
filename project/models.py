from flask_login import UserMixin
from extensions import db


class User(UserMixin ,db.Model ): # table in database
    id = db.Column(db.Integer, primary_key= True)
    username= db.Column(db.String(100), unique=True, nullable = False)
    email= db.Column(db.String(100),unique=True, nullable = False)
    password = db.Column(db.String(100), nullable = False)
    role = db.Column(db.String(100), nullable = False )
    patient_appointment = db.relationship('Appointment',foreign_key="Appointment.patient_id", back_populates="patient") # this took all the info from appointment whose patient id is patient_id
    doctor_appointment = db.relationship('Appointment',foreign_key="Appointment.doctor_id", back_populates="doctor")

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable = False) # here patient_id is the foreign key which is connected to user.id
    doctor_id =  db.Column(db.Integer, db.ForeignKey("user.id"), nullable = False)
    appointment_date = db.Column(db.Date, nullable= False)
    appointment_time = db.Column(db.Time, nullable= False)
    reason = db.Column(db.Text, nullable= False)
    status= db.Column(db.String(100), nullable = False, default= "pending")
    patient = db.relationship("User",foreign_keys=[patient_id], back_populates="patient_appointment") # it takes info from User from the way of patient_id as we have two foreign keys patient_id and doctor_id
    doctor = db.relationship("User",foreign_keys=[doctor_id], back_populates="doctor_appointment")