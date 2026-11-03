"""
ThreadLab Launcher.
Run with: py run.py
"""
import sys
import os

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from backend.app import create_app
from backend.config import Config

if __name__ == "__main__":
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    app = create_app()
    print("=" * 65)
    print("ThreadLab - Interactive Multithreading Simulation Platform")
    print(f"Backend & Frontend available at: http://{Config.HOST}:{Config.PORT}")
    print("=" * 65)
    app.run(host=Config.HOST, port=Config.PORT, debug=False)


