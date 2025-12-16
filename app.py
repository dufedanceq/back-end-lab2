import uuid
from flask import Flask
from flask_smorest import Api, Blueprint, abort
from flask.views import MethodView

from db import db, migrate
from models import User, Category, Record, Currency
from schemas import UserSchema, CategorySchema, RecordSchema, CurrencySchema, RecordQuerySchema

blp = Blueprint("api", "api", url_prefix="/")

@blp.route("/currency")
class CurrencyList(MethodView):
    @blp.response(200, CurrencySchema(many=True))
    def get(self):
        return Currency.query.all()

    @blp.arguments(CurrencySchema)
    @blp.response(201, CurrencySchema)
    def post(self, currency_data):
        if Currency.query.filter_by(name=currency_data['name']).first():
            abort(400, message="Currency already exists")
        currency = Currency(name=currency_data['name'])
        db.session.add(currency)
        db.session.commit()
        return currency

@blp.route("/user")
class UserList(MethodView):
    @blp.response(200, UserSchema(many=True))
    def get(self):
        return User.query.all()

    @blp.arguments(UserSchema)
    @blp.response(201, UserSchema)
    def post(self, user_data):
        if 'default_currency_id' in user_data:
            if not Currency.query.get(user_data['default_currency_id']):
                abort(404, message="Currency not found")

        user = User(
            id=str(uuid.uuid4()), 
            name=user_data['name'],
            default_currency_id=user_data.get('default_currency_id')
        )
        db.session.add(user)
        db.session.commit()
        return user

@blp.route("/user/<user_id>")
class UserResource(MethodView):
    @blp.response(200, UserSchema)
    def get(self, user_id):
        return User.query.get_or_404(user_id)

    def delete(self, user_id):
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {"message": "User deleted"}

@blp.route("/category")
class CategoryList(MethodView):
    @blp.response(200, CategorySchema(many=True))
    def get(self):
        return Category.query.all()

    @blp.arguments(CategorySchema)
    @blp.response(201, CategorySchema)
    def post(self, cat_data):
        category = Category(id=str(uuid.uuid4()), name=cat_data['name'])
        db.session.add(category)
        db.session.commit()
        return category

@blp.route("/category/<category_id>")
class CategoryResource(MethodView):
    def delete(self, category_id):
        cat = Category.query.get_or_404(category_id)
        db.session.delete(cat)
        db.session.commit()
        return {"message": "Category deleted"}

@blp.route("/record")
class RecordList(MethodView):
    @blp.arguments(RecordQuerySchema, location="query")
    @blp.response(200, RecordSchema(many=True))
    def get(self, args):
        query = Record.query
        if args.get('user_id'):
            query = query.filter_by(user_id=args['user_id'])
        if args.get('category_id'):
            query = query.filter_by(category_id=args['category_id'])
        if not args:
            abort(400, message="Filter params required")
        return query.all()

    @blp.arguments(RecordSchema)
    @blp.response(201, RecordSchema)
    def post(self, record_data):
        user = User.query.get(record_data['user_id'])
        category = Category.query.get(record_data['category_id'])
        if not user or not category:
            abort(404, message="User or Category not found")

        currency_id = record_data.get('currency_id')
        if not currency_id:
            if not user.default_currency_id:
                 abort(400, message="No currency provided and user has no default")
            currency_id = user.default_currency_id
        elif not Currency.query.get(currency_id):
            abort(404, message="Currency not found")

        record = Record(
            id=str(uuid.uuid4()),
            user_id=record_data['user_id'],
            category_id=record_data['category_id'],
            currency_id=currency_id,
            amount=record_data['amount']
        )
        db.session.add(record)
        db.session.commit()
        return record

@blp.route("/record/<record_id>")
class RecordResource(MethodView):
    @blp.response(200, RecordSchema)
    def get(self, record_id):
        return Record.query.get_or_404(record_id)

    def delete(self, record_id):
        rec = Record.query.get_or_404(record_id)
        db.session.delete(rec)
        db.session.commit()
        return {"message": "Record deleted"}

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)
    migrate.init_app(app, db)
    api = Api(app)
    api.register_blueprint(blp)
    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True, port=5000)