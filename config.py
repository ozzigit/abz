import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    # FLASK_DEBUG = 1
    CSRF_ENABLED = True
    WTF_CSRF_SECRET_KEY = '1234567890'
    SECRET_KEY = '0987654321'
    SQLALCHEMY_DATABASE_URI = "postgresql://abz_user:abz_pass@localhost:5432/abz_db"
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class ProductionConfig(Config):
    DEBUG = False
    # FLASK_DEBUG = 0


class DevelopConfig(Config):
    DEBUG = True
    # FLASK_DEBUG = 1
    ASSETS_DEBUG = True
