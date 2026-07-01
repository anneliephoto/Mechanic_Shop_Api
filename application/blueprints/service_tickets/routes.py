from flask import jsonify, request
from marshmallow import ValidationError

from application.blueprints.service_tickets import service_tickets_bp
from application.blueprints.service_tickets.schemas import service_ticket_schema, service_tickets_schema
from application.extensions import db
from application.models import ServiceTicket, Mechanic


@service_tickets_bp.route("", methods=["POST"])
def create_service_ticket():
    try:
        ticket_data = service_ticket_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    new_ticket = ServiceTicket(**ticket_data)
    db.session.add(new_ticket)
    db.session.commit()

    return service_ticket_schema.jsonify(new_ticket), 201


@service_tickets_bp.route("", methods=["GET"])
def get_service_tickets():
    tickets = db.session.query(ServiceTicket).all()
    return service_tickets_schema.jsonify(tickets), 200


@service_tickets_bp.route("/<int:ticket_id>/assign-mechanic/<int:mechanic_id>", methods=["PUT"])
def assign_mechanic(ticket_id, mechanic_id):
    ticket = db.session.get(ServiceTicket, ticket_id)
    mechanic = db.session.get(Mechanic, mechanic_id)

    if not ticket:
        return jsonify({"error": "Service ticket not found."}), 404

    if not mechanic:
        return jsonify({"error": "Mechanic not found."}), 404

    if mechanic in ticket.mechanics:
        return jsonify({"message": "Mechanic already assigned to this ticket."}), 200

    ticket.mechanics.append(mechanic)
    db.session.commit()

    return jsonify({"message": f"Mechanic id {mechanic_id} assigned to ticket id {ticket_id}."}), 200


@service_tickets_bp.route("/<int:ticket_id>/remove-mechanic/<int:mechanic_id>", methods=["PUT"])
def remove_mechanic(ticket_id, mechanic_id):
    ticket = db.session.get(ServiceTicket, ticket_id)
    mechanic = db.session.get(Mechanic, mechanic_id)

    if not ticket:
        return jsonify({"error": "Service ticket not found."}), 404

    if not mechanic:
        return jsonify({"error": "Mechanic not found."}), 404

    if mechanic not in ticket.mechanics:
        return jsonify({"message": "Mechanic is not assigned to this ticket."}), 200

    ticket.mechanics.remove(mechanic)
    db.session.commit()

    return jsonify({"message": f"Mechanic id {mechanic_id} removed from ticket id {ticket_id}."}), 200