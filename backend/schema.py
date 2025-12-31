from marshmallow import Schema, fields, validate

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
    specializations=fields.List(fields.Str(), required=True)
    description=fields.Str()
    availabilities = fields.List(fields.Nested(AvailabilitySchema), required=True)