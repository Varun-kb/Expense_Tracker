# routes/auth.py
# Handles user registration and login

from flask import Blueprint, request, jsonify
import bcrypt          # for hashing passwords safely
import jwt             # for creating login tokens
import datetime
import uuid            # for generating unique user IDs
from config import users_col, SECRET_KEY

# Create a "blueprint" - a group of related routes
auth_bp = Blueprint("auth", __name__)


# ─────────────────────────────────────────────
# REGISTER  →  POST /api/auth/register
# ─────────────────────────────────────────────
@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    # Make sure all required fields are sent
    name     = data.get("name", "").strip()
    email    = data.get("email", "").strip().lower()
    password = data.get("password", "")

    if not name or not email or not password:
        return jsonify({"error": "Name, email and password are required"}), 400

    if len(password) < 6:
        return jsonify({"error": "Password must be at least 6 characters"}), 400

    # Check if email already exists
    if users_col.find_one({"email": email}):
        return jsonify({"error": "Email already registered"}), 409

    # Hash the password before saving (never store plain text passwords!)
    hashed_pw = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    # Create the user document to save in MongoDB
    user = {
        "_id":      str(uuid.uuid4()),   # unique ID
        "name":     name,
        "email":    email,
        "password": hashed_pw.decode("utf-8"),   # store as string
        "created":  datetime.datetime.utcnow().isoformat()
    }
    users_col.insert_one(user)

    # Create a JWT token so the user is logged in immediately after registering
    token = _make_token(user["_id"], user["name"], user["email"])

    return jsonify({
        "message": "Registered successfully!",
        "token":   token,
        "user":    {"id": user["_id"], "name": name, "email": email}
    }), 201


# ─────────────────────────────────────────────
# LOGIN  →  POST /api/auth/login
# ─────────────────────────────────────────────
@auth_bp.route("/login", methods=["POST"])
def login():
    data     = request.get_json()
    email    = data.get("email", "").strip().lower()
    password = data.get("password", "")

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    # Find the user by email
    user = users_col.find_one({"email": email})
    if not user:
        return jsonify({"error": "Invalid email or password"}), 401

    # Check if the password matches the hashed one in the database
    if not bcrypt.checkpw(password.encode("utf-8"), user["password"].encode("utf-8")):
        return jsonify({"error": "Invalid email or password"}), 401

    # Create and return a JWT token
    token = _make_token(user["_id"], user["name"], user["email"])

    return jsonify({
        "message": "Login successful!",
        "token":   token,
        "user":    {"id": user["_id"], "name": user["name"], "email": user["email"]}
    }), 200


# ─────────────────────────────────────────────
# Helper: Create a JWT token
# ─────────────────────────────────────────────
def _make_token(user_id, name, email):
    payload = {
        "user_id": user_id,
        "name":    name,
        "email":   email,
        # Token expires in 7 days
        "exp":     datetime.datetime.utcnow() + datetime.timedelta(days=7)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")
