from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class CarsModel(db.Model):
    __tablename__ = 'employee'

    id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    name = db.Column(db.String(), nullable=False)
    work_position = db.Column(db.String(), nullable=False)
    date_join = db.Column(db.DateTime(), default=datetime.now())
    wage = db.Column(db.Float(precision=10, decimal_return_scale=2), default=0.01)
    chief = db.Column(db.ForeignKey("employee_id"), default=None)

    def __init__(self, id, name, work_position, date_join, wage, chief):
        self.id = id
        self.name = name
        self.work_position = work_position
        self.date_join = date_join
        self.wage = wage
        self.chief = chief
