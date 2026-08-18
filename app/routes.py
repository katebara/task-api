"""Routes for the Task Manager API.

Endpoints:
    GET    /tasks          -> list all tasks
    POST   /tasks          -> create a task
    GET    /tasks/<id>     -> get one task
    PUT    /tasks/<id>     -> update a task
    DELETE /tasks/<id>     -> delete a task
    GET    /health         -> health check
"""

from flask import Blueprint, current_app, jsonify, request

bp = Blueprint("tasks", __name__)


@bp.get("/health")
def health():
    return jsonify({"status": "ok"}), 200


@bp.get("/tasks")
def list_tasks():
    tasks = current_app.config["TASKS"]
    return jsonify(list(tasks.values())), 200


@bp.post("/tasks")
def create_task():
    data = request.get_json(silent=True) or {}
    title = data.get("title")

    if not title or not isinstance(title, str):
        return jsonify({"error": "title is required and must be a string"}), 400

    task_id = current_app.config["NEXT_ID"]
    task = {
        "id": task_id,
        "title": title,
        "done": bool(data.get("done", False)),
    }
    current_app.config["TASKS"][task_id] = task
    current_app.config["NEXT_ID"] += 1

    return jsonify(task), 201


@bp.get("/tasks/<int:task_id>")
def get_task(task_id):
    task = current_app.config["TASKS"].get(task_id)
    if task is None:
        return jsonify({"error": "task not found"}), 404
    return jsonify(task), 200


@bp.put("/tasks/<int:task_id>")
def update_task(task_id):
    tasks = current_app.config["TASKS"]
    task = tasks.get(task_id)
    if task is None:
        return jsonify({"error": "task not found"}), 404

    data = request.get_json(silent=True) or {}
    if "title" in data:
        if not isinstance(data["title"], str) or not data["title"]:
            return jsonify({"error": "title must be a non-empty string"}), 400
        task["title"] = data["title"]
    if "done" in data:
        task["done"] = bool(data["done"])

    return jsonify(task), 200


@bp.delete("/tasks/<int:task_id>")
def delete_task(task_id):
    tasks = current_app.config["TASKS"]
    if task_id not in tasks:
        return jsonify({"error": "task not found"}), 404
    del tasks[task_id]
    return "", 204
