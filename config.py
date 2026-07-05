class Config:
    SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://root:theBoot26$$$@localhost/mechanic_shop"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CACHE_TYPE = "SimpleCache"
    CACHE_DEFAULT_TIMEOUT = 60
