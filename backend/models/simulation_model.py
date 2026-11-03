"""
Simulation Model for ThreadLab.
Defines standardized data structures for Gantt segments, execution telemetry, and scheduling results.
"""
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Any, Optional


@dataclass
class GanttSegment:
    thread_id: str
    name: str
    start_time: int
    end_time: int
    duration: int
    color: str
    segment_type: str = "execution"  # "execution", "idle", "context_switch"

    def to_dict(self) -> Dict[str, Any]:
        # Standardized segment type strings
        seg_lower = (self.segment_type or "execution").lower()
        if "idle" in seg_lower:
            norm_type = "CPU_IDLE"
            compat_type = "idle"
        elif "context" in seg_lower or "cs" in seg_lower:
            norm_type = "CONTEXT_SWITCH"
            compat_type = "context_switch"
        else:
            norm_type = "THREAD_EXECUTION"
            compat_type = "execution"

        return {
            "thread_id": self.thread_id,
            "name": self.name,
            "start": self.start_time,
            "start_time": self.start_time,
            "end": self.end_time,
            "end_time": self.end_time,
            "duration": self.duration,
            "color": self.color,
            "type": norm_type,
            "segment_type": compat_type
        }


@dataclass
class SchedulingResult:
    algorithm: str
    timeline: List[GanttSegment] = field(default_factory=list)
    thread_metrics: List[Dict[str, Any]] = field(default_factory=list)
    total_time: int = 0
    busy_time: int = 0
    idle_time: int = 0
    context_switch_count: int = 0
    context_switch_overhead: int = 0
    avg_waiting_time: float = 0.0
    avg_turnaround_time: float = 0.0
    avg_response_time: float = 0.0
    cpu_utilization: float = 0.0  # Percentage
    throughput: float = 0.0        # Completed threads / total time
    time_quantum: Optional[int] = None
    context_switch_overhead_unit: int = 0

    def to_dict(self) -> Dict[str, Any]:
        segs = [seg.to_dict() if isinstance(seg, GanttSegment) else seg for seg in self.timeline]
        return {
            "algorithm": self.algorithm,
            "time_quantum": self.time_quantum,
            "context_switch_overhead": self.context_switch_overhead,
            "context_switch_overhead_unit": self.context_switch_overhead_unit,
            "timeline": segs,
            "segments": segs,
            "thread_metrics": self.thread_metrics,
            "threads": self.thread_metrics,
            "total_time": self.total_time,
            "busy_time": self.busy_time,
            "idle_time": self.idle_time,
            "context_switch_count": self.context_switch_count,
            "avg_waiting_time": round(self.avg_waiting_time, 2),
            "avg_turnaround_time": round(self.avg_turnaround_time, 2),
            "avg_response_time": round(self.avg_response_time, 2),
            "cpu_utilization": round(self.cpu_utilization, 2),
            "throughput": round(self.throughput, 3),
            "metrics": {
                "average_waiting_time": round(self.avg_waiting_time, 2),
                "average_turnaround_time": round(self.avg_turnaround_time, 2),
                "average_response_time": round(self.avg_response_time, 2),
                "cpu_utilization": round(self.cpu_utilization, 2),
                "throughput": round(self.throughput, 3),
                "context_switches": self.context_switch_count,
                "total_time": self.total_time,
                "busy_time": self.busy_time,
                "idle_time": self.idle_time
            }
        }
