"""
Unit Tests for Concurrency & Synchronization Primitives:
- Race condition with lost updates
- Mutex lock protection
- Counting Semaphores
- Producer-Consumer Bounded Buffer
"""
import pytest
from backend.synchronization.race_condition import SharedCounterExperiment
from backend.synchronization.mutex import simulate_mutex_competition
from backend.synchronization.semaphore import simulate_semaphore
from backend.synchronization.producer_consumer import simulate_producer_consumer


def test_race_condition_lost_updates():
    exp = SharedCounterExperiment(iterations=1000)
    res = exp.run_without_sync()
    assert res["synchronized"] is False
    assert res["is_thread_safe"] is False
    assert res["expected_final"] == 2000
    assert res["final_counter"] < 2000
    assert res["lost_writes"] > 0


def test_mutex_guaranteed_consistency():
    exp = SharedCounterExperiment(iterations=1000)
    res = exp.run_with_mutex()
    assert res["synchronized"] is True
    assert res["is_thread_safe"] is True
    assert res["expected_final"] == 2000
    assert res["final_counter"] == 2000
    assert res["lost_writes"] == 0


def test_mutex_simulation():
    res = simulate_mutex_competition(num_threads=3)
    assert res["total_threads"] == 3
    assert len(res["events"]) > 0
    actions = [e["action"] for e in res["events"]]
    assert "ACQUIRE" in actions
    assert "RELEASE" in actions
    assert "BLOCK" in actions


def test_semaphore_simulation():
    res = simulate_semaphore(initial_permits=2, total_threads=4)
    assert res["initial_permits"] == 2
    actions = [e["action"] for e in res["events"]]
    assert "WAIT_GRANTED" in actions
    assert "WAIT_BLOCKED" in actions
    assert "SIGNAL" in actions


def test_producer_consumer():
    res = simulate_producer_consumer(buffer_size=4, operations_count=6)
    assert res["buffer_size"] == 4
    actions = [e["action"] for e in res["events"]]
    assert "PRODUCE" in actions
    assert "CONSUME" in actions

