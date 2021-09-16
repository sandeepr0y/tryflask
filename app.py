from flask import Blueprint

from MyApplication import MyApplication
import myapp
import integrations


app = MyApplication.create_app()
api = Blueprint('api', __name__, static_folder='static', template_folder='templates')


def initialize():
    myapp.initialize()
    api.register_blueprint(myapp.bp, url_prefix='/')

    integrations.initialize()
    api.register_blueprint(integrations.bp, url_prefix='/integrations')

    app.register_blueprint(api, url_prefix='/api')


if __name__ == '__main__':
    initialize()
    app.run()
