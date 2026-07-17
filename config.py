import os
from dotenv import load_dotenv

load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))
_database_url = os.environ.get('DATABASE_URL')


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-prod')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    if _database_url:
        SQLALCHEMY_DATABASE_URI = _database_url.replace('postgres://', 'postgresql://')
        if 'sqlite' in _database_url:
            SQLALCHEMY_ENGINE_OPTIONS = {
                'connect_args': {'check_same_thread': False},
            }
        else:
            SQLALCHEMY_ENGINE_OPTIONS = {
                'pool_size': 5,
                'pool_recycle': 300,
                'pool_pre_ping': True,
            }
    else:
        SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'instance', 'app.db')
        SQLALCHEMY_ENGINE_OPTIONS = {
            'connect_args': {'check_same_thread': False},
        }


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


config = {
    'development': Config,
    'production': Config,
    'testing': TestingConfig,
    'default': Config,
}
