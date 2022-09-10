import datetime
from app import app, db
from random import randint, choice, randrange
from faker import Faker
from app.models import Employee


class Commands:

    @classmethod
    def add_employees_in_bd(cls, model):
        """ Adds workers with random names to the database
        """
        # create a Boss
        boss = model(name='Boss', work_position='Boss', wage=0, chief=None)
        db.session.add(boss)
        db.session.commit()
        boss_id = db.session.query(Employee).filter(Employee.name == 'Boss').one().id
        workers_in_previous_hierarchy = set()
        workers_in_previous_hierarchy.add(boss_id)
        list_workers = [10, 30, 70, 200, 2000]

        for hierarchy in range(5):
            all_workers_before_update = set([worker[0] for worker in db.session.query(Employee.id).all()])

            for i in range(list_workers[hierarchy]):
                new_employee = model(**cls.__random_dict_employee(workers_in_previous_hierarchy))
                db.session.add(new_employee)
            db.session.commit()

            all_workers = set([worker[0] for worker in db.session.query(Employee.id).all()])
            workers_in_previous_hierarchy = all_workers - all_workers_before_update

    @staticmethod
    def __random_dict_employee(chief_model_set):
        """ Returns a dictionary with random values to fill in the Employee model. """
        faker = Faker('ru_RU')
        random_object = choice(list(chief_model_set))
        random_date = datetime.date(randrange(1970, 2005), randrange(1, 13), randrange(1, 29))
        return {'name': faker.name(),
                'work_position': faker.job(),
                'date_join': random_date,
                'wage': randint(10000, 60000),
                'chief': random_object
                }

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
