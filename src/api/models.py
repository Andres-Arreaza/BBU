from flask_sqlalchemy import SQLAlchemy
from enum import Enum
from flask_admin.contrib.sqla import ModelView

db = SQLAlchemy()

class RoleEnum(Enum):
    PATIENT = "PATIENT"
    DOCTOR = "DOCTOR"
    MANAGER = "MANAGER"

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    country = db.Column(db.String(80), nullable=False)
    city = db.Column(db.String(80), nullable=False)
    age = db.Column(db.String(80), nullable=False)
    role = db.Column(db.Enum(RoleEnum), nullable=False)
    img_url = db.Column(db.String(250))

    appointments = db.relationship("Appointment", back_populates="patient", lazy=True)
    testimonials = db.relationship("Testimonial", back_populates="patient", lazy=True)
    doctors = db.relationship("Doctor", back_populates="user", lazy=True)
    medical_histories = db.relationship("MedicalHistory", back_populates="patient", lazy=True)

    def __repr__(self):
        return f'<User {self.id}, {self.email}>'

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "country": self.country,
            "city": self.city,
            "age": self.age,
            "role": self.role.value,
            "img_url": self.img_url,
        }

    def serialize_doctors(self):
        return [doctor.serialize() for doctor in self.doctors]


class Doctor(db.Model):
    __tablename__ = 'doctors'

    id = db.Column(db.Integer, primary_key=True)
    speciality = db.Column(db.String(100), nullable=False)
    time_availability = db.Column(db.String(100), nullable=False)
    medical_consultant_price = db.Column(db.Float, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    user = db.relationship(User)
    appointments = db.relationship("Appointment", back_populates="doctor", lazy=True)
    medical_histories = db.relationship("MedicalHistory", back_populates="doctor", lazy=True)

    def __repr__(self):
        return f'<Doctor {self.id}>'

    def serialize(self):
        return {
            "id": self.id,
            "info": self.user.serialize() if self.user else None,
            "speciality": self.speciality,
            "time_availability": self.time_availability,
            "medical_consultant_price": self.medical_consultant_price,
        }


class Appointment(db.Model):
    __tablename__ = 'appointments'

    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    doctor_id = db.Column(db.Integer, db.ForeignKey("doctors.id"))
    date = db.Column (db.DateTime)

    doctor = db.relationship(Doctor)
    patient = db.relationship(User)

    def __repr__(self):
        return f'<Appointment {self.id}>'

    def serialize(self):
        return {
            "id": self.id,
            "patient_id": self.patient.id if self.patient else None,
            "doctor_id": self.doctor.id if self.doctor else None,
            "date": self.date.isoformat() if self.date else None
        }


class TestimonialCount(Enum):
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5

class Testimonial(db.Model):
    __tablename__ = "testimonials"

    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    content = db.Column(db.String(256), nullable=False)
    count = db.Column(db.Enum(TestimonialCount))

    patient = db.relationship(User)

    def __repr__(self):
        return f'<Testimonial {self.id}>'

    def serialize(self):
        return {
            "id": self.id,
            # "patient": {"first_name": self.patient.first_name, "last_name": self.patient.last_name, "img_url": self.patient.img_url},
            "patient": {"first_name": self.patient.first_name, "last_name": self.patient.last_name},
            "content": self.content,
            "count": self.count.value if self.count else None
        }


class TokenBlockedList(db.Model):
    __tablename__ = 'token_blocked_list'

    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(50), unique=True, nullable=False)

    def __repr__(self):
        return f'<TokenBlockedList {self.jti}>'

    def serialize(self):
        return {
            "id": self.id,
            "jti": self.jti,
        }

class MedicalHistory(db.Model):
    __tablename__ = 'medical_histories'

    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey("doctors.id"), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    observation = db.Column(db.String(1000), nullable=True)

    doctor = db.relationship(Doctor, back_populates="medical_histories")
    patient = db.relationship(User, back_populates="medical_histories")

    def __repr__(self):
        return f'<MedicalHistory {self.id}>'

    def serialize(self):
        return {
            "id": self.id,
            "doctor": self.doctor.serialize() if self.doctor else None,
            "patient": self.patient.serialize() if self.patient else None,
            "created_at": self.created_at,
            "observation": self.observation
        }

class MedicalHistoryView(ModelView):
    column_list = ('id', 'doctor_id', 'patient_id', 'created_at', 'observation')
    form_columns = ('doctor_id', 'patient_id', 'observation')