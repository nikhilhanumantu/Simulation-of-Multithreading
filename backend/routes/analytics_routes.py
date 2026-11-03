"""
Flask REST API Routes for Performance Analytics.
"""
from flask import Blueprint, jsonify, request
from backend.engine.thread_manager import thread_manager_instance
from backend.scheduling.scheduler import compare_all_algorithms

analytics_bp = Blueprint("analytics", __name__, url_prefix="/api/analytics")


@analytics_bp.route("", methods=["GET"])
def get_analytics():
    threads = thread_manager_instance.get_all()
    q = int(request.args.get("quantum", 2))
    cs = int(request.args.get("overhead", 0))

    if threads:
        comp = compare_all_algorithms(threads=threads, time_quantum=q, context_switch_overhead=cs)
    else:
        comp = {
            "results": {},
            "comparison_table": [],
            "best_waiting": "None",
            "best_turnaround": "None",
            "best_throughput": "None"
        }

    return jsonify({
        "success": True,
        "dataset": "Current Active Thread Pool",
        "thread_count": len(threads),
        "comparison": comp,
        "data": {
            "comparison": comp
        }
    })


@analytics_bp.route("/comparison", methods=["GET"])
def get_comparison():
    threads = thread_manager_instance.get_all()
    q = int(request.args.get("quantum", 2))
    cs = int(request.args.get("overhead", 0))

    if threads:
        comp = compare_all_algorithms(threads=threads, time_quantum=q, context_switch_overhead=cs)
        table = comp["comparison_table"]
        best_w = comp["best_waiting"]
        best_t = comp["best_turnaround"]
        best_tp = comp["best_throughput"]
    else:
        comp = {
            "results": {},
            "comparison_table": [],
            "best_waiting": "None",
            "best_turnaround": "None",
            "best_throughput": "None"
        }
        table = []
        best_w = "None"
        best_t = "None"
        best_tp = "None"

    return jsonify({
        "success": True,
        "comparison": comp,
        "data": {
            "comparison": comp
        },
        "comparison_table": table,
        "best_waiting": best_w,
        "best_turnaround": best_t,
        "best_throughput": best_tp
    })
