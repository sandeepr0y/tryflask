from MyApplication import MyApplication


db = MyApplication.get_db()
ma = MyApplication.get_ma()


class User(db.Model):

    __tablename__ = 'auth_user'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    public_id = db.Column(db.String(50), nullable=False, unique=True)
    first_name = db.Column(db.String(150), nullable=False)
    last_name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(128), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    last_login = db.Column(db.DateTime())

    def __repr__(self):
        return 'User(public_id={})'.format(self.public_id)


class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User
    public_id = ma.auto_field()
    first_name = ma.auto_field()
    last_name = ma.auto_field()
    email = ma.auto_field()
