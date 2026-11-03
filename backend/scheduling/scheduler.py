"""
Scheduler Dispatcher & Benchmark Suite.
Runs individual scheduling algorithms or runs all 4 on the identical workload for fair comparison.
"""
from typing import List, Dict, Any
from backend.models.thread_model import Thread
from backend.models.simulation_model import SchedulingResult
from backend.scheduling.fcfs import run_fcfs
from backend.scheduling.sjf import run_sjf
from backend.scheduling.priority import run_priority
from backend.scheduling.round_robin import run_round_robin


def run_scheduler(
    algorithm: str,
    threads: List[Thread],
    time_quantum: int = 2,
    context_switch_overhead: int = 0
) -> SchedulingResult:
    algo_key = algorithm.strip().lower().replace("-", " ").replace("_", " ")

    if "fcfs" in algo_key or "first come" in algo_key:
        return run_fcfs(threads, context_switch_overhead=context_switch_overhead)
    elif "sjf" in algo_key or "shortest" in algo_key:
        return run_sjf(threads, context_switch_overhead=context_switch_overhead)
    elif "priority" in algo_key:
        return run_priority(threads, context_switch_overhead=context_switch_overhead)
    elif "round" in algo_key or "robin" in algo_key or "rr" in algo_key:
        return run_round_robin(threads, time_quantum=time_quantum, context_switch_overhead=context_switch_overhead)
    else:
        # Default fallback
        return run_round_robin(threads, time_quantum=time_quantum, context_switch_overhead=context_switch_overhead)


def compare_all_algorithms(
    threads: List[Thread],
    time_quantum: int = 2,
    context_switch_overhead: int = 0
) -> Dict[str, Any]:
    """Runs all 4 algorithms on identical thread set and returns comparison table and chart metrics."""
    fcfs_res = run_fcfs(threads, context_switch_overhead=context_switch_overhead)
    sjf_res = run_sjf(threads, context_switch_overhead=context_switch_overhead)
    prio_res = run_priority(threads, context_switch_overhead=context_switch_overhead)
    rr_res = run_round_robin(threads, time_quantum=time_quantum, context_switch_overhead=context_switch_overhead)

    comparison_table = [
        {
            "algorithm": "FCFS",
            "avg_waiting": fcfs_res.avg_waiting_time,
            "avg_turnaround": fcfs_res.avg_turnaround_time,
            "avg_response": fcfs_res.avg_response_time,
            "cpu_utilization": fcfs_res.cpu_utilization,
            "throughput": fcfs_res.throughput,
            "context_switches": fcfs_res.context_switch_count,
            "total_time": fcfs_res.total_time,
        },
        {
            "algorithm": "SJF",
            "avg_waiting": sjf_res.avg_waiting_time,
            "avg_turnaround": sjf_res.avg_turnaround_time,
            "avg_response": sjf_res.avg_response_time,
            "cpu_utilization": sjf_res.cpu_utilization,
            "throughput": sjf_res.throughput,
            "context_switches": sjf_res.context_switch_count,
            "total_time": sjf_res.total_time,
        },
        {
            "algorithm": "Priority",
            "avg_waiting": prio_res.avg_waiting_time,
            "avg_turnaround": prio_res.avg_turnaround_time,
            "avg_response": prio_res.avg_response_time,
            "cpu_utilization": prio_res.cpu_utilization,
            "throughput": prio_res.throughput,
            "context_switches": prio_res.context_switch_count,
            "total_time": prio_res.total_time,
        },
        {
            "algorithm": f"Round Robin (q={time_quantum})",
            "avg_waiting": rr_res.avg_waiting_time,
            "avg_turnaround": rr_res.avg_turnaround_time,
            "avg_response": rr_res.avg_response_time,
            "cpu_utilization": rr_res.cpu_utilization,
            "throughput": rr_res.throughput,
            "context_switches": rr_res.context_switch_count,
            "total_time": rr_res.total_time,
        },
    ]

    return {
        "results": {
            "FCFS": fcfs_res.to_dict(),
            "SJF": sjf_res.to_dict(),
            "Priority": prio_res.to_dict(),
            "Round Robin": rr_res.to_dict(),
        },
        "fcfs": fcfs_res.to_dict(),
        "sjf": sjf_res.to_dict(),
        "priority": prio_res.to_dict(),
        "round_robin": rr_res.to_dict(),
        "comparison_table": comparison_table,
        "best_waiting": min(comparison_table, key=lambda x: x["avg_waiting"])["algorithm"],
        "best_turnaround": min(comparison_table, key=lambda x: x["avg_turnaround"])["algorithm"],
        "best_throughput": max(comparison_table, key=lambda x: x["throughput"])["algorithm"],
    }
