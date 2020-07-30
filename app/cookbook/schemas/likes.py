from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field

from app.models.models import Like


class LikeCreateSchema(SQLAlchemyAutoSchema):
    class Meta:
        table = Like.__table__

    recipe_id = auto_field(required=True)


class LikeSchema(SQLAlchemyAutoSchema):
    class Meta:
        table = Like.__table__
        include_fk = True
