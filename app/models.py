from . import db
from datetime import datetime

class User(db.Model):
    id       = db.Column(db.Integer, primary_key=True)
    email    = db.Column(db.String(150), unique=True, nullable=False)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    lifestyle_data = db.relationship('LifestyleData', backref='user', lazy=True)
    appointments = db.relationship('Appointment', backref='user', lazy=True)

class LifestyleData(db.Model):
    id               = db.Column(db.Integer, primary_key=True)
    sleep_hours      = db.Column(db.Float, nullable=False)
    diet_quality     = db.Column(db.String(100), nullable=False)
    exercise_minutes = db.Column(db.Integer, nullable=False)
    stress_level     = db.Column(db.String(50), nullable=False)
    timestamp        = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Doctor(db.Model):
    id        = db.Column(db.Integer, primary_key=True)
    name      = db.Column(db.String(150), nullable=False)
    specialty = db.Column(db.String(100), nullable=False)
    appointments = db.relationship('Appointment', backref='doctor', lazy=True)

class Appointment(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    user_id     = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    doctor_id   = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    date        = db.Column(db.Date, nullable=False)
    time_slot   = db.Column(db.String(50), nullable=False)  # e.g., "09:00 AM"
    status      = db.Column(db.String(20), default='booked', nullable=False)  # booked, cancelled
    created_at  = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)