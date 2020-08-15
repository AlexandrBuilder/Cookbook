from datetime import datetime
from app.models import db
from passlib.hash import sha256_crypt


class BaseModel(db.Model):
    @classmethod
    def insert_by_list_data(cls, data_list):
        return cls.insert().values(data_list).returning(cls.__table__).gino.all()


class User(BaseModel):
    __tablename__ = 'users'

    STATUS_ACTIVE = 'active'
    STATUS_BLOCKED = 'blocked'

    STATUSES = [STATUS_ACTIVE, STATUS_BLOCKED]

    ROLE_USER = 'user'
    ROLE_ADMIN = 'admin'

    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False, index=True)
    password = db.Column(db.String(150))
    status = db.Column(db.String(30), nullable=False, default=STATUS_ACTIVE, index=True)
    role = db.Column(db.String(30), nullable=False, default=ROLE_USER, index=True)
    count_recipes = db.Column(db.Integer(), default=0)
    count_likes = db.Column(db.Integer(), default=0)

    def set_password(self, password):
        self.password = sha256_crypt.hash(password)

    def check_password(self, password):
        return sha256_crypt.verify(password, self.password)


class Image(db.Model):
    __tablename__ = 'images'

    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(200), nullable=False)


class Recipe(db.Model):
    __tablename__ = 'recipes'

    STATUS_ACTIVE = 'active'
    STATUS_BLOCKED = 'blocked'

    STATUSES = [STATUS_ACTIVE, STATUS_BLOCKED]

    TYPE_SALAD = 'salad'
    TYPE_FIRST_COURSE = 'first course'
    TYPE_SECOND_COURSE = 'second course'
    TYPE_SOUP = 'soup'
    TYPE_DESSERT = 'dessert'
    TYPE_DRINK = 'drink'

    TYPES = [TYPE_SALAD, TYPE_FIRST_COURSE, TYPE_SECOND_COURSE, TYPE_SOUP, TYPE_DESSERT, TYPE_DRINK]

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False, index=True)
    description = db.Column(db.String(3000), nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(db.String(30), nullable=False, default=STATUS_ACTIVE)
    type = db.Column(db.String(50), nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    image_id = db.Column(db.Integer, db.ForeignKey('images.id'))
    count_likes = db.Column(db.Integer(), default=0)

    def __init__(self, **kw):
        super().__init__(**kw)
        self._recipe_steps = set()
        self._tags = set()
        self._user = None

    @property
    def recipe_steps(self):
        return self._recipe_steps

    @recipe_steps.setter
    def recipe_steps(self, recipe_steps):
        self._recipe_steps = recipe_steps

    def add_recipe_step(self, recipe_step):
        print(recipe_step)
        self._recipe_steps.add(recipe_step)

    @property
    def tags(self):
        return self._tags

    @tags.setter
    def tags(self, tags):
        self._tags = tags

    def add_tag(self, tag):
        self._tags.add(tag)

    @property
    def user(self):
        return self._user

    @user.setter
    def user(self, user):
        self._user = user


class RecipeStep(BaseModel):
    __tablename__ = 'recipe_steps'

    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(3000), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'))


class Tag(BaseModel):
    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)


class RecipeXTag(BaseModel):
    __tablename__ = 'recipe_x_tag'

    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'), nullable=False)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), nullable=False)


class Like(BaseModel):
    __tablename__ = 'likes'

    id = db.Column(db.Integer(), primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('tags.id'), nullable=False)


class SelectedRecipe(BaseModel):
    __tablename__ = 'selected_recipes'

    id = db.Column(db.Integer(), primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('tags.id'), nullable=False)
