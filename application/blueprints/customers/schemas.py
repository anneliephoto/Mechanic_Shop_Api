from application.extensions import ma
from application.models import Customer
from marshmallow import fields


class CustomerSchema(ma.SQLAlchemyAutoSchema):
    password = fields.String(required=True, load_only=True)

    class Meta:
        model = Customer
        load_instance = False

class LoginSchema(ma.Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True)


login_schema = LoginSchema()

customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)
