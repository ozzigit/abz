import datetime
import os
from app import app, db
from random import randint, choice, randrange
from faker import Faker
from app.models import Employee


class Commands:

    @classmethod
    def add_employees_in_bd(cls, model):
        """ Adds workers with random names to the database
        """
        list_of_random_photo = os.listdir('app/static/images/personal')
        workers_in_previous_hierarchy = set()
        list_workers = [2, 15, 700, 2100, 8500, 40000]

        for hierarchy in range(len(list_workers)):
            all_workers_before_update = set(db.session.query(model).all())
            for i in range(list_workers[hierarchy]):
                new_employee = model(**cls.__random_dict_employee(workers_in_previous_hierarchy, list_of_random_photo))
                db.session.add(new_employee)
            db.session.commit()

            all_workers = set(db.session.query(model).all())
            workers_in_previous_hierarchy = all_workers - all_workers_before_update

    @staticmethod
    def __random_dict_employee(chief_model_set, list_of_random_photo):
        """ Returns a dictionary with random values to fill in the Employee model. """
        faker = Faker('ru_RU')
        random_photo = choice(list_of_random_photo)
        random_date = str(datetime.date(randrange(1970, 2010), randrange(1, 13), randrange(1, 29)))

        obj = {
            'name': faker.name(),
            'work_position': faker.job(),
            'date_join': random_date,
            'wage': randint(10000, 60000),
            'photo_url': random_photo,
        }
        if len(chief_model_set):
            obj['chief'] = choice(list(chief_model_set))
            obj['chief_name'] = obj['chief'].name

        return obj

    @classmethod
    def clear_db(cls, model):
        db.session.query(model).delete()
        db.session.commit()


@app.cli.command("init_db_employers")
def init_db_employers():
    """set random values in employee table"""
    Commands.clear_db(Employee)
    Commands.add_employees_in_bd(Employee)


@app.cli.command("clear_employers")
def clear_employers():
    """clear employee table in db"""
    Commands.clear_db(Employee)
