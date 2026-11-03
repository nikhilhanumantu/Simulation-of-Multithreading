"""
Priority CPU Scheduling Algorithm (Non-preemptive).
Selects the arrived thread with the highest priority (where 1 = Highest Priority).
"""
from typing import List, Dict, Any
from copy import deepcopy
from backend.models.thread_model import Thread
from backend.models.simulation_model import SchedulingResult, GanttSegment


def run_priority(threads: List[Thread], context_switch_overhead: int = 0) -> SchedulingResult:
    if not threads:
        return SchedulingResult(algorithm="Priority")

    pool = [deepcopy(t) for t in threads]
    remaining = pool.copy()
    completed: List[Thread] = []
    timeline: List[GanttSegment] = []

    current_time = 0
    busy_time = 0
    idle_time = 0
    context_switch_count = 0
    total_cs_time = 0
    last_thread_id = None

    while remaining:
        arrived = [t for t in remaining if t.arrival_time <= current_time]

        if not arrived:
            earliest = min(remaining, key=lambda t: t.arrival_time)
            idle_dur = earliest.arrival_time - current_time
            timeline.append(GanttSegment(
                thread_id="IDLE",
                name="CPU Idle",
                start_time=current_time,
                end_time=earliest.arrival_time,
                duration=idle_dur,
                color="#E2E8F0",
                segment_type="idle"
            ))
            idle_time += idle_dur
            current_time = earliest.arrival_time
            last_thread_id = None
            continue

        # Smallest priority integer = Highest priority
        chosen = min(arrived, key=lambda t: (t.priority, t.arrival_time, t.id))
        remaining.remove(chosen)

        if context_switch_overhead > 0 and last_thread_id is not None and last_thread_id != chosen.id:
            cs_start = current_time
            current_time += context_switch_overhead
            timeline.append(GanttSegment(
                thread_id="CS",
                name="Context Switch",
                start_time=cs_start,
                end_time=current_time,
                duration=context_switch_overhead,
                color="#CBD5E1",
                segment_type="context_switch"
            ))
            context_switch_count += 1
            total_cs_time += context_switch_overhead

        start_time = current_time
        chosen.start_time = start_time
        chosen.first_response_time = start_time
        chosen.response_time = start_time - chosen.arrival_time

        exec_dur = chosen.burst_time
        current_time += exec_dur
        busy_time += exec_dur

        chosen.completion_time = current_time
        chosen.turnaround_time = chosen.completion_time - chosen.arrival_time
        chosen.waiting_time = chosen.turnaround_time - chosen.burst_time
        chosen.state = "TERMINATED"

        timeline.append(GanttSegment(
            thread_id=chosen.id,
            name=chosen.name,
            start_time=start_time,
            end_time=current_time,
            duration=exec_dur,
            color=chosen.color,
            segment_type="execution"
        ))

        completed.append(chosen)
        last_thread_id = chosen.id

    total_time = current_time
    n = len(completed)
    avg_wt = sum(t.waiting_time for t in completed) / n if n else 0.0
    avg_tat = sum(t.turnaround_time for t in completed) / n if n else 0.0
    avg_rt = sum(t.response_time for t in completed) / n if n else 0.0
    cpu_util = (busy_time / total_time * 100.0) if total_time > 0 else 0.0
    throughput = (n / total_time) if total_time > 0 else 0.0

    return SchedulingResult(
        algorithm="Priority",
        timeline=timeline,
        thread_metrics=[t.to_dict() for t in completed],
        total_time=total_time,
        busy_time=busy_time,
        idle_time=idle_time,
        context_switch_count=context_switch_count,
        context_switch_overhead=total_cs_time,
        avg_waiting_time=round(avg_wt, 2),
        avg_turnaround_time=round(avg_tat, 2),
        avg_response_time=round(avg_rt, 2),
        cpu_utilization=round(cpu_util, 1),
        throughput=round(throughput, 3),
        context_switch_overhead_unit=context_switch_overhead
    )

