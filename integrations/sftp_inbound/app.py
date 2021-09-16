from flask import Blueprint, jsonify


bp = Blueprint('sftp_inbound', __name__, static_folder='static', template_folder='templates')


@bp.route('/', methods=['GET'])
def index():
    return jsonify({'msg': 'coming soon'})


def initialize():
    pass
