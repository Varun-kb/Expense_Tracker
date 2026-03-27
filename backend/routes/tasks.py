# routes/tasks.py
# Handles all task operations: create, read, update, delete

from flask import Blueprint, request, jsonify
import datetime
import uuid
from config import tasks_col
from .helpers import token_required   # our helper to check login

tasks_bp = Blueprint("tasks", __name__)


# ─────────────────────────────────────────────
# GET ALL TASKS  →  GET /api/tasks
# ─────────────────────────────────────────────
@tasks_bp.route("/", methods=["GET"])
@token_required   # user must be logged in
def get_tasks(current_user):
    # Only return tasks belonging to the logged-in user
    tasks = list(tasks_col.find(
        {"user_id": current_user["user_id"]},
        {"_id": 0}   # don't send the internal MongoDB _id
    ))
    return jsonify(tasks), 200


# ─────────────────────────────────────────────
# CREATE TASK  →  POST /api/tasks
# ─────────────────────────────────────────────
@tasks_bp.route("/", methods=["POST"])
@token_required
def create_task(current_user):
    data = request.get_json()

    title = data.get("title", "").strip()
    if not title:
        return jsonify({"error": "Task title is required"}), 400

    task = {
        "_id":      str(uuid.uuid4()),
        "id":       str(uuid.uuid4()),           # frontend-friendly id
        "user_id":  current_user["user_id"],     # link task to this user
        "title":    title,
        "desc":     data.get("desc", ""),
        "priority": data.get("priority", "medium"),  # low / medium / high
        "status":   data.get("status", "pending"),   # pending / in-progress / done
        "due":      data.get("due", ""),
        "created":  datetime.datetime.utcnow().isoformat()[:10]   # YYYY-MM-DD
    }
    tasks_col.insert_one(task)

    # Return the task without MongoDB's internal _id
    task.pop("_id", None)
    return jsonify({"message": "Task created!", "task": task}), 201


# ─────────────────────────────────────────────
# UPDATE TASK  →  PUT /api/tasks/<task_id>
# ─────────────────────────────────────────────
@tasks_bp.route("/<task_id>", methods=["PUT"])
@token_required
def update_task(current_user, task_id):
    data = request.get_json()

    # Find the task and make sure it belongs to this user
    task = tasks_col.find_one({"id": task_id, "user_id": current_user["user_id"]})
    if not task:
        return jsonify({"error": "Task not found"}), 404

    # Only update fields that were sent
    update_fields = {}
    for field in ["title", "desc", "priority", "status", "due"]:
        if field in data:
            update_fields[field] = data[field]

    tasks_col.update_one({"id": task_id}, {"$set": update_fields})
    return jsonify({"message": "Task updated!"}), 200


# ─────────────────────────────────────────────
# DELETE TASK  →  DELETE /api/tasks/<task_id>
# ─────────────────────────────────────────────
@tasks_bp.route("/<task_id>", methods=["DELETE"])
@token_required
def delete_task(current_user, task_id):
    result = tasks_col.delete_one({"id": task_id, "user_id": current_user["user_id"]})
    if result.deleted_count == 0:
        return jsonify({"error": "Task not found"}), 404
    return jsonify({"message": "Task deleted!"}), 200
