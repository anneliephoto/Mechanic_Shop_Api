from flask import Flask

from application.extensions import db, ma
from config import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    ma.init_app(app)

    from application.blueprints.customers import customers_bp
    from application.blueprints.mechanics.routes import mechanics_bp
    from application.blueprints.service_tickets import service_tickets_bp

    app.register_blueprint(customers_bp, url_prefix="/customers")
    app.register_blueprint(mechanics_bp, url_prefix="/mechanics")
    app.register_blueprint(service_tickets_bp, url_prefix="/service_tickets")

    @app.route("/")
    def home():
        return "Mechanic Shop API is working!"

    with app.app_context():
        db.create_all()


    return app
