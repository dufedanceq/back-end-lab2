from sqlalchemy.sql import func
from db import db

class Currency(db.Model):
    __tablename__ = 'currency'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(3), unique=True, nullable=False)

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.String(36), primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    
    default_currency_id = db.Column(db.Integer, db.ForeignKey('currency.id'), nullable=True)
    default_currency = db.relationship('Currency')

class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.String(36), primary_key=True)
    name = db.Column(db.String(80), nullable=False)

class Record(db.Model):
    __tablename__ = 'record'
    id = db.Column(db.String(36), primary_key=True)
    user_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)
    category_id = db.Column(db.String(36), db.ForeignKey('category.id'), nullable=False)
    currency_id = db.Column(db.Integer, db.ForeignKey('currency.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, server_default=func.now())

    user = db.relationship('User')
    category = db.relationship('Category')
    currency = db.relationship('Currency')