import datetime
import logging
import sys
from logging import Formatter

import sqlalchemy
from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import Model, SQLAlchemy
from sqlalchemy.ext.declarative import declared_attr

from mystripeapp import utils


def start(override=None):
    """
    Bootstrap the application.

    :return {Flask}: Returns the configuration Flask applciation object.
    """
    env = utils.environment()

    app = Flask(
        __name__, template_folder="/mystripeapp/mystripeapp/ui", static_folder="/mystripeapp/mystripeapp/ui/static",
    )

    configuration = dict(
        {
            "SERVER_NAME": "{name}:{port}".format(name=env["app"]["name"], port=env["app"]["port"]),
            "WTF_CSRF_SECRET_KEY": env["app"]["secret"],
            "WTF_CSRF_ENABLED": True,
            "WTF_CSRF_METHODS": ["GET", "POST", "PUT", "DELETE"],
            "SQLALCHEMY_TRACK_MODIFICATIONS": False,
            "SQLALCHEMY_DATABASE_URI": "{provider}://{user}:{password}@{host}:{port}/{db}".format(
                provider=env["database"]["provider"],
                user=env["database"]["username"],
                password=env["database"]["password"],
                host=env["database"]["host"],
                port=env["database"]["port"],
                db=env["database"]["database"],
            ),
        },
        **override or {}
    )

    # Apply default configuration values...
    for configuration_value in configuration:
        app.config[configuration_value] = configuration[configuration_value]

    # Enable the login manager library...
    app.login_manager = LoginManager(app)
    app.secret_key = env["app"]["secret"]

    # Setup the logging handlers and formatters...
    handler = logging.StreamHandler(stream=sys.stdout)
    handler.setFormatter(Formatter("%(asctime)s %(levelname)s: %(message)s"))
    handler.setLevel(logging.INFO)
    app.logger.handlers = [handler]
    app.logger.setLevel(logging.INFO)

    return app


class BaseModel(Model):
    """
    The base model for all database models. This will include some common
    columns for all tables:
    """

    @declared_attr
    def id(self):
        return sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True, nullable=False)

    @declared_attr
    def created_at(self):
        return sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.utcnow, nullable=False)


app = start()
db = SQLAlchemy(app, model_class=BaseModel)
migrate = Migrate(app, db)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
