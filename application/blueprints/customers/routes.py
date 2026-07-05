from flask import jsonify, request
from marshmallow import ValidationError

from application.blueprints.customers import customers_bp
from application.blueprints.customers.schemas import customer_schema, customers_schema, login_schema
from application.blueprints.service_tickets.schemas import service_tickets_schema
from application.extensions import db, limiter
from application.models import Customer, ServiceTicket
from application.utils.util import encode_token, token_required

@customers_bp.route("/login", methods=["POST"])
def login():
    try:
        login_data = login_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    customer = db.session.query(Customer).filter_by(email=login_data["email"]).first()

    if not customer or customer.password != login_data["password"]:
        return jsonify({"error": "Invalid email or password."}), 401

    token = encode_token(customer.id)
    return jsonify({"token": token}), 200

@customers_bp.route("", methods=["POST"])
@limiter.limit("5 per hour")
def create_customer():
    # Limit account creation attempts to reduce spam and abuse on a write endpoint.
    try:
        customer_data = customer_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    existing_customer = db.session.query(Customer).filter_by(email=customer_data["email"]).first()

    if existing_customer:
        return jsonify({"error": "Email already associated with an account."}), 400

    new_customer = Customer(**customer_data)
    db.session.add(new_customer)
    db.session.commit()

    return customer_schema.jsonify(new_customer), 201


@customers_bp.route("", methods=["GET"])
def get_customers():
    try:
        limit = int(request.args.get("limit", 10))
        offset = int(request.args.get("offset", 0))
    except ValueError:
        return jsonify({"error": "limit and offset must be integers."}), 400

    if limit < 1:
        return jsonify({"error": "limit must be greater than 0."}), 400

    if offset < 0:
        return jsonify({"error": "offset cannot be negative."}), 400

    query = db.session.query(Customer)
    total = query.count()
    customers = query.offset(offset).limit(limit).all()

    return (
        jsonify(
            {
                "data": customers_schema.dump(customers),
                "pagination": {
                    "limit": limit,
                    "offset": offset,
                    "count": len(customers),
                    "total": total,
                },
            }
        ),
        200,
    )


@customers_bp.route("/my-tickets", methods=["GET"])
@token_required
def get_my_tickets(auth_customer_id):
    tickets = db.session.query(ServiceTicket).filter_by(customer_id=auth_customer_id).all()
    return service_tickets_schema.jsonify(tickets), 200


@customers_bp.route("/<int:customer_id>", methods=["GET"])
@token_required
def get_customer(customer_id, auth_customer_id):
    if customer_id != auth_customer_id:
        return jsonify({"error": "Forbidden. You can only access your own account."}), 403

    customer = db.session.get(Customer, customer_id)

    if not customer:
        return jsonify({"error": "Customer not found."}), 404

    return customer_schema.jsonify(customer), 200


@customers_bp.route("/<int:customer_id>", methods=["PUT"])
@token_required
def update_customer(customer_id, auth_customer_id):
    if customer_id != auth_customer_id:
        return jsonify({"error": "Forbidden. You can only update your own account."}), 403

    customer = db.session.get(Customer, customer_id)

    if not customer:
        return jsonify({"error": "Customer not found."}), 404

    try:
        customer_data = customer_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    for key, value in customer_data.items():
        setattr(customer, key, value)

    db.session.commit()

    return customer_schema.jsonify(customer), 200


@customers_bp.route("/<int:customer_id>", methods=["DELETE"])
@token_required
def delete_customer(customer_id, auth_customer_id):
    if customer_id != auth_customer_id:
        return jsonify({"error": "Forbidden. You can only delete your own account."}), 403

    customer = db.session.get(Customer, customer_id)

    if not customer:
        return jsonify({"error": "Customer not found."}), 404

    db.session.delete(customer)
    db.session.commit()



    return jsonify({"message": f"Customer id {customer_id} successfully deleted."}), 200
