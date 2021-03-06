import os


DATABASE_URL = os.environ.get(
    "DATABASE_URL", "postgresql://postgres@localhost:5432/stellar"
)
REDIS_URL = os.environ.get("REDIS_URL", "redis://localhost:6379/0")
AMQP_URL = os.environ.get("AMQP_URL", "amqp://localhost:5672")


class BaseConfig(object):
    HOST = "127.0.0.1"
    PORT = 8000

    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    CELERY_BACKEND_URL = REDIS_URL
    CELERY_BROKER_URL = REDIS_URL


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    CELERY_TASK_ALWAYS_EAGER = True

    SECRET_KEY = "not-a-secret-key"


class ProductionConfig(BaseConfig):
    DEBUG = False
    TESTING = False

    SECRET_KEY = os.environ.get("SECRET_KEY", "not-a-secret-key")

    SESSION_COOKIE_SECURE = True
