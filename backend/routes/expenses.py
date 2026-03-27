# routes/expenses.py
# Handles all expense operations: create, read, update, delete

from flask import Blueprint, request, jsonify
import datetime
import uuid
from config import expenses_col
from .helpers import token_required

expenses_bp = Blueprint("expenses", __name__)


# ─────────────────────────────────────────────
# GET ALL EXPENSES  →  GET /api/expenses
# ─────────────────────────────────────────────
@expenses_bp.route("/", methods=["GET"])
@token_required
def get_expenses(current_user):

    expenses = list(
        expenses_col.find(
            {"user_id": current_user["user_id"]},
            {"_id": 0}
        )
    )

    return jsonify(expenses), 200


# ─────────────────────────────────────────────
# CREATE EXPENSE  →  POST /api/expenses
# ─────────────────────────────────────────────
@expenses_bp.route("/", methods=["POST"])
@token_required
def create_expense(current_user):

    data = request.get_json(silent=True) or {}

    # Accept both desc and description
    desc = data.get("description") or data.get("desc", "")
    desc = desc.strip()

    amount = data.get("amount", 0)

    if not desc:
        return jsonify({"error": "Description is required"}), 400

    if not amount or float(amount) <= 0:
        return jsonify({"error": "Valid amount is required"}), 400


    expense_id = str(uuid.uuid4())

    expense = {
        "_id": expense_id,
        "id": expense_id,
        "user_id": current_user["user_id"],
        "desc": desc,
        "amount": float(amount),
        "category": data.get("category", "Other"),
        "date": data.get(
            "date",
            datetime.datetime.utcnow().isoformat()[:10]
        ),
        "created": datetime.datetime.utcnow().isoformat()[:10]
    }

    expenses_col.insert_one(expense)

    expense.pop("_id", None)

    return jsonify({
        "message": "Expense added!",
        "expense": expense
    }), 201


# ─────────────────────────────────────────────
# UPDATE EXPENSE  →  PUT /api/expenses/<expense_id>
# ─────────────────────────────────────────────
@expenses_bp.route("/<expense_id>", methods=["PUT"])
@token_required
def update_expense(current_user, expense_id):

    data = request.get_json(silent=True) or {}

    expense = expenses_col.find_one(
        {"id": expense_id, "user_id": current_user["user_id"]}
    )

    if not expense:
        return jsonify({"error": "Expense not found"}), 404


    update_fields = {}

    if "description" in data:
        update_fields["desc"] = data["description"]

    if "desc" in data:
        update_fields["desc"] = data["desc"]

    if "amount" in data:
        update_fields["amount"] = float(data["amount"])

    if "category" in data:
        update_fields["category"] = data["category"]

    if "date" in data:
        update_fields["date"] = data["date"]


    expenses_col.update_one(
        {"id": expense_id},
        {"$set": update_fields}
    )

    return jsonify({"message": "Expense updated!"}), 200


# ─────────────────────────────────────────────
# DELETE EXPENSE  →  DELETE /api/expenses/<expense_id>
# ─────────────────────────────────────────────
@expenses_bp.route("/<expense_id>", methods=["DELETE"])
@token_required
def delete_expense(current_user, expense_id):

    result = expenses_col.delete_one(
        {"id": expense_id, "user_id": current_user["user_id"]}
    )

    if result.deleted_count == 0:
        return jsonify({"error": "Expense not found"}), 404

    return jsonify({"message": "Expense deleted!"}), 200