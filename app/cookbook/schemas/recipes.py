from marshmallow import validate, validates, ValidationError, fields, Schema
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from marshmallow_sqlalchemy.fields import Nested

from app.models.models import Recipe, RecipeStep
from app.cookbook.schemas.tags import TagCreateSchema, TagSchema
from app.cookbook.schemas.users import UserRecipeSchema
from app.cookbook.schemas.recipe_step import RecipeStepCreateSchema


class RecipeCreateSchema(SQLAlchemyAutoSchema):
    class Meta:
        table = Recipe.__table__
        exclude = ('id', 'status', 'created', 'user_id')

    type = auto_field(validate=validate.OneOf(Recipe.TYPES))
    image_id = auto_field()
    recipe_steps = Nested(RecipeStepCreateSchema, many=True)
    tags = Nested(TagCreateSchema, many=True)
    user = Nested(UserRecipeSchema, many=False)

    @validates('recipe_steps')
    def validate_recipe_steps(self, recipe_steps):
        numbers = []
        for recipe_step in recipe_steps:
            number = recipe_step['number']
            if number in numbers:
                raise ValidationError('The number of the "{}" step of the recipe is repeated'.format(number))
            numbers.append(number)

    @validates('tags')
    def validate_tags(self, tags):
        tags_list = [tag['name'] for tag in tags]
        if len(tags_list) != len(set(tags_list)):
            raise ValidationError('The sequence has repeating tags')


class RecipeSchema(SQLAlchemyAutoSchema):
    class Meta:
        table = Recipe.__table__

    image_id = auto_field()
    recipe_steps = Nested(RecipeStepCreateSchema, many=True)
    tags = Nested(TagSchema, many=True)
    user = Nested(UserRecipeSchema, many=False)


class RecipeLifterSchema(Schema):
    SORT_DESC = 'desc'
    SORT_ASC = 'asc'

    SORTS = [SORT_ASC, SORT_DESC]

    tag = fields.Str(validate=validate.Length(max=100))
    name = fields.Str(validate=validate.Length(max=250))
    type = fields.Str(validate=validate.OneOf(Recipe.TYPES))
    user_id = fields.Int()
    has_image = fields.Bool()
    created_sort = fields.Str(validate=validate.OneOf(SORTS))
    name_sort = fields.Str(validate=validate.OneOf(SORTS))
    count_likes_sort = fields.Str(validate=validate.OneOf(SORTS))
    page = fields.Int(missing=1)
    per_page = fields.Int(missing=10, validate=validate.Range(max=100))


class RecipeChangeStatusSchema(SQLAlchemyAutoSchema):
    status = fields.Str(required=True, validate=validate.OneOf(Recipe.STATUSES))
