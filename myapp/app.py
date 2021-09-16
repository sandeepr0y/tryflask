import uuid
import jwt
from datetime import datetime, timedelta
from functools import wraps
from flask import Blueprint, jsonify, request, make_response, g
from werkzeug.security import generate_password_hash, check_password_hash

from MyApplication import MyApplication
from .models import User, UserSchema


app = MyApplication.get_app()
db = MyApplication.get_db()
bp = Blueprint('myapp', __name__, static_folder='static', template_folder='templates')


# decorator for verifying the JWT
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # jwt is passed in the request header
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        # return 401 if token is not passed
        if not token:
            return jsonify({'message': 'Token is missing !!'}), 401

        try:
            # decoding the payload to fetch the stored details
            data = jwt.decode(token, app.config['SECRET_KEY'], 'HS256')
            g.me = User.query \
                .filter_by(public_id=data['public_id']) \
                .first()
        except:
            return jsonify({
                'message': 'Token is invalid !!'
            }), 401
        # returns the current logged in users contex to the routes
        return f(*args, **kwargs)

    return decorated


@bp.route('/', methods=['GET'])
def index():
    return jsonify({'message': 'Hurray! api server is running'})


@bp.route('/login', methods=['POST'])
def login():
    data = request.json

    if data is None:
        return make_response('Could not verify', 401)

    email = data.get('email')
    password = data.get('password')

    if email is None or password is None:
        return make_response('Could not verify', 401)

    user = User.query.filter_by(email=email).first()
    if not user:
        return make_response('Could not verify', 401)
    elif check_password_hash(user.password, password):
        token = jwt.encode({
            'public_id': user.public_id,
            'exp': datetime.utcnow() + timedelta(minutes=30)
        }, app.config['SECRET_KEY'])
        return jsonify({
            'token': token
        }), 201
    else:
        return make_response('Could not verify', 403)


@bp.route('/me', methods=['GET'])
@token_required
def me():
    users_schema = UserSchema()
    return users_schema.jsonify(g.me)


@bp.route('/users', methods=['GET'])
@token_required
def get_all_users():
    # print(repr(models.User.__table__))
    all_users = User.query.all()
    users_schema = UserSchema(many=True)
    return users_schema.jsonify(all_users)


@bp.route('/users', methods=['POST'])
def create_users():
    data = request.json

    email = data.get('email')
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    password = data.get('password')

    # checking for existing user
    user = User.query.filter_by(email=email).first()
    if not user:
        # database ORM object
        user = User(
            public_id=str(uuid.uuid4()),
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=generate_password_hash(password)
        )
        # insert user
        db.session.add(user)
        db.session.commit()
        return make_response('Successfully registered.', 201)
    else:
        # returns 202 if user already exists
        return make_response('User already exists. Please Log in.', 202)


def initialize():
    pass
