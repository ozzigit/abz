from sqlalchemy.orm import relationship

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

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    work_position = db.Column(db.String(), nullable=False)
    date_join = db.Column(db.String(), default="1965-01-01")
    wage = db.Column(db.Float(precision=10, decimal_return_scale=2), default=0.01)
    chief_id = db.Column(db.Integer, db.ForeignKey("employee.id"), index=True, nullable=True)
    chief = relationship('Employee', remote_side=[id])
    chief_name = db.Column(db.String(), default="None")
    photo_url = db.Column(db.String(), default="")

    def __repr__(self):
        return '<Name {}, id {}, chief {}>'.format(self.name, self.id, self.chief)

    def to_dict(self):
        chief = db.session.query(Employee).filter(Employee.id == self.chief_id).all()
        if len(chief):
            chief = chief[0]
            chief_id = chief.id
        else:
            chief_id = "None"
        return {
            'id': self.id,
            'name': self.name,
            'work_position': self.work_position,
            'date_join': self.date_join,
            'wage': self.wage,
            'chief_id': chief_id,
            "chief_name": self.chief_name
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
