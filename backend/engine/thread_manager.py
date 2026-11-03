"""
Thread Manager Engine.
Provides CRUD operations, state transitions, preset loaders, and telemetry metrics with strict validation.
"""
from typing import List, Dict, Any, Optional
from copy import deepcopy
from backend.models.thread_model import Thread, THREAD_PALETTE

DEFAULT_PRESET_THREADS = [
    {"id": "T1", "name": "Worker-Compute", "arrival_time": 0, "burst_time": 8, "priority": 2, "state": "RUNNING"},
    {"id": "T2", "name": "Renderer-Sync", "arrival_time": 1, "burst_time": 4, "priority": 1, "state": "READY"},
    {"id": "T3", "name": "Disk-Writer", "arrival_time": 2, "burst_time": 6, "priority": 3, "state": "BLOCKED"},
    {"id": "T4", "name": "Background-Job", "arrival_time": 3, "burst_time": 3, "priority": 2, "state": "READY"},
]


class ThreadManager:
    def __init__(self):
        self._threads: Dict[str, Thread] = {}
        self.load_preset()

    def load_preset(self):
        self._threads.clear()
        for idx, item in enumerate(DEFAULT_PRESET_THREADS):
            t = Thread.from_dict(item)
            t.color = THREAD_PALETTE[idx % len(THREAD_PALETTE)]
            self._threads[t.id] = t

    def get_all(self) -> List[Thread]:
        def sort_key(t: Thread):
            digits = "".join(filter(str.isdigit, t.id))
            return (int(digits) if digits else 999, t.id)
        return sorted(list(self._threads.values()), key=sort_key)

    def get_by_id(self, thread_id: str) -> Optional[Thread]:
        return self._threads.get(thread_id)

    def create(self, data: Dict[str, Any]) -> Thread:
        tid = data.get("id")
        if not tid:
            existing_nums = [int("".join(filter(str.isdigit, t))) for t in self._threads if any(c.isdigit() for c in t)]
            next_num = (max(existing_nums) + 1) if existing_nums else 1
            tid = f"T{next_num}"
        else:
            tid = str(tid).strip().upper()
            if not tid.startswith("T"):
                tid = f"T{tid}"

        if tid in self._threads:
            raise ValueError(f"Duplicate Thread ID: Thread with ID '{tid}' already exists")

        # Validation: arrival_time cannot be negative
        try:
            arrival = int(data.get("arrival_time", 0))
        except (ValueError, TypeError):
            raise ValueError("Arrival time must be a valid integer")
        if arrival < 0:
            raise ValueError("Invalid Arrival Time: Arrival time cannot be negative")

        # Validation: burst_time must be strictly greater than 0
        try:
            burst = int(data.get("burst_time", 4))
        except (ValueError, TypeError):
            raise ValueError("Burst time must be a valid integer")
        if burst <= 0:
            raise ValueError("Invalid Burst Time: Burst time must be greater than zero")

        # Validation: priority must be >= 1 (1 is highest priority)
        try:
            priority = int(data.get("priority", 1))
        except (ValueError, TypeError):
            raise ValueError("Priority must be a valid integer")
        if priority < 1:
            raise ValueError("Invalid Priority: Priority must be 1 or greater (1 = highest priority)")

        name = data.get("name", f"Thread-{tid}").strip() or f"Thread-{tid}"
        state = data.get("state", "READY").upper()
        if state not in ("NEW", "READY", "RUNNING", "BLOCKED", "TERMINATED"):
            state = "READY"

        num = int("".join(filter(str.isdigit, tid))) if any(c.isdigit() for c in tid) else len(self._threads) + 1
        color = THREAD_PALETTE[(num - 1) % len(THREAD_PALETTE)]

        thread = Thread(
            id=tid,
            name=name,
            arrival_time=arrival,
            burst_time=burst,
            priority=priority,
            remaining_time=burst,
            state=state,
            color=color
        )
        self._threads[tid] = thread
        return thread

    def update(self, thread_id: str, data: Dict[str, Any]) -> Thread:
        thread = self.get_by_id(thread_id)
        if not thread:
            raise KeyError(f"Thread '{thread_id}' not found")

        if "name" in data and data["name"]:
            thread.name = str(data["name"]).strip()
        if "arrival_time" in data:
            arr = int(data["arrival_time"])
            if arr < 0:
                raise ValueError("Arrival time cannot be negative")
            thread.arrival_time = arr
        if "burst_time" in data:
            burst = int(data["burst_time"])
            if burst <= 0:
                raise ValueError("Burst time must be greater than zero")
            thread.burst_time = burst
            if thread.state in ("NEW", "READY"):
                thread.remaining_time = burst
        if "priority" in data:
            prio = int(data["priority"])
            if prio < 1:
                raise ValueError("Priority must be 1 or greater (1 = highest priority)")
            thread.priority = prio
        if "state" in data:
            thread.transition_to(data["state"])
        if "color" in data and data["color"]:
            thread.color = data["color"]

        return thread

    def delete(self, thread_id: str) -> bool:
        tid = thread_id.strip().upper()
        if tid in self._threads:
            del self._threads[tid]
            return True
        return False

    def clear_all(self):
        self._threads.clear()

    def get_stats(self) -> Dict[str, int]:
        threads = list(self._threads.values())
        return {
            "total": len(threads),
            "running": sum(1 for t in threads if t.state == "RUNNING"),
            "ready": sum(1 for t in threads if t.state == "READY"),
            "blocked": sum(1 for t in threads if t.state == "BLOCKED"),
            "terminated": sum(1 for t in threads if t.state == "TERMINATED"),
        }


# Global singleton instance
thread_manager_instance = ThreadManager()
