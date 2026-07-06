from application import create_app


# Render/Gunicorn entrypoint for production deployment.
app = create_app("ProductionConfig")
