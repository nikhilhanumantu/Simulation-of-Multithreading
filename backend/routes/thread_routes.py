"""
Flask REST API Routes for Thread Management.
"""
from flask import Blueprint, jsonify, request
from backend.engine.thread_manager import thread_manager_instance

thread_bp = Blueprint("threads", __name__, url_prefix="/api/threads")


@thread_bp.route("", methods=["GET"])
def get_threads():
    threads = thread_manager_instance.get_all()
    stats = thread_manager_instance.get_stats()
    return jsonify({
        "success": True,
        "count": len(threads),
        "threads": [t.to_dict() for t in threads],
        "stats": stats
    })


@thread_bp.route("", methods=["POST"])
def create_thread():
    data = request.get_json() or {}
    try:
        t = thread_manager_instance.create(data)
        return jsonify({
            "success": True,
            "message": f"Thread {t.id} created successfully",
            "thread": t.to_dict()
        }), 201
    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 400


@thread_bp.route("/<thread_id>", methods=["GET"])
def get_single_thread(thread_id):
    t = thread_manager_instance.get_by_id(thread_id.strip().upper())
    if not t:
        return jsonify({"success": False, "error": f"Thread {thread_id} not found"}), 404
    return jsonify({"success": True, "thread": t.to_dict()})


@thread_bp.route("/<thread_id>", methods=["PUT"])
def update_thread(thread_id):
    data = request.get_json() or {}
    try:
        t = thread_manager_instance.update(thread_id.strip().upper(), data)
        return jsonify({
            "success": True,
            "message": f"Thread {thread_id} updated successfully",
            "thread": t.to_dict()
        })
    except KeyError as e:
        return jsonify({"success": False, "error": str(e)}), 404
    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 400


@thread_bp.route("/<thread_id>", methods=["DELETE"])
def delete_thread(thread_id):
    deleted = thread_manager_instance.delete(thread_id.strip().upper())
    if not deleted:
        return jsonify({"success": False, "error": f"Thread {thread_id} not found"}), 404
    return jsonify({"success": True, "message": f"Thread {thread_id} deleted successfully"})


@thread_bp.route("/clear", methods=["POST"])
def clear_threads():
    thread_manager_instance.clear()
    return jsonify({"success": True, "message": "All threads cleared"})


@thread_bp.route("/preset", methods=["POST"])
def load_preset():
    thread_manager_instance.load_preset()
    threads = thread_manager_instance.get_all()
    return jsonify({
        "success": True,
        "message": "Default preset loaded",
        "threads": [t.to_dict() for t in threads],
        "stats": thread_manager_instance.get_stats()
    })


@thread_bp.route("/stats", methods=["GET"])
def get_stats():
    return jsonify({"success": True, "stats": thread_manager_instance.get_stats()})

