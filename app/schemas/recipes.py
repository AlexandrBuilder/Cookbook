from marshmallow import validate, validates, ValidationError
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from marshmallow_sqlalchemy.fields import Nested

from app.models.models import Recipe, RecipeStep


class RecipeStepCreateSchema(SQLAlchemyAutoSchema):
    class Meta:
        table = RecipeStep.__table__


class RecipeSchema(SQLAlchemyAutoSchema):
    class Meta:
        table = Recipe.__table__

    recipe_steps = Nested(RecipeStepCreateSchema, many=True)


class RecipeCreateSchema(SQLAlchemyAutoSchema):
    class Meta:
        table = Recipe.__table__
        exclude = ('id', 'status', 'created', 'user_id')

    type = auto_field(validate=validate.OneOf(Recipe.TYPES))
    recipe_steps = Nested(RecipeStepCreateSchema, many=True)

    @validates('recipe_steps')
    def validate_bob(self, recipe_steps):
        numbers = []
        for recipe_step in recipe_steps:
            number = recipe_step['number']
            if number in numbers:
                raise ValidationError('The number of the "{}" step of the recipe is repeated'.format(number))
            numbers.append(number)
