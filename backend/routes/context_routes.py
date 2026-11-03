"""
Flask REST API Routes for Context Switching Simulator.
"""
from flask import Blueprint, jsonify, request
from backend.engine.context_switch import ContextSwitchSimulator

context_bp = Blueprint("context", __name__, url_prefix="/api/context-switching")
_simulator = ContextSwitchSimulator()


@context_bp.route("/state", methods=["GET"])
def get_state():
    step = int(request.args.get("step", 1))
    data = _simulator.get_simulation_state(step=step)
    return jsonify({
        "success": True,
        "step": step,
        "context": data
    })


@context_bp.route("/step", methods=["POST"])
def step_simulation():
    body = request.get_json() or {}
    step = int(body.get("step", 1))
    data = _simulator.get_simulation_state(step=step)
    return jsonify({
        "success": True,
        "step": step,
        "context": data
    })

