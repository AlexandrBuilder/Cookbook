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
