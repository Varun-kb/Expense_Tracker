from functools import wraps

import jwt
from flask import jsonify, request

from config import SECRET_KEY, users_col


def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")
        token = ""

        if auth_header.startswith("Bearer "):
            token = auth_header.split(" ", 1)[1].strip()
        else:
            token = auth_header.strip()

        if not token:
            return jsonify({"error": "Token is missing"}), 401

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token has expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401

        user = users_col.find_one(
            {"_id": payload.get("user_id")},
            {"_id": 1, "name": 1, "email": 1},
        )
        if not user:
            return jsonify({"error": "User not found"}), 401

        current_user = {
            "user_id": user["_id"],
            "name": user.get("name"),
            "email": user.get("email"),
        }

        return func(current_user, *args, **kwargs)

    return decorated
