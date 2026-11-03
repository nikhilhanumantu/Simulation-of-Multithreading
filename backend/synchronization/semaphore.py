"""
Counting and Binary Semaphore Simulator.
Models wait() (P) and signal() (V) operations with permit counting and blocked queues.
"""
from typing import List, Dict, Any


def simulate_semaphore(initial_permits: int = 2, total_threads: int = 4) -> Dict[str, Any]:
    permits = max(1, min(initial_permits, 5))
    thread_ids = [f"T{i+1}" for i in range(max(2, min(total_threads, 6)))]
    
    current_permits = permits
    active_threads: List[str] = []
    wait_queue: List[str] = []
    events: List[Dict[str, Any]] = []
    tick = 0

    events.append({
        "tick": tick,
        "action": "INIT",
        "permits": current_permits,
        "max_permits": permits,
        "active_threads": [],
        "wait_queue": [],
        "description": f"Counting Semaphore initialized with {permits} permits. Capacity: {permits} concurrent threads."
    })

    # Threads arrive and request permits
    for t in thread_ids:
        tick += 1
        if current_permits > 0:
            current_permits -= 1
            active_threads.append(t)
            events.append({
                "tick": tick,
                "action": "WAIT_GRANTED",
                "thread": t,
                "permits": current_permits,
                "max_permits": permits,
                "active_threads": list(active_threads),
                "wait_queue": list(wait_queue),
                "description": f"{t} called wait(S). Permit granted! ({current_permits} permits remaining)."
            })
        else:
            wait_queue.append(t)
            events.append({
                "tick": tick,
                "action": "WAIT_BLOCKED",
                "thread": t,
                "permits": current_permits,
                "max_permits": permits,
                "active_threads": list(active_threads),
                "wait_queue": list(wait_queue),
                "description": f"{t} called wait(S). No permits available (S=0). {t} is BLOCKED."
            })

    # Active threads release permits and wake waiting threads
    while active_threads:
        finishing = active_threads.pop(0)
        tick += 1
        current_permits += 1
        events.append({
            "tick": tick,
            "action": "SIGNAL",
            "thread": finishing,
            "permits": current_permits,
            "max_permits": permits,
            "active_threads": list(active_threads),
            "wait_queue": list(wait_queue),
            "description": f"{finishing} finished and called signal(S). Permit released (S={current_permits})."
        })

        if wait_queue:
            unblocked = wait_queue.pop(0)
            current_permits -= 1
            active_threads.append(unblocked)
            tick += 1
            events.append({
                "tick": tick,
                "action": "WAKE_UP",
                "thread": unblocked,
                "permits": current_permits,
                "max_permits": permits,
                "active_threads": list(active_threads),
                "wait_queue": list(wait_queue),
                "description": f"{unblocked} was awakened from queue and consumed the released permit (S={current_permits})."
            })

    return {
        "initial_permits": permits,
        "total_threads": len(thread_ids),
        "events": events
    }

