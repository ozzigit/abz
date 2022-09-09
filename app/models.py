from app import db, login
from sqlalchemy import Identity
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


@login.user_loader
def load_user(id):
    return Users.query.get(int(id))


class Employee(db.Model):
    __tablename__ = 'employee'

    id = db.Column(db.Integer, Identity(start=1), nullable=False, unique=True, primary_key=True, autoincrement=True)
    name = db.Column(db.String(), nullable=False)
    work_position = db.Column(db.String(), nullable=False)
    date_join = db.Column(db.DateTime(), default=datetime.now())
    wage = db.Column(db.Float(precision=10, decimal_return_scale=2), default=0.01)
    chief = db.Column(db.ForeignKey("employee.id"), default=None)

    def __repr__(self):
        return '<Name {}, id {}, chief {}>'.format(self.name, self.id, self.chief)

    def to_dict(self):
        return {
            'name': self.name,
            'work_position': self.work_position,
            'date_join': self.date_join,
            'wage': self.wage,
            'chief': self.chief
        }


class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, Identity(start=1), primary_key=True, nullable=False, unique=True, autoincrement=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)
