import uuid
from flask import Flask, jsonify
from flask_smorest import Api, Blueprint, abort
from flask.views import MethodView
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import (JWTManager, create_access_token, jwt_required, get_jwt_identity)

from db import db, migrate
from models import User, Category, Record, Currency
from schemas import (
    UserSchema, CategorySchema, RecordSchema, 
    CurrencySchema, RecordQuerySchema, UserLoginSchema
)

blp = Blueprint("api", "api", url_prefix="/")

@blp.route("/register")
class UserRegister(MethodView):
    @blp.arguments(UserSchema)
    @blp.response(201, UserSchema)
    def post(self, user_data):
        if User.query.filter_by(name=user_data['name']).first():
            abort(409, message="A user with that name already exists")
            
        if 'default_currency_id' in user_data:
             if not Currency.query.get(user_data['default_currency_id']):
                 abort(404, message="Currency not found")

        user = User(
            id=str(uuid.uuid4()),
            name=user_data['name'],
            password=pbkdf2_sha256.hash(user_data['password']),
            default_currency_id=user_data.get('default_currency_id')
        )
        db.session.add(user)
        db.session.commit()
        return user

@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(UserLoginSchema)
    def post(self, user_data):
        user = User.query.filter_by(name=user_data['name']).first()

        if user and pbkdf2_sha256.verify(user_data['password'], user.password):
            access_token = create_access_token(identity=user.id)
            return {"access_token": access_token}

        abort(401, message="Invalid credentials")

@blp.route("/users")
class UserList(MethodView):
    @jwt_required()
    @blp.response(200, UserSchema(many=True))
    def get(self):
        return User.query.all()

@blp.route("/user/<user_id>")
class UserResource(MethodView):
    @jwt_required()
    @blp.response(200, UserSchema)
    def get(self, user_id):
        return User.query.get_or_404(user_id)

    @jwt_required()
    def delete(self, user_id):
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {"message": "User deleted"}

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

@blp.route("/category")
class CategoryList(MethodView):
    @jwt_required()
    @blp.response(200, CategorySchema(many=True))
    def get(self):
        return Category.query.all()

    @jwt_required()
    @blp.arguments(CategorySchema)
    @blp.response(201, CategorySchema)
    def post(self, cat_data):
        category = Category(id=str(uuid.uuid4()), name=cat_data['name'])
        db.session.add(category)
        db.session.commit()
        return category

@blp.route("/category/<category_id>")
class CategoryResource(MethodView):
    @jwt_required()
    def delete(self, category_id):
        cat = Category.query.get_or_404(category_id)
        db.session.delete(cat)
        db.session.commit()
        return {"message": "Category deleted"}

@blp.route("/record")
class RecordList(MethodView):
    @jwt_required()
    @blp.arguments(RecordQuerySchema, location="query")
    @blp.response(200, RecordSchema(many=True))
    def get(self, args):
        query = Record.query

        if args.get('user_id'):
            query = query.filter_by(user_id=args['user_id'])
        if args.get('category_id'):
            query = query.filter_by(category_id=args['category_id'])
        
        return query.all()

    @jwt_required()
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
    @jwt_required()
    @blp.response(200, RecordSchema)
    def get(self, record_id):
        return Record.query.get_or_404(record_id)

    @jwt_required()
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
    
    jwt = JWTManager(app)

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({"message": "The token has expired.", "error": "token_expired"}), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({"message": "Signature verification failed.", "error": "invalid_token"}), 401

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return jsonify({
            "description": "Request does not contain an access token.",
            "error": "authorization_required"
        }), 401

    api = Api(app)
    api.register_blueprint(blp)
    
    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True, port=5000)