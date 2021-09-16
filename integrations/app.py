from flask import Blueprint, jsonify
from myapp import token_required
from . import sftp_inbound, models


bp = Blueprint('integrations', __name__, static_folder='static', template_folder='templates')


@bp.route('/', methods=['GET'])
def index():
    return jsonify({'message': 'not implemented'})


@bp.route('/date_formats', methods=['GET'])
@token_required
def date_formats():
    date_format_data = models.HrDateFormat.query.all()
    hr_date_formats_schema = models.HrDateFormatSchema(many=True)
    return hr_date_formats_schema.jsonify(date_format_data)


def initialize():
    sftp_inbound.initialize()
    bp.register_blueprint(sftp_inbound.bp, url_prefix='sftp_inbound')
