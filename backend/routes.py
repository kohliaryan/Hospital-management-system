from flask import current_app as app, jsonify, request
from marshmallow import ValidationError
from flask_security.utils import hash_password
from schema import RegisterSchema
from models import Role, User, db

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