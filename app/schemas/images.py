from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from app.models.models import Image


class ImageSchema(SQLAlchemyAutoSchema):
    class Meta:
        table = Image.__table__