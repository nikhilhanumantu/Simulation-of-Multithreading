"""
Integration Tests for Flask REST API Endpoints with validation checks.
"""
import pytest
from backend.app import create_app
from backend.engine.thread_manager import thread_manager_instance


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        # Ensure preset threads loaded before test
        thread_manager_instance.load_preset()
        yield client


def test_api_threads(client):
    res = client.get("/api/threads")
    assert res.status_code == 200
    data = res.get_json()
    assert data["success"] is True
    assert "threads" in data
    assert len(data["threads"]) >= 4


def test_api_thread_validation_rejections(client):
    # 1. Reject duplicate ID
    res_dup = client.post("/api/threads", json={"id": "T1", "burst_time": 4})
    assert res_dup.status_code == 400
    assert "already exists" in res_dup.get_json()["error"]

    # 2. Reject negative arrival time
    res_neg_arr = client.post("/api/threads", json={"id": "T99", "arrival_time": -3, "burst_time": 4})
    assert res_neg_arr.status_code == 400
    assert "cannot be negative" in res_neg_arr.get_json()["error"]

    # 3. Reject zero or negative burst time
    res_zero_burst = client.post("/api/threads", json={"id": "T99", "burst_time": 0})
    assert res_zero_burst.status_code == 400
    assert "greater than zero" in res_zero_burst.get_json()["error"]

    # 4. Reject invalid priority < 1
    res_bad_prio = client.post("/api/threads", json={"id": "T99", "burst_time": 4, "priority": 0})
    assert res_bad_prio.status_code == 400
    assert "Priority must be 1 or greater" in res_bad_prio.get_json()["error"]


def test_api_scheduling(client):
    res = client.post("/api/scheduling/run", json={"algorithm": "Round Robin", "time_quantum": 2})
    assert res.status_code == 200
    data = res.get_json()
    assert data["success"] is True
    assert "result" in data
    assert data["result"]["algorithm"] == "Round Robin"
    assert "segments" in data["result"]
    assert "metrics" in data["result"]
    assert data["result"]["segments"][0]["type"] in ["THREAD_EXECUTION", "CPU_IDLE", "CONTEXT_SWITCH"]


def test_api_scheduling_compare(client):
    res = client.post("/api/scheduling/compare", json={"time_quantum": 2})
    assert res.status_code == 200
    data = res.get_json()
    assert data["success"] is True
    assert len(data["comparison"]["comparison_table"]) == 4


def test_api_synchronization_race(client):
    res = client.post("/api/synchronization/race-condition", json={"iterations": 1000, "with_mutex": False})
    assert res.status_code == 200
    data = res.get_json()
    assert data["success"] is True
    assert data["result"]["final_counter"] < 2000

    res_mut = client.post("/api/synchronization/race-condition", json={"iterations": 1000, "with_mutex": True})
    assert res_mut.status_code == 200
    data_mut = res_mut.get_json()
    assert data_mut["result"]["final_counter"] == 2000


def test_api_deadlock_detect(client):
    res = client.post("/api/deadlock/detect", json={})
    assert res.status_code == 200
    data = res.get_json()
    assert data["success"] is True
    assert data["result"]["deadlock_detected"] is True


def test_api_banker_validation(client):
    # Invalid banker input where allocation exceeds max claim
    bad_banker = {
        "available": [3, 3],
        "max_matrix": [[2, 2]],
        "allocation_matrix": [[3, 1]]
    }
    res = client.post("/api/deadlock/banker", json=bad_banker)
    assert res.status_code == 400
    assert "cannot exceed its maximum claim" in res.get_json()["error"]


def test_api_context_switch(client):
    res = client.get("/api/context-switching/state?step=2")
    assert res.status_code == 200
    data = res.get_json()
    assert data["success"] is True
    assert data["step"] == 2


def test_api_system_overview(client):
    res = client.get("/api/system/overview")
    assert res.status_code == 200
    data = res.get_json()
    assert data["success"] is True
    assert "stats" in data
    assert "cpu_utilization" in data
    assert "recent_activity" in data
    assert len(data["recent_activity"]) > 0


def test_api_analytics_endpoints(client):
    res = client.get("/api/analytics")
    assert res.status_code == 200
    data = res.get_json()
    assert data["success"] is True
    assert "comparison" in data
    assert "data" in data

    res_comp = client.get("/api/analytics/comparison")
    assert res_comp.status_code == 200
    data_comp = res_comp.get_json()
    assert data_comp["success"] is True
    assert len(data_comp["comparison_table"]) == 4
