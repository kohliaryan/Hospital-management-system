import uuid
from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin, RoleMixin

db = SQLAlchemy()


user_roles = db.Table(
    "user_roles",
    db.Column("user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
    db.Column("role_id", db.Integer, db.ForeignKey("role.id"), primary_key=True)
)


class User(db.Model, UserMixin):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean(), default=True)

    fs_uniquifier = db.Column(
        db.String(255),
        unique=True,
        nullable=False,
        default=lambda: str(uuid.uuid4())
    )

    roles = db.relationship(
        "Role",
        secondary=user_roles,
        backref=db.backref("users", lazy="dynamic")
    )


class Role(db.Model, RoleMixin):
    __tablename__ = "role"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)


class Specialization(db.Model):
    __tablename__ = "specialization"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)


doctor_specializations = db.Table(
    "doctor_specializations",
    db.Column(
        "doctor_id",
        db.Integer,
        db.ForeignKey("doctor_profile.id"),
        primary_key=True
    ),
    db.Column(
        "specialization_id",
        db.Integer,
        db.ForeignKey("specialization.id"),
        primary_key=True
    )
)


class DoctorProfile(db.Model):
    __tablename__ = "doctor_profile"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False,
        unique=True,
        index=True
    )

    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255))

    user = db.relationship(
        "User",
        backref=db.backref("doctor_profile", uselist=False)
    )

    specializations = db.relationship(
        "Specialization",
        secondary=doctor_specializations,
        backref=db.backref("doctors", lazy="dynamic")
    )

class DoctorAvailability(db.Model):
    __tablename__ = "doctor_availability"

    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey("doctor_profile.id"), nullable=False)
    day_of_week = db.Column(db.String(10), nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)

    doctor = db.relationship("DoctorProfile", backref="availabilities")

class Appointment(db.Model):
    __tablename__ = "appointment"
    
    id = db.Column(
        db.Integer, 
        primary_key=True)

    doctor_id = db.Column(
        db.Integer, 
        db.ForeignKey("doctor_profile.id"), 
        nullable=False
        )

    patient_id = db.Column(
        db.Integer,
        db.ForeignKey("patient_profile.id"), 
        nullable=False)

    appointment_datetime = db.Column(
        db.DateTime,
        nullable=False,
        index=True
    )

    status = db.Column(
        db.String(10),
        default="scheduled",
        nullable=False
    )

    doctor = db.relationship("DoctorProfile", backref="appointments")
    patient = db.relationship("PatientProfile", backref="appointments")

class PatientProfile(db.Model):
    __tablename__ = "patient_profile"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False, unique=True, index=True)

    user = db.relationship("User", backref=db.backref("patient_profile", uselist=False))

