from flask import Blueprint, jsonify, request
from marshmallow import ValidationError

from application.blueprints.mechanics.schemas import mechanic_schema, mechanics_schema
from application.extensions import db
from application.models import Mechanic


mechanics_bp = Blueprint("mechanics", __name__)


@mechanics_bp.route("", methods=["POST"])
def create_mechanic():
    try:
        mechanic_data = mechanic_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    new_mechanic = Mechanic(**mechanic_data)
    db.session.add(new_mechanic)
    db.session.commit()

    return mechanic_schema.jsonify(new_mechanic), 201


@mechanics_bp.route("", methods=["GET"])
def get_mechanics():
    mechanics = db.session.query(Mechanic).all()
    return mechanics_schema.jsonify(mechanics), 200


@mechanics_bp.route("/<int:mechanic_id>", methods=["PUT"])
def update_mechanic(mechanic_id):
    mechanic = db.session.get(Mechanic, mechanic_id)

    if not mechanic:
        return jsonify({"error": "Mechanic not found."}), 404

    try:
        mechanic_data = mechanic_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    for key, value in mechanic_data.items():
        setattr(mechanic, key, value)

    db.session.commit()

    return mechanic_schema.jsonify(mechanic), 200


@mechanics_bp.route("/<int:mechanic_id>", methods=["DELETE"])
def delete_mechanic(mechanic_id):
    mechanic = db.session.get(Mechanic, mechanic_id)

    if not mechanic:
        return jsonify({"error": "Mechanic not found."}), 404

    db.session.delete(mechanic)
    db.session.commit()

    return jsonify({"message": f"Mechanic id {mechanic_id} successfully deleted."}), 200
from flask import Blueprint, jsonify, request
from marshmallow import ValidationError

from application.blueprints.mechanics.schemas import mechanic_schema, mechanics_schema
from application.extensions import db
from application.models import Mechanic


mechanics_bp = Blueprint("mechanics", __name__)


@mechanics_bp.route("", methods=["POST"])
def create_mechanic():
    try:
        mechanic_data = mechanic_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    new_mechanic = Mechanic(**mechanic_data)
    db.session.add(new_mechanic)
    db.session.commit()

    return mechanic_schema.jsonify(new_mechanic), 201


@mechanics_bp.route("", methods=["GET"])
def get_mechanics():
    mechanics = db.session.query(Mechanic).all()
    return mechanics_schema.jsonify(mechanics), 200


@mechanics_bp.route("/<int:mechanic_id>", methods=["PUT"])
def update_mechanic(mechanic_id):
    mechanic = db.session.get(Mechanic, mechanic_id)

    if not mechanic:
        return jsonify({"error": "Mechanic not found."}), 404

    try:
        mechanic_data = mechanic_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    for key, value in mechanic_data.items():
        setattr(mechanic, key, value)

    db.session.commit()

    return mechanic_schema.jsonify(mechanic), 200


@mechanics_bp.route("/<int:mechanic_id>", methods=["DELETE"])
def delete_mechanic(mechanic_id):
    mechanic = db.session.get(Mechanic, mechanic_id)

    if not mechanic:
        return jsonify({"error": "Mechanic not found."}), 404

    db.session.delete(mechanic)
    db.session.commit()

    return jsonify({"message": f"Mechanic id {mechanic_id} successfully deleted."}), 200