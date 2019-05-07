import os

DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://user:password@postgres:5432/stellar")

class BaseConfig(object):
    HOST = "127.0.0.1"
    PORT = 8080

    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    TESTING = True

    SECRET_KEY = "not-a-secret-key"


class ProductionConfig(BaseConfig):
    DEBUG = False
    TESTING = False

    SECRET_KEY = os.environ.get("SECRET_KEY", None)

    SESSION_COOKIE_SECURE = True
