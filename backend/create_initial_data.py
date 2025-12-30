from models import Role, Specialization, User, db
from flask_security.utils import hash_password
roles = ["Admin", "Doctor", "Patient"]
basic_users = [
    {
        "email": "admin@test.com",
        "password": "password",
        "role": "Admin"
    },
    {
        "email": "patient@test.com",
        "password": "password",
        "role": "Patient"      
    },
    {
        "email": "doctor@test.com",
        "password": "password",
        "role": "Doctor"   
    }
]

specializations = [
    "General Medicine",
    "Cardiology",
    "Orthopedics",
    "Gynecology",
    "Pediatrics"
]

def create_initial_data():
    # Create roles
    for name in roles:
        if not Role.query.filter_by(name=name).first():
            db.session.add(Role(name=name))
    db.session.commit()

    # Create users
    for user_data in basic_users:
        if User.query.filter_by(email=user_data["email"]).first():
            continue

        user = User(
            email=user_data["email"],
            password=hash_password(user_data["password"])
        )

        role = Role.query.filter_by(name=user_data["role"]).first()
        user.roles.append(role)

        db.session.add(user)

    db.session.commit()

    # Create specializations
    for s in specializations:
        if not Specialization.query.filter_by(name=s).first():
            specialization = Specialization(name=s)
            db.session.add(specialization)
    db.session.commit()
