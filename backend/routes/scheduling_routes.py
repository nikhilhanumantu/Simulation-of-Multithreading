"""
Flask REST API Routes for CPU Scheduling.
"""
from flask import Blueprint, jsonify, request
from backend.engine.thread_manager import thread_manager_instance
from backend.models.thread_model import Thread
from backend.scheduling.scheduler import run_scheduler, compare_all_algorithms

scheduling_bp = Blueprint("scheduling", __name__, url_prefix="/api/scheduling")


@scheduling_bp.route("/run", methods=["POST"])
def run_simulation():
    data = request.get_json() or {}
    algorithm = data.get("algorithm", "Round Robin")
    time_quantum = int(data.get("time_quantum", 2))
    context_switch_overhead = int(data.get("context_switch_overhead", 0))

    custom_threads = data.get("threads")
    if custom_threads and isinstance(custom_threads, list):
        threads = [Thread.from_dict(t) for t in custom_threads]
    else:
        threads = thread_manager_instance.get_all()

    if not threads:
        return jsonify({"success": False, "error": "No threads available for scheduling"}), 400

    result = run_scheduler(
        algorithm=algorithm,
        threads=threads,
        time_quantum=time_quantum,
        context_switch_overhead=context_switch_overhead
    )

    return jsonify({
        "success": True,
        "algorithm": algorithm,
        "result": result.to_dict()
    })


@scheduling_bp.route("/compare", methods=["GET", "POST"])
def compare_algorithms():
    if request.method == "POST":
        data = request.get_json() or {}
    else:
        data = {
            "time_quantum": request.args.get("time_quantum", 2),
            "context_switch_overhead": request.args.get("context_switch_overhead", 0)
        }
    time_quantum = int(data.get("time_quantum", 2))
    context_switch_overhead = int(data.get("context_switch_overhead", 0))

    custom_threads = data.get("threads")
    if custom_threads and isinstance(custom_threads, list):
        threads = [Thread.from_dict(t) for t in custom_threads]
    else:
        threads = thread_manager_instance.get_all()

    if not threads:
        return jsonify({"success": False, "error": "No threads available for comparison"}), 400

    comparison = compare_all_algorithms(
        threads=threads,
        time_quantum=time_quantum,
        context_switch_overhead=context_switch_overhead
    )

    return jsonify({
        "success": True,
        "comparison": comparison,
        "data": comparison
    })

