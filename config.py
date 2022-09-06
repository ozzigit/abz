import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    CSRF_ENABLED = True
    WTF_CSRF_SECRET_KEY = '1234567890'
    SECRET_KEY = '0987654321'
    SQLALCHEMY_DATABASE_URI = "postgresql://abz_user:abz_pass@localhost:5432/abz_db"


class ProductionConfig(Config):
    DEBUG = False


class DevelopConfig(Config):
    DEBUG = True
    ASSETS_DEBUG = True
