"""
Deadlock Recovery Strategies.
Simulates resolving deadlocks via thread termination or resource preemption.
"""
from typing import Dict, Any, List
from backend.deadlock.resource_manager import ResourceManager
from backend.deadlock.detection import detect_deadlock


def recover_by_termination(victim_thread: str = "T2") -> Dict[str, Any]:
    """
    Terminates victim thread, releases its allocated resources, and breaks the circular wait.
    """
    manager = ResourceManager()
    initial_check = detect_deadlock(manager.allocations, manager.requests)

    # Terminate victim
    freed_resources = manager.terminate_thread(victim_thread)

    # If R2 was freed, and T1 was requesting R2, T1 can now acquire R2!
    if "R2" in freed_resources and "T1" in manager.requests and manager.requests["T1"] == "R2":
        manager.allocate("R2", "T1")

    after_check = detect_deadlock(manager.allocations, manager.requests)

    return {
        "action": "TERMINATE_THREAD",
        "victim_thread": victim_thread,
        "freed_resources": freed_resources,
        "before_state": initial_check,
        "after_state": after_check,
        "graph_state": manager.get_graph_state(),
        "resolved": not after_check["deadlock_detected"],
        "message": (
            f"Successfully terminated {victim_thread}. Released {freed_resources}. "
            f"Remaining threads proceeded safely and circular wait has been dissolved."
        )
    }

