from app import app, db
import random
from faker import Faker
from .models import Employee


class Commands:

    @classmethod
    def add_employees_in_bd(cls, model):
        """ Adds workers with random names to the database
        """
        workers_previous_hierarchy = []
        list_workers = [1, 2, 3, 4, 5]

        for hierarchy in range(5):
            _workers_created = []
            for i in range(list_workers[hierarchy]):
                new_employee = model(**cls.__random_dict_employee(workers_previous_hierarchy))
                _workers_created.append(new_employee)
                db.session.add(new_employee)

            workers_previous_hierarchy = _workers_created

        print(workers_previous_hierarchy)

        db.session.commit()

    @staticmethod
    def __random_dict_employee(chief_model_list=None):
        """ Returns a dictionary with random values to fill in the Employee model. """
        faker = Faker('uk_UA')
        random_object = random.choice(chief_model_list) if chief_model_list is not None else chief_model_list
        return {
            'name': faker.name(),
            'work_position': faker.job(),
            'wage': random.randint(3000, 4000),
            'chief': random_object
        }

    @classmethod
    def clear_db(cls, model):
        db.session.query(model).delete()
        db.session.commit()


@app.cli.command("init_db")
def init_db():
    """set values in db"""
    Commands.add_employees_in_bd(Employee)


@app.cli.command("clear_db")
def del_tables():
    """del all tables in db"""
    Commands.clear_db(Employee)
