"""
Unit Tests for Deadlock Lab:
- Cycle detection on Resource Allocation Graph
- Circular wait identification
- Banker's Algorithm safe-state & sequence finder
- Deadlock recovery
- Comprehensive input validation & edge case rejection
"""
import pytest
from backend.deadlock.detection import detect_deadlock
from backend.deadlock.banker_algorithm import run_bankers_algorithm
from backend.deadlock.recovery import recover_by_termination


def test_deadlock_detection_with_cycle():
    # T1 holds R1, requests R2; T2 holds R2, requests R1 (Cycle!)
    alloc = {"R1": "T1", "R2": "T2"}
    req = {"T1": "R2", "T2": "R1"}

    res = detect_deadlock(alloc, req)
    assert res["deadlock_detected"] is True
    assert set(res["deadlocked_threads"]) == {"T1", "T2"}
    assert set(res["deadlocked_resources"]) == {"R1", "R2"}


def test_deadlock_detection_no_cycle():
    # T1 holds R1, requests R2; T2 holds R2, requests nothing (Safe!)
    alloc = {"R1": "T1", "R2": "T2"}
    req = {"T1": "R2"}

    res = detect_deadlock(alloc, req)
    assert res["deadlock_detected"] is False
    assert len(res["cycle_path"]) == 0


def test_deadlock_detection_input_handling():
    # Null or empty inputs should not crash
    res = detect_deadlock(None, None)
    assert res["deadlock_detected"] is False

    # Invalid non-dict input should raise ValueError
    with pytest.raises(ValueError, match="must be a dictionary"):
        detect_deadlock(["invalid"], {})


def test_bankers_algorithm_safe_state():
    avail = [3, 3, 2]
    max_m = [
        [7, 5, 3],
        [3, 2, 2],
        [9, 0, 2],
        [2, 2, 2],
        [4, 3, 3]
    ]
    alloc_m = [
        [0, 1, 0],
        [2, 0, 0],
        [3, 0, 2],
        [2, 1, 1],
        [0, 0, 2]
    ]
    procs = ["P0", "P1", "P2", "P3", "P4"]

    res = run_bankers_algorithm(avail, max_m, alloc_m, procs)
    assert res["is_safe"] is True
    assert len(res["safe_sequence"]) == 5
    assert res["safe_sequence"][0] == "P1"


def test_bankers_algorithm_invalid_inputs():
    # Empty available vector
    with pytest.raises(ValueError, match="Invalid Available Vector"):
        run_bankers_algorithm([], [[1]], [[0]])

    # Row length mismatch
    with pytest.raises(ValueError, match="Row Length Mismatch"):
        run_bankers_algorithm([1, 2], [[1, 2, 3]], [[0, 1, 0]])

    # Negative value
    with pytest.raises(ValueError, match="must be a non-negative integer"):
        run_bankers_algorithm([1, -1], [[1, 2]], [[0, 1]])


def test_bankers_algorithm_allocation_exceeds_max():
    avail = [3, 3]
    max_m = [[2, 2]]
    alloc_m = [[3, 1]]  # Allocation (3) > Max (2) for R0!

    with pytest.raises(ValueError, match="cannot exceed its maximum claim"):
        run_bankers_algorithm(avail, max_m, alloc_m)


def test_deadlock_recovery():
    res = recover_by_termination(victim_thread="T2")
    assert res["action"] == "TERMINATE_THREAD"
    assert res["resolved"] is True
    assert res["after_state"]["deadlock_detected"] is False
