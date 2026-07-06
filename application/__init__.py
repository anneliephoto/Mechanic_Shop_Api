from flask import Flask, jsonify, redirect
from flask_swagger_ui import get_swaggerui_blueprint

from application.extensions import cache, db, limiter, ma
from config import Config, ProductionConfig


CONFIG_MAP = {
    "Config": Config,
    "ProductionConfig": ProductionConfig,
}


def create_app(config_name_or_overrides=None):
    app = Flask(__name__)
    app.config.from_object(Config)

    if isinstance(config_name_or_overrides, str):
        config_class = CONFIG_MAP.get(config_name_or_overrides, Config)
        app.config.from_object(config_class)
    elif isinstance(config_name_or_overrides, dict):
        app.config.update(config_name_or_overrides)

    SWAGGER_URL = "/api/docs"
    API_URL = "/static/swagger.yaml"
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={"app_name": "Mechanic Shop API"},
    )

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
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

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
        return redirect("/api/docs")

    with app.app_context():
        db.create_all()


    return app
