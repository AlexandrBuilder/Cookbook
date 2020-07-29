from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from app.models.models import Tag


class TagCreateSchema(SQLAlchemyAutoSchema):
    class Meta:
        table = Tag.__table__
        exclude = ('id',)


class TagSchema(SQLAlchemyAutoSchema):
    class Meta:
        table = Tag.__table__