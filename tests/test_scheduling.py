"""
Unit Tests for CPU Scheduling Algorithms:
- FCFS
- SJF
- Priority (1 = highest)
- Round Robin (preemptive, time quantum, context switch overhead)
- Standardized Gantt segment types & metric calculations
"""
import pytest
from backend.models.thread_model import Thread
from backend.scheduling.fcfs import run_fcfs
from backend.scheduling.sjf import run_sjf
from backend.scheduling.priority import run_priority
from backend.scheduling.round_robin import run_round_robin
from backend.scheduling.scheduler import compare_all_algorithms


@pytest.fixture
def sample_threads():
    return [
        Thread(id="T1", arrival_time=0, burst_time=8, priority=2),
        Thread(id="T2", arrival_time=1, burst_time=4, priority=1),
        Thread(id="T3", arrival_time=2, burst_time=6, priority=3),
        Thread(id="T4", arrival_time=3, burst_time=3, priority=2),
    ]


def test_fcfs_execution(sample_threads):
    res = run_fcfs(sample_threads)
    assert res.algorithm == "FCFS"
    assert res.total_time == 8 + 4 + 6 + 3  # 21
    assert res.busy_time == 21
    assert res.idle_time == 0
    assert len(res.timeline) == 4
    assert res.timeline[0].thread_id == "T1"
    assert res.timeline[1].thread_id == "T2"
    assert res.cpu_utilization == 100.0
    assert res.avg_waiting_time > 0
    assert res.avg_turnaround_time > 0

    # Verify standardized segment types
    seg_dict = res.timeline[0].to_dict()
    assert seg_dict["type"] == "THREAD_EXECUTION"
    assert "start" in seg_dict and "end" in seg_dict


def test_fcfs_idle_time():
    # T2 arrives at time 10, creating 5 units of CPU idle time
    threads = [
        Thread(id="T1", arrival_time=0, burst_time=5),
        Thread(id="T2", arrival_time=10, burst_time=4),
    ]
    res = run_fcfs(threads)
    assert res.total_time == 14
    assert res.idle_time == 5
    assert res.busy_time == 9
    idle_segs = [s for s in res.timeline if s.segment_type == "idle"]
    assert len(idle_segs) == 1
    assert idle_segs[0].duration == 5
    assert idle_segs[0].to_dict()["type"] == "CPU_IDLE"


def test_sjf_execution(sample_threads):
    res = run_sjf(sample_threads)
    assert res.algorithm == "SJF"
    assert res.total_time == 21
    order = [s.thread_id for s in res.timeline if s.segment_type == "execution"]
    assert order == ["T1", "T4", "T2", "T3"]


def test_priority_execution(sample_threads):
    res = run_priority(sample_threads)
    assert res.algorithm == "Priority"
    assert res.total_time == 21
    order = [s.thread_id for s in res.timeline if s.segment_type == "execution"]
    assert order == ["T1", "T2", "T4", "T3"]


def test_round_robin_preemption(sample_threads):
    q = 2
    res = run_round_robin(sample_threads, time_quantum=q)
    assert res.algorithm == "Round Robin"
    assert res.time_quantum == 2
    assert res.total_time == 21
    t1_segs = [s for s in res.timeline if s.thread_id == "T1"]
    assert len(t1_segs) == 4


def test_round_robin_context_switch_penalty(sample_threads):
    res = run_round_robin(sample_threads, time_quantum=2, context_switch_overhead=1)
    assert res.context_switch_count > 0
    assert res.context_switch_overhead > 0
    assert res.total_time > 21

    # Verify context switch segment type
    cs_segs = [s for s in res.timeline if s.segment_type == "context_switch"]
    assert len(cs_segs) > 0
    assert cs_segs[0].to_dict()["type"] == "CONTEXT_SWITCH"


def test_metric_mathematical_consistency(sample_threads):
    res = run_fcfs(sample_threads)
    for t in res.thread_metrics:
        # TAT = Completion - Arrival
        assert t["turnaround_time"] == t["completion_time"] - t["arrival_time"]
        # WT = Turnaround - Burst
        assert t["waiting_time"] == t["turnaround_time"] - t["burst_time"]
        # RT = First Start - Arrival
        assert t["response_time"] == t["start_time"] - t["arrival_time"]

    # CPU Utilization = busy_time / total_time * 100
    expected_util = (res.busy_time / res.total_time) * 100.0
    assert pytest.approx(res.cpu_utilization, 0.01) == expected_util

    # Throughput = len(completed) / total_time
    expected_tp = len(res.thread_metrics) / res.total_time
    assert pytest.approx(res.throughput, abs=0.01) == expected_tp


def test_compare_all_algorithms(sample_threads):
    comp = compare_all_algorithms(sample_threads, time_quantum=2)
    assert "results" in comp
    assert "comparison_table" in comp
    assert len(comp["comparison_table"]) == 4
    assert comp["best_waiting"] in ["FCFS", "SJF", "Priority", "Round Robin (q=2)"]
