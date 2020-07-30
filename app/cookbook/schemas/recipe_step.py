from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from app.models.models import RecipeStep


class RecipeStepCreateSchema(SQLAlchemyAutoSchema):
    class Meta:
        table = RecipeStep.__table__
