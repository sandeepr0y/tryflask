from MyApplication import MyApplication
from marshmallow import fields
from sqlalchemy.dialects.postgresql import BIT


db = MyApplication.get_db()
ma = MyApplication.get_ma()


class HrDateFormat(db.Model):
    hr_date_format_id = db.Column(db.BigInteger, primary_key=True, nullable=False)
    display_text = db.Column(db.String(64), nullable=False)
    regular_expression = db.Column(db.String(256), nullable=False)
    py_format = db.Column(db.String(64), nullable=False)
    priority = db.Column(db.Integer, nullable=False)
    is_default = db.Column(BIT(1), nullable=False)
    created_date = db.Column(db.DateTime(timezone=True), nullable=False)
    modified_date = db.Column(db.DateTime(timezone=True), nullable=False)

    __bind_key__ = 'postgres'
    __tablename__ = 'hr_date_format'
    __table_args__ = {
        # 'autoload': True,
        'schema': 'public',
        # 'autoload_with': db.get_engine(bind='postgres')
    }


class HrDateFormatSchema(ma.SQLAlchemySchema):
    class Meta:
        model = HrDateFormat
    id = fields.Integer(attribute='hr_date_format_id')
    name = fields.String(attribute='display_text')
    regex = fields.String(attribute='regular_expression')
    py_format = ma.auto_field()
    priority = ma.auto_field()
    is_default = fields.Function(lambda obj: obj.is_default == '1')
