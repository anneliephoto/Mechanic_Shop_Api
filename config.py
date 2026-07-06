import os


class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "SQLALCHEMY_DATABASE_URI",
        "mysql+mysqlconnector://root:theBoot26$$$@localhost/mechanic_shop",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CACHE_TYPE = "SimpleCache"
    CACHE_DEFAULT_TIMEOUT = 60
    SECRET_KEY = os.environ.get("SECRET_KEY", "super secret secrets")


class ProductionConfig(Config):
    DEBUG = False
