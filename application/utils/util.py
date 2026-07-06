from datetime import datetime, timedelta, timezone
from functools import wraps
import os

from flask import jsonify, request
from jose import jwt
from jose.exceptions import ExpiredSignatureError, JWTError


SECRET_KEY = os.environ.get("SECRET_KEY") or "super secret secrets"
ALGORITHM = "HS256"


def encode_token(customer_id):
    payload = {
        "exp": datetime.now(timezone.utc) + timedelta(hours=1),
        "iat": datetime.now(timezone.utc),
        "sub": str(customer_id),
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token


def decode_token(token):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return int(payload["sub"])


def token_required(route_function):
    @wraps(route_function)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")

        if not auth_header.startswith("Bearer "):
            return jsonify({"error": "Authorization header must be Bearer token."}), 401

        token = auth_header.split(" ", 1)[1].strip()
        if not token:
            return jsonify({"error": "Missing token."}), 401

        try:
            customer_id = decode_token(token)
        except ExpiredSignatureError:
            return jsonify({"error": "Token has expired."}), 401
        except JWTError:
            return jsonify({"error": "Invalid token."}), 401

        return route_function(*args, auth_customer_id=customer_id, **kwargs)

    return wrapper