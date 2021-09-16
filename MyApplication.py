import yaml
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow


class MyApplication(object):

    app = None
    db = None
    ma = None

    @classmethod
    def get_db(cls):
        if cls.db is None:
            cls.db = SQLAlchemy()
        return cls.db

    @classmethod
    def get_ma(cls):
        if cls.ma is None:
            cls.ma = Marshmallow()
        return cls.ma

    @classmethod
    def create_app(cls):
        if cls.app is None:
            app = Flask(__name__)
            app.config.from_file('config.yaml', load=yaml.safe_load)

            cls.get_db().init_app(app)
            cls.get_ma().init_app(app)

            cls.app = app

        return cls.app

    @classmethod
    def get_app(cls):
        return cls.create_app()
