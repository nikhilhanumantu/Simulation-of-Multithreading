"""
ThreadLab Flask Application.
Main entry point serving REST API endpoints and integrated frontend pages.
"""
import os
import sys

# Ensure project root is on Python sys.path
PROJECT_ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS

from backend.config import Config, FRONTEND_DIR, BASE_DIR
from backend.routes.thread_routes import thread_bp
from backend.routes.scheduling_routes import scheduling_bp
from backend.routes.synchronization_routes import sync_bp
from backend.routes.deadlock_routes import deadlock_bp
from backend.routes.context_routes import context_bp
from backend.routes.analytics_routes import analytics_bp
from backend.routes.system_routes import system_bp


def create_app(config_class=Config):
    app = Flask(
        __name__,
        static_folder=FRONTEND_DIR,
        static_url_path="/static"
    )
    app.config.from_object(config_class)

    # Enable CORS for all routes
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Register API Blueprints
    app.register_blueprint(thread_bp)
    app.register_blueprint(scheduling_bp)
    app.register_blueprint(sync_bp)
    app.register_blueprint(deadlock_bp)
    app.register_blueprint(context_bp)
    app.register_blueprint(analytics_bp)
    app.register_blueprint(system_bp)

    # Frontend Page Routes
    @app.route("/")
    @app.route("/landing")
    def serve_index():
        return send_from_directory(FRONTEND_DIR, "index.html")

    @app.route("/login")
    def serve_login():
        return send_from_directory(os.path.join(FRONTEND_DIR, "pages"), "login.html")

    @app.route("/dashboard")
    def serve_dashboard():
        return send_from_directory(os.path.join(FRONTEND_DIR, "pages"), "dashboard.html")

    @app.route("/thread-manager")
    @app.route("/threads")
    def serve_thread_manager():
        return send_from_directory(os.path.join(FRONTEND_DIR, "pages"), "thread-manager.html")

    @app.route("/cpu-scheduling")
    @app.route("/scheduler")
    def serve_cpu_scheduling():
        return send_from_directory(os.path.join(FRONTEND_DIR, "pages"), "cpu-scheduling.html")

    @app.route("/thread-lifecycle")
    @app.route("/lifecycle")
    def serve_thread_lifecycle():
        return send_from_directory(os.path.join(FRONTEND_DIR, "pages"), "thread-lifecycle.html")

    @app.route("/synchronization-lab")
    @app.route("/synchronization")
    def serve_synchronization():
        return send_from_directory(os.path.join(FRONTEND_DIR, "pages"), "synchronization.html")

    @app.route("/deadlock-lab")
    @app.route("/deadlock")
    def serve_deadlock():
        return send_from_directory(os.path.join(FRONTEND_DIR, "pages"), "deadlock.html")

    @app.route("/context-switching")
    def serve_context_switching():
        return send_from_directory(os.path.join(FRONTEND_DIR, "pages"), "context-switching.html")

    @app.route("/performance-analytics")
    @app.route("/analytics")
    def serve_analytics():
        return send_from_directory(os.path.join(FRONTEND_DIR, "pages"), "analytics.html")

    @app.route("/learning-mode")
    @app.route("/learning")
    def serve_learning():
        return send_from_directory(os.path.join(FRONTEND_DIR, "pages"), "learning.html")

    # Static asset fallback routes
    @app.route("/frontend/<path:filename>")
    def serve_frontend_files(filename):
        return send_from_directory(FRONTEND_DIR, filename)

    @app.route("/<path:filename>")
    def serve_root_static(filename):
        # Check in frontend dir first
        full_path = os.path.join(FRONTEND_DIR, filename)
        if os.path.exists(full_path):
            return send_from_directory(FRONTEND_DIR, filename)
        # Check in project root (for screen images or static assets)
        root_path = os.path.join(BASE_DIR, filename)
        if os.path.exists(root_path):
            return send_from_directory(BASE_DIR, filename)
        return jsonify({"error": f"File {filename} not found"}), 404

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"error": "Resource not found", "status": 404}), 404

    @app.errorhandler(500)
    def server_error(e):
        return jsonify({"error": "Internal server error", "status": 500, "details": str(e)}), 500

    return app


if __name__ == "__main__":
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    app = create_app()
    print("=" * 60)
    print("ThreadLab - Multithreading Simulation Platform")
    print("Running on http://127.0.0.1:5000")
    print("=" * 60)
    app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG)

