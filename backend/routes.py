from datetime import datetime
from flask import current_app as app, jsonify, request
from flask_login import current_user
from marshmallow import ValidationError
from flask_security.utils import hash_password
from flask_security import roles_required
from schema import AddDoctorSchema, BookSchema, RegisterSchema
from models import Appointment, DoctorAvailability, DoctorProfile, PatientProfile, Role, Specialization, User, db

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
    
    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"msg": "Email is already reigisterd."}), 403

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
    data = request.get_json()
    
    try:
        BookSchema().load(data=data)
    except ValidationError as err:
        return jsonify(err.messages), 400

    doctor = DoctorProfile.query.get(data["doctor_id"])
    if not doctor:
        return jsonify({"msg": "Invalid doctor id"}), 404

    try:
        dt_object = datetime.fromisoformat(data["date_time"]).replace(tzinfo=None)
    except ValueError:
        return jsonify({"msg": "Invalid date format"}), 400

    if dt_object < datetime.now():
        return jsonify({"msg": "You cannot book appointments in the past"}), 400

    if dt_object.minute not in [0, 30]:
        return jsonify({"msg": "Slots must be at :00 or :30 minutes"}), 400

    day_name = dt_object.strftime("%A")

    slot_found_in_schedule = False
    
    for availability in doctor.availabilities:
        if availability.day_of_week == day_name:
            if availability.start_time <= dt_object.time() < availability.end_time:
                slot_found_in_schedule = True
                break
    
    if not slot_found_in_schedule:
        return jsonify({"msg": "Doctor is not available at this time"}), 400

    existing_appointment = Appointment.query.filter_by(
        doctor_id=doctor.id, 
        appointment_datetime=dt_object,
        status="scheduled"
    ).first()

    if existing_appointment:
        return jsonify({"msg": "Slot is already booked!"}), 400

    if not current_user.patient_profile:
         return jsonify({"msg": "User profile not found"}), 400

    appointment = Appointment(
        doctor=doctor, 
        patient=current_user.patient_profile,
        price=doctor.consultation_price, 
        appointment_datetime=dt_object
    )
    
    db.session.add(appointment)
    db.session.commit()

    return jsonify({"msg": "Appointment Scheduled"}), 201