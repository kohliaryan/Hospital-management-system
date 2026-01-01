from datetime import datetime
from marshmallow import Schema, ValidationError, fields, validate

class RegisterSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=8))

class AvailabilitySchema(Schema):
    day_of_week = fields.Str(required=True)
    start_time = fields.Time(required=True, format='%H:%M')
    end_time = fields.Time(required=True, format='%H:%M')

class AddDoctorSchema(Schema):
    name = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=8))
    specializations = fields.List(fields.Str(), required=True)
    description = fields.Str()
    consultation_price = fields.Int(required=True)
    availabilities = fields.List(fields.Nested(AvailabilitySchema), required=True)

def validate_future_date(value):
    if value < datetime.now():
        raise ValidationError("Appointment time must be in the future.")

class BookSchema(Schema):
    doctor_id = fields.Integer(required=True)
    date_time = fields.DateTime(required=True, validate=validate_future_date)
