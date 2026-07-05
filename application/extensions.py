from flask_marshmallow import Marshmallow
from flask_caching import Cache
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
ma = Marshmallow()
cache = Cache(config={"CACHE_TYPE": "SimpleCache"})
limiter = Limiter(key_func=get_remote_address, storage_uri="memory://")
