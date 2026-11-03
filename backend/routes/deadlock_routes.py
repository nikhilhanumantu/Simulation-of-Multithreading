"""
Flask REST API Routes for Deadlock Lab with input validation.
"""
from flask import Blueprint, jsonify, request
from backend.deadlock.resource_manager import ResourceManager
from backend.deadlock.detection import detect_deadlock
from backend.deadlock.banker_algorithm import run_bankers_algorithm
from backend.deadlock.recovery import recover_by_termination

deadlock_bp = Blueprint("deadlock", __name__, url_prefix="/api/deadlock")
_default_resource_manager = ResourceManager()


@deadlock_bp.route("/graph", methods=["GET"])
def get_graph():
    state = _default_resource_manager.get_graph_state()
    detection = detect_deadlock(_default_resource_manager.allocations, _default_resource_manager.requests)
    return jsonify({
        "success": True,
        "graph": state,
        "detection": detection
    })


@deadlock_bp.route("/detect", methods=["POST"])
def detect_deadlock_endpoint():
    data = request.get_json() or {}
    allocations = data.get("allocations", _default_resource_manager.allocations)
    requests = data.get("requests", _default_resource_manager.requests)

    try:
        result = detect_deadlock(allocations, requests)
        return jsonify({
            "success": True,
            "result": result
        })
    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 400


@deadlock_bp.route("/banker", methods=["POST"])
def run_banker():
    data = request.get_json() or {}
    # Default classic example matching textbook specifications:
    available = data.get("available", [3, 3, 2])
    max_matrix = data.get("max_matrix", [
        [7, 5, 3],
        [3, 2, 2],
        [9, 0, 2],
        [2, 2, 2],
        [4, 3, 3]
    ])
    allocation_matrix = data.get("allocation_matrix", [
        [0, 1, 0],
        [2, 0, 0],
        [3, 0, 2],
        [2, 1, 1],
        [0, 0, 2]
    ])
    process_names = data.get("process_names", ["P0", "P1", "P2", "P3", "P4"])

    try:
        result = run_bankers_algorithm(
            available=available,
            max_matrix=max_matrix,
            allocation_matrix=allocation_matrix,
            process_names=process_names
        )
        return jsonify({
            "success": True,
            "result": result
        })
    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 400


@deadlock_bp.route("/recover", methods=["POST"])
def recover_deadlock():
    data = request.get_json() or {}
    victim = data.get("victim_thread", "T2")

    result = recover_by_termination(victim_thread=victim)
    return jsonify({
        "success": True,
        "result": result
    })


@deadlock_bp.route("/reset", methods=["POST"])
def reset_graph():
    global _default_resource_manager
    _default_resource_manager = ResourceManager()
    return jsonify({
        "success": True,
        "message": "Resource Allocation Graph reset to initial circular wait state",
        "graph": _default_resource_manager.get_graph_state()
    })
