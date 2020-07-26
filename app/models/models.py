from datetime import datetime
from app.models import db
from passlib.hash import sha256_crypt


class User(db.Model):
    __tablename__ = "users"

    STATUS_ACTIVE = 'active'
    STATUS_BLOCKED = 'blocked'

    STATUSES = [STATUS_ACTIVE, STATUS_BLOCKED]

    ROLE_USER = 'user'
    ROLE_ADMIN = 'admin'

    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(150))
    status = db.Column(db.String(30), nullable=False, default=STATUS_ACTIVE)
    role = db.Column(db.String(30), nullable=False, default=ROLE_USER)

    def __mapper__(self):
        pass

    def set_password(self, password):
        self.password = sha256_crypt.hash(password)

    def check_password(self, password):
        return sha256_crypt.verify(password, self.password)


class Recipe(db.Model):
    __tablename__ = "recipes"

    STATUS_ACTIVE = 'active'
    STATUS_BLOCKED = 'blocked'

    TYPE_SALAD = 'salad'
    TYPE_FIRST_COURSE = 'first course'
    TYPE_SECOND_COURSE = 'second course'
    TYPE_SOUP = 'soup'
    TYPE_DESSERT = 'dessert'
    TYPE_DRINK = 'drink'

    TYPES = [TYPE_SALAD, TYPE_FIRST_COURSE, TYPE_SECOND_COURSE, TYPE_SOUP, TYPE_DESSERT, TYPE_DRINK]

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    description = db.Column(db.String(3000), nullable=False)
    created = db.Column(db.DateTime, nullable=False, index=True, default=datetime.utcnow)
    status = db.Column(db.String(30), nullable=False, default=STATUS_ACTIVE)
    type = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, **kw):
        super().__init__(**kw)
        self._recipe_steps = []

    @property
    def recipe_steps(self):
        return self._recipe_steps

    @recipe_steps.setter
    def recipe_steps(self, recipe_steps):
        self._recipe_steps.append(recipe_steps)

    def add_recipe_step(self, recipe_step):
        self._recipe_steps.append(recipe_step)

    def add_user(self, user):
        self.user_id = user.id


class RecipeStep(db.Model):
    __tablename__ = "recipe_steps"

    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(3000), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'))


class Image(db.Model):
    __tablename__ = "images"

    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(200), nullable=False)
