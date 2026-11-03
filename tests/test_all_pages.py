import pytest
from backend.app import create_app
from backend.config import TestingConfig


@pytest.fixture
def client():
    app = create_app(TestingConfig)
    with app.test_client() as client:
        yield client


def test_page_routes(client):
    routes = [
        "/",
        "/landing",
        "/login",
        "/dashboard",
        "/thread-manager",
        "/threads",
        "/cpu-scheduling",
        "/scheduler",
        "/thread-lifecycle",
        "/lifecycle",
        "/synchronization-lab",
        "/synchronization",
        "/deadlock-lab",
        "/deadlock",
        "/context-switching",
        "/performance-analytics",
        "/analytics",
        "/learning-mode",
        "/learning",
    ]
    for r in routes:
        res = client.get(r)
        assert res.status_code == 200, f"Route {r} failed with status {res.status_code}"
        assert b"<!DOCTYPE html>" in res.data or b"<html" in res.data


def test_direct_page_files(client):
    pages = [
        "/pages/login.html",
        "/pages/dashboard.html",
        "/pages/thread-manager.html",
        "/pages/cpu-scheduling.html",
        "/pages/thread-lifecycle.html",
        "/pages/synchronization.html",
        "/pages/deadlock.html",
        "/pages/context-switching.html",
        "/pages/analytics.html",
        "/pages/learning.html",
    ]
    for p in pages:
        res = client.get(p)
        assert res.status_code == 200, f"Page file {p} failed with status {res.status_code}"
        assert len(res.data) > 500


def test_static_js_assets(client):
    assets = [
        "/js/api.js",
        "/js/navigation.js"
    ]
    for a in assets:
        res = client.get(a)
        assert res.status_code == 200, f"Asset {a} failed with status {res.status_code}"
        assert len(res.data) > 100


def test_system_status_and_overview(client):
    res = client.get("/api/system/overview")
    assert res.status_code == 200
    data = res.get_json()
    assert data["success"] is True
    assert "stats" in data
    assert "cpu_utilization" in data


def test_all_algorithms_comparison(client):
    res = client.get("/api/analytics")
    assert res.status_code == 200
    d = res.get_json()["comparison"]
    assert "fcfs" in d
    assert "sjf" in d
    assert "priority" in d
    assert "round_robin" in d

