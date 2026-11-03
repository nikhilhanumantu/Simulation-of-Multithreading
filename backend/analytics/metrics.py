"""
Performance Analytics Metric Engine.
Calculates Turnaround Time, Waiting Time, Response Time, CPU Utilization, and Throughput according to standard Operating System formulas.
"""
from typing import List, Dict, Any
from backend.models.thread_model import Thread


def calculate_turnaround_time(completion_time: int, arrival_time: int) -> int:
    """TAT = Completion Time - Arrival Time"""
    return max(0, completion_time - arrival_time)


def calculate_waiting_time(turnaround_time: int, burst_time: int) -> int:
    """WT = Turnaround Time - Burst Time"""
    return max(0, turnaround_time - burst_time)


def calculate_response_time(first_start_time: int, arrival_time: int) -> int:
    """RT = First Start Time - Arrival Time"""
    return max(0, first_start_time - arrival_time)


def calculate_cpu_utilization(busy_time: int, total_time: int) -> float:
    """CPU Utilization = (Busy Time / Total Time) * 100"""
    if total_time <= 0:
        return 0.0
    return round((busy_time / total_time) * 100.0, 1)


def calculate_throughput(completed_threads: int, total_time: int) -> float:
    """Throughput = Completed Threads / Total Time"""
    if total_time <= 0:
        return 0.0
    return round(completed_threads / total_time, 3)


def generate_analytics_report(threads: List[Thread], total_time: int, busy_time: int) -> Dict[str, Any]:
    n = len(threads)
    if n == 0:
        return {
            "total_threads": 0,
            "avg_waiting_time": 0.0,
            "avg_turnaround_time": 0.0,
            "avg_response_time": 0.0,
            "cpu_utilization": 0.0,
            "throughput": 0.0,
            "threads": []
        }

    thread_data = []
    for t in threads:
        tat = calculate_turnaround_time(t.completion_time or 0, t.arrival_time)
        wt = calculate_waiting_time(tat, t.burst_time)
        rt = calculate_response_time(t.first_response_time or 0, t.arrival_time)
        thread_data.append({
            "id": t.id,
            "name": t.name,
            "arrival_time": t.arrival_time,
            "burst_time": t.burst_time,
            "completion_time": t.completion_time,
            "turnaround_time": tat,
            "waiting_time": wt,
            "response_time": rt
        })

    avg_tat = sum(x["turnaround_time"] for x in thread_data) / n
    avg_wt = sum(x["waiting_time"] for x in thread_data) / n
    avg_rt = sum(x["response_time"] for x in thread_data) / n

    return {
        "total_threads": n,
        "avg_waiting_time": round(avg_wt, 2),
        "avg_turnaround_time": round(avg_tat, 2),
        "avg_response_time": round(avg_rt, 2),
        "cpu_utilization": calculate_cpu_utilization(busy_time, total_time),
        "throughput": calculate_throughput(n, total_time),
        "total_time": total_time,
        "busy_time": busy_time,
        "threads": thread_data
    }

