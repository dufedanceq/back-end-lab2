from marshmallow import Schema, fields

class CurrencySchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)

class UserSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True) 
    default_currency_id = fields.Int(required=False)

class UserLoginSchema(Schema):
    name = fields.Str(required=True)
    password = fields.Str(required=True)

class CategorySchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)

class RecordSchema(Schema):
    id = fields.Str(dump_only=True)
    user_id = fields.Str(required=True)
    category_id = fields.Str(required=True)
    currency_id = fields.Int(load_default=None)
    amount = fields.Float(required=True)
    timestamp = fields.DateTime(dump_only=True)

class RecordQuerySchema(Schema):
    user_id = fields.Str(required=False)
    category_id = fields.Str(required=False)