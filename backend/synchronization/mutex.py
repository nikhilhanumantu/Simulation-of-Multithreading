"""
Mutex Lock Demonstration.
Visualizes mutual exclusion, critical section locking, and waiting thread queues.
"""
from typing import List, Dict, Any


def simulate_mutex_competition(num_threads: int = 3, work_duration: int = 2) -> Dict[str, Any]:
    """
    Simulates threads competing for a single Mutex (M1).
    Generates step-by-step timeline of lock requests, acquisition, critical section execution,
    and release.
    """
    events: List[Dict[str, Any]] = []
    threads = [f"T{i+1}" for i in range(max(2, min(num_threads, 5)))]
    
    lock_owner = None
    wait_queue: List[str] = []
    time_tick = 0

    # Step 1: Initial state
    events.append({
        "tick": time_tick,
        "action": "INIT",
        "lock_state": "UNLOCKED",
        "lock_owner": None,
        "critical_section": None,
        "wait_queue": [],
        "description": "Mutex M1 initialized to UNLOCKED (0). All threads in READY state."
    })

    # Step 2: T1 arrives and acquires lock
    time_tick += 1
    lock_owner = "T1"
    events.append({
        "tick": time_tick,
        "action": "ACQUIRE",
        "thread": "T1",
        "lock_state": "LOCKED",
        "lock_owner": "T1",
        "critical_section": "T1 (Writing to shared memory)",
        "wait_queue": [],
        "description": "T1 requested Mutex M1. Mutex is free; T1 acquired lock and entered Critical Section."
    })

    # Step 3: T2 and T3 try to acquire lock while T1 is inside
    for t in threads[1:]:
        time_tick += 1
        wait_queue.append(t)
        events.append({
            "tick": time_tick,
            "action": "BLOCK",
            "thread": t,
            "lock_state": "LOCKED",
            "lock_owner": lock_owner,
            "critical_section": f"{lock_owner} (in progress)",
            "wait_queue": list(wait_queue),
            "description": f"{t} attempted to acquire M1, but M1 is held by {lock_owner}. {t} is BLOCKED and queued."
        })

    # Step 4: T1 completes work and releases lock
    time_tick += work_duration
    events.append({
        "tick": time_tick,
        "action": "RELEASE",
        "thread": "T1",
        "lock_state": "UNLOCKED",
        "lock_owner": None,
        "critical_section": None,
        "wait_queue": list(wait_queue),
        "description": "T1 finished critical section work and called mutex_unlock(M1)."
    })

    # Step 5: Next waiting thread (T2) unblocks and acquires lock
    while wait_queue:
        next_t = wait_queue.pop(0)
        time_tick += 1
        lock_owner = next_t
        events.append({
            "tick": time_tick,
            "action": "UNBLOCK_ACQUIRE",
            "thread": next_t,
            "lock_state": "LOCKED",
            "lock_owner": next_t,
            "critical_section": f"{next_t} (active)",
            "wait_queue": list(wait_queue),
            "description": f"{next_t} was awakened from wait queue, acquired M1, and entered Critical Section."
        })
        time_tick += work_duration
        events.append({
            "tick": time_tick,
            "action": "RELEASE",
            "thread": next_t,
            "lock_state": "UNLOCKED",
            "lock_owner": None,
            "critical_section": None,
            "wait_queue": list(wait_queue),
            "description": f"{next_t} finished and called mutex_unlock(M1)."
        })

    return {
        "mutex_id": "M1",
        "total_ticks": time_tick,
        "total_threads": len(threads),
        "events": events
    }

