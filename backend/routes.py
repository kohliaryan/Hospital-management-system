from flask import current_app as app, jsonify, request
from marshmallow import ValidationError
from flask_security.utils import hash_password
from flask_security import roles_required, roles_accepted
from schema import AddDoctor, RegisterSchema
from models import DoctorProfile, Role, Specialization, User, db

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
        AddDoctor().load(data=data)
    except ValidationError as err:
        return jsonify(err.messages), 400
    s = Specialization.query.filter_by(name=data["specialization"]).first()
    if not s:
        return jsonify({"msg": "No such specialization exsists!"}), 404
    user = User(email=data["email"], password=hash_password(data["password"]))
    doctor = DoctorProfile(name=data["name"], description=data.get("description", ""), user=user)
    doctor.specializations.append(s)
    db.session.add_all([user, doctor])
    db.session.commit()
    return jsonify({"msg": "Doctor added successfully!"}), 201
