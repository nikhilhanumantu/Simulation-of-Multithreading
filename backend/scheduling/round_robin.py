"""
Round Robin (RR) CPU Scheduling Algorithm.
Preemptive scheduling where each thread receives a cyclic time slice (quantum).
"""
from typing import List, Dict, Any
from collections import deque
from copy import deepcopy
from backend.models.thread_model import Thread
from backend.models.simulation_model import SchedulingResult, GanttSegment


def run_round_robin(threads: List[Thread], time_quantum: int = 2, context_switch_overhead: int = 0) -> SchedulingResult:
    if not threads:
        return SchedulingResult(algorithm="Round Robin", time_quantum=time_quantum)

    if time_quantum <= 0:
        time_quantum = 1

    # Deepcopy to preserve original models
    pool = [deepcopy(t) for t in threads]
    for t in pool:
        t.remaining_time = t.burst_time

    # Sort un-arrived threads by arrival time, then ID
    unarrived = sorted(pool, key=lambda t: (t.arrival_time, t.id))
    ready_queue: deque[Thread] = deque()
    completed: List[Thread] = []
    timeline: List[GanttSegment] = []

    current_time = 0
    busy_time = 0
    idle_time = 0
    context_switch_count = 0
    total_cs_time = 0
    last_thread_id = None

    # Enqueue threads arriving at time 0
    while unarrived and unarrived[0].arrival_time <= current_time:
        t = unarrived.pop(0)
        t.state = "READY"
        ready_queue.append(t)

    while ready_queue or unarrived:
        if not ready_queue:
            # Advance to next arrival
            next_arrival = unarrived[0].arrival_time
            idle_dur = next_arrival - current_time
            timeline.append(GanttSegment(
                thread_id="IDLE",
                name="CPU Idle",
                start_time=current_time,
                end_time=next_arrival,
                duration=idle_dur,
                color="#E2E8F0",
                segment_type="idle"
            ))
            idle_time += idle_dur
            current_time = next_arrival
            last_thread_id = None

            while unarrived and unarrived[0].arrival_time <= current_time:
                t = unarrived.pop(0)
                t.state = "READY"
                ready_queue.append(t)
            continue

        curr = ready_queue.popleft()

        # Context switch overhead if switching away from a different thread
        if context_switch_overhead > 0 and last_thread_id is not None and last_thread_id != curr.id:
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

            # While context switching, any newly arrived threads enter ready queue
            while unarrived and unarrived[0].arrival_time <= current_time:
                t = unarrived.pop(0)
                t.state = "READY"
                ready_queue.append(t)

        if curr.first_response_time is None:
            curr.first_response_time = current_time
            curr.response_time = current_time - curr.arrival_time
            curr.start_time = current_time

        slice_dur = min(time_quantum, curr.remaining_time)
        start_time = current_time
        curr.state = "RUNNING"
        current_time += slice_dur
        busy_time += slice_dur
        curr.remaining_time -= slice_dur

        timeline.append(GanttSegment(
            thread_id=curr.id,
            name=curr.name,
            start_time=start_time,
            end_time=current_time,
            duration=slice_dur,
            color=curr.color,
            segment_type="execution"
        ))

        # Check for newly arrived threads during this slice execution
        while unarrived and unarrived[0].arrival_time <= current_time:
            t = unarrived.pop(0)
            t.state = "READY"
            ready_queue.append(t)

        if curr.remaining_time > 0:
            curr.state = "READY"
            ready_queue.append(curr)
        else:
            curr.state = "TERMINATED"
            curr.completion_time = current_time
            curr.turnaround_time = curr.completion_time - curr.arrival_time
            curr.waiting_time = curr.turnaround_time - curr.burst_time
            completed.append(curr)

        last_thread_id = curr.id

    total_time = current_time
    n = len(completed)
    avg_wt = sum(t.waiting_time for t in completed) / n if n else 0.0
    avg_tat = sum(t.turnaround_time for t in completed) / n if n else 0.0
    avg_rt = sum(t.response_time for t in completed) / n if n else 0.0
    cpu_util = (busy_time / total_time * 100.0) if total_time > 0 else 0.0
    throughput = (n / total_time) if total_time > 0 else 0.0

    return SchedulingResult(
        algorithm="Round Robin",
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
        time_quantum=time_quantum,
        context_switch_overhead_unit=context_switch_overhead
    )

