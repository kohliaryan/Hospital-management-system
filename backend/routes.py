from datetime import datetime
from flask import current_app as app, jsonify, request
from marshmallow import ValidationError
from flask_security.utils import hash_password
from flask_security import roles_required
from schema import AddDoctorSchema, RegisterSchema
from models import DoctorAvailability, DoctorProfile, PatientProfile, Role, Specialization, User, db

@app.get('/')
def hello():
    return "Server is running!"

@app.post("/api/register")
def register():
    data = request.get_json()
    try:
        RegisterSchema().load(data=data)
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    user = User.query.filter_by(email=data["email"]).first()
    if user:
        return jsonify({"msg": "User already exsist!"}), 400
    
    user = User(email=data["email"], password=hash_password(data["password"]))
    role = Role.query.filter_by(name="Patient").first()
    user.roles.append(role)
    db.session.add(user)
    db.session.commit()
    return jsonify({"msg": "User created successfully!"}), 201

@app.post("/api/doctor")
@roles_required("Admin")
def add_doctor():
    data = request.get_json()
    try:
        AddDoctorSchema().load(data=data)
    except ValidationError as err:
        return jsonify(err.messages), 400

    user = User(email=data["email"], password=hash_password(data["password"]))
    doctor = DoctorProfile(name=data["name"], description=data.get("description", ""),consultation_price=data["consultation_price"], user=user)

    for s in data.get("specializations"):
        doctor.specializations.append(Specialization.query.filter_by(name=s).first())

    for a in data["availabilities"]:
        s_time = datetime.strptime(a["start_time"], "%H:%M").time()
        e_time = datetime.strptime(a["end_time"], "%H:%M").time()
        availability = DoctorAvailability(doctor=doctor, day_of_week=a["day_of_week"], start_time=s_time, end_time=e_time)
        doctor.availabilities.append(availability)

    db.session.add_all([user, doctor])
    db.session.commit()
    return jsonify({"msg": "Doctor added successfully!"}), 201

@app.get("/api/doctors")
def doctors():
    doctors = []
    for doctor in DoctorProfile.query.all():
        d = {}
        d["name"] = doctor.name
        d["description"] = doctor.description
        d["consultation_price"] = doctor.consultation_price
        d["specializations"] = []
        for s in doctor.specializations:
            d["specializations"].append(s.name)
        doctors.append(d)
    return doctors

@app.get("/api/patients")
def patients():
    patients = []
    for patient in PatientProfile.query.all():
        p = {}
        p["name"] = patient.name
        p["age"] = patient.age
        p["gender"] = patient.gender
        patients.append(p)
    return patients

@app.post("/api/book")
@roles_required("Patient")
def book():
    return "Hello Patient!"