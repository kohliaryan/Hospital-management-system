from datetime import datetime
from flask import current_app as app, jsonify, request
from flask_login import current_user
from marshmallow import ValidationError
from flask_security.utils import hash_password
from flask_security import roles_required, roles_accepted
from schema import AddDoctorSchema, BookSchema, DignosisSchema, RegisterSchema
from models import Appointment, DoctorAvailability, DoctorProfile, MedicalRecord, PatientProfile, Role, Specialization, User, db

@app.get('/')
def hello():
    return "Server is running!"

@app.post("/api/register")
def register():
    data = request.get_json(silent=True)
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
    data = request.get_json(silent=True)
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
    data = request.get_json(silent=True)
    
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

@app.get("/api/appointments")
@roles_required("Doctor")
def appointments():
    doctor = current_user.doctor_profile
    
    appointments = Appointment.query.filter_by(
        doctor_id=doctor.id, 
        status="scheduled"
    ).order_by(Appointment.appointment_datetime.asc()).all()

    output = []

    for appointment in appointments:
        a = {}
        a["id"] = appointment.id
        a["name"] = appointment.patient.name
        a["age"] = appointment.patient.age
        a["gender"] = appointment.patient.gender
        a["date"] = appointment.appointment_datetime.isoformat()
        
        output.append(a)

    return jsonify(output)

@app.post("/api/appointment/<int:id>/complete")
@roles_required("Doctor")
def complete_appointment(id):
    appointment = Appointment.query.get(id)
    if not appointment:
        return jsonify({"msg": "Invalid Appointment Id"}), 400

    if current_user.doctor_profile != appointment.doctor:
        return jsonify({"msg": "Not Permitted"}), 401
    
    data = request.get_json(silent=True)

    try:
        DignosisSchema().load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    appointment.status = "completed"

    dignosis = MedicalRecord(
        symptoms = data["symptoms"],
        diagnosis = data["diagnosis"],
        treatment = data["treatment"],
        prescription=data.get("prescription"),
        appointment = appointment,
        patient_id = appointment.patient_id
    )
    
    db.session.add(dignosis)
    db.session.commit()
    return jsonify({"msg": "Marked as completed!"})

@app.post("/api/appointment/<int:id>/cancel")
@roles_accepted("Doctor", "Patient") 
def cancel_appointment(id):
    appt = Appointment.query.get_or_404(id)

    if appt.status != "scheduled":
        return jsonify({"msg": "Cannot cancel this appointment (It is already completed or cancelled)"}), 400

    is_authorized = False

    if current_user.has_role("Doctor"):
        if current_user.doctor_profile and appt.doctor_id == current_user.doctor_profile.id:
            is_authorized = True

    elif current_user.has_role("Patient"):
        if current_user.patient_profile and appt.patient_id == current_user.patient_profile.id:
            is_authorized = True

    if not is_authorized:
        return jsonify({"msg": "Unauthorized. You do not own this appointment."}), 403

    appt.status = "cancelled"
    db.session.commit()

    return jsonify({"msg": "Appointment cancelled successfully"}), 200