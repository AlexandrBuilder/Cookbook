from marshmallow import Schema, fields, validate
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from app.models.models import User


class UserRegistrationAndAuthSchema(Schema):
    username = fields.Str(required=True, validate=validate.Length(min=4, max=100))
    password = fields.Str(required=True, validate=validate.Length(min=8, max=100))


class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        table = User.__table__
        exclude = ('password',)


class UserChangeStatusSchema(SQLAlchemyAutoSchema):
    status = fields.Str(required=True, validate=validate.OneOf(User.STATUSES))


class UserListSchema(SQLAlchemyAutoSchema):
    collaborators = fields.List(fields.Nested(UserSchema))


class UserRecipeSchema(SQLAlchemyAutoSchema):
    class Meta:
        table = User.__table__
        exclude = ('password', 'role')
