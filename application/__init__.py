from flask import Flask, jsonify

from application.extensions import cache, db, limiter, ma
from config import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    ma.init_app(app)
    cache.init_app(app)
    limiter.init_app(app)

    from application.blueprints.customers import customers_bp
    from application.blueprints.inventory import inventory_bp
    from application.blueprints.mechanics.routes import mechanics_bp
    from application.blueprints.service_tickets import service_tickets_bp

    app.register_blueprint(customers_bp, url_prefix="/customers")
    app.register_blueprint(inventory_bp, url_prefix="/inventory")
    app.register_blueprint(mechanics_bp, url_prefix="/mechanics")
    app.register_blueprint(service_tickets_bp, url_prefix="/service_tickets")

    @app.errorhandler(429)
    def handle_rate_limit(error):
        return (
            jsonify(
                {
                    "error": "Rate limit exceeded.",
                    "message": getattr(error, "description", "Too many requests."),
                }
            ),
            429,
        )

    @app.route("/")
    def home():
        return "Mechanic Shop API is working!"

    with app.app_context():
        db.create_all()


    return app
