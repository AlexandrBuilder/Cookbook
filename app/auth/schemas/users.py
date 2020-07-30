from marshmallow import Schema, fields, validate


class UserAuthSchema(Schema):
    username = fields.Str(required=True, validate=validate.Length(min=4, max=100))
    password = fields.Str(required=True, validate=validate.Length(min=8, max=100))
