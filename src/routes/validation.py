from marshmallow import Schema, fields, validate


RegistrationSchema = Schema.from_dict({
    "username": fields.Str(required=True),
    "email": fields.Email(required=True),
    "password": fields.Str(required=True),
    "notification": fields.Str()
})

LoginSchema = Schema.from_dict({
    "email": fields.Email(required=True),
    "password": fields.Str(required=True)
})

UpdateUserSchema = Schema.from_dict({
    "username": fields.Str(),
    "email": fields.Email(),
    "password": fields.Str(),
    "userId": fields.Str(required=True),
    "sessionId": fields.Str(required=True),
    "notification": fields.Str()
})