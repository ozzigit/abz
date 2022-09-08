from app import db
from sqlalchemy import Identity
from datetime import datetime


class Employee(db.Model):
    __tablename__ = 'employee'

    id = db.Column(db.Integer, Identity(start=1), nullable=False, unique=True, primary_key=True, autoincrement=True)
    name = db.Column(db.String(), nullable=False)
    work_position = db.Column(db.String(), nullable=False)
    date_join = db.Column(db.DateTime(), default=datetime.now())
    wage = db.Column(db.Float(precision=10, decimal_return_scale=2), default=0.01)
    chief = db.Column(db.ForeignKey("employee.id"), default=None)

    # def __init__(self, id, name, work_position, date_join, wage, chief):
    #     self.id = id
    #     self.name = name
    #     self.work_position = work_position
    #     self.date_join = date_join
    #     self.wage = wage
    #     self.chief = chief
    def __repr__(self):
        return '<Name {}, id {}, chief {}>'.format(self.name, self.id, self.chief)


class Users(db.Model):
    id = db.Column(db.Integer, Identity(start=1), primary_key=True, nullable=False, unique=True, autoincrement=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    # def __init__(self, id, username, email, password_hash):
    #     self.id = id
    #     self.username = username
    #     self.email = email
    #     self.password_hash = password_hash

    def __repr__(self):
        return '<User {}>'.format(self.username)
