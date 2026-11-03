"""
Flask REST API Routes for Synchronization Lab.
"""
from flask import Blueprint, jsonify, request
from backend.synchronization.race_condition import SharedCounterExperiment
from backend.synchronization.mutex import simulate_mutex_competition
from backend.synchronization.semaphore import simulate_semaphore
from backend.synchronization.producer_consumer import simulate_producer_consumer

sync_bp = Blueprint("synchronization", __name__, url_prefix="/api/synchronization")


@sync_bp.route("/race-condition", methods=["POST"])
def run_race_condition():
    data = request.get_json() or {}
    iterations = int(data.get("iterations", 1000))
    with_mutex = bool(data.get("with_mutex", False))
    delay_mode = data.get("delay_mode", "normal")

    exp = SharedCounterExperiment(iterations=iterations, delay_mode=delay_mode)
    if with_mutex:
        result = exp.run_with_mutex()
    else:
        result = exp.run_without_sync()

    return jsonify({
        "success": True,
        "result": result
    })


@sync_bp.route("/mutex", methods=["POST"])
def run_mutex_demo():
    data = request.get_json() or {}
    num_threads = int(data.get("num_threads", 3))
    work_duration = int(data.get("work_duration", 2))

    result = simulate_mutex_competition(num_threads=num_threads, work_duration=work_duration)
    return jsonify({
        "success": True,
        "result": result
    })


@sync_bp.route("/semaphore", methods=["POST"])
def run_semaphore_demo():
    data = request.get_json() or {}
    initial_permits = int(data.get("initial_permits", 2))
    total_threads = int(data.get("total_threads", 4))

    result = simulate_semaphore(initial_permits=initial_permits, total_threads=total_threads)
    return jsonify({
        "success": True,
        "result": result
    })


@sync_bp.route("/producer-consumer", methods=["POST"])
def run_producer_consumer():
    data = request.get_json() or {}
    buffer_size = int(data.get("buffer_size", 5))
    operations_count = int(data.get("operations_count", 8))

    result = simulate_producer_consumer(buffer_size=buffer_size, operations_count=operations_count)
    return jsonify({
        "success": True,
        "result": result
    })

