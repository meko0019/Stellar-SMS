import os
import logging 

from celery import Celery
import flask

from client.database import db



celery = Celery(
    __name__, broker=os.environ.get("REDIS_URL"), backend=os.environ.get("REDIS_URL")
)

def create_app(settings=None):
    """Application factory with optional overridable settings.
    """
    if settings is None: 
        settings = {}

    app = flask.Flask(__name__)

    if settings.get("DEBUG", False) or os.environ.get("DEBUG", False):
        app.config.from_object("config.DevelopmentConfig")
    else: 
        app.config.from_object("config.ProductionConfig")

    app.config.from_mapping(settings)

    celery.conf.update(app.config)

    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask

    # Initialize the database with the application.
    db.init_app(app)

    gunicorn_logger = logging.getLogger("gunicorn.error")
    root_logger = logging.getLogger("")
    root_logger.handlers = gunicorn_logger.handlers
    root_logger.setLevel(gunicorn_logger.level)

    if app.config.get("DEBUG"):
        db_logger = logging.getLogger("sqlalchemy.engine")
        db_logger.setLevel(logging.INFO)

        c_logger = logging.getLogger("client")
        c_logger.setLevel(logging.DEBUG)

    from client import index_blueprint
    from client.api.views import api_blueprint
    from client.api.views.users import users_blueprint
    from client.api.views.messages import msgs_blueprint

    app.register_blueprint(users_blueprint)
    app.register_blueprint(index_blueprint)
    app.register_blueprint(api_blueprint)
    app.register_blueprint(msgs_blueprint)

    from client.transactions import tasks 

    return app
