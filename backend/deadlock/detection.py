"""
Deadlock Detection Engine.
Finds circular dependencies in Resource Allocation Graphs and Wait-For Graphs with input validation.
"""
from typing import Dict, List, Any, Optional, Set


def detect_deadlock(allocations: Any, requests: Any) -> Dict[str, Any]:
    """
    Constructs the bipartite directed graph:
    - Allocation: Resource R -> Thread T (Resource held by Thread)
    - Request: Thread T -> Resource R (Thread waiting for Resource)

    Performs strict validation on allocations and requests to prevent runtime crashes.
    Runs Depth First Search to detect directed cycles (circular wait).
    """
    # Validation
    if allocations is None:
        allocations = {}
    if requests is None:
        requests = {}

    if not isinstance(allocations, dict):
        raise ValueError("Invalid format: 'allocations' must be a dictionary mapping resources to threads")
    if not isinstance(requests, dict):
        raise ValueError("Invalid format: 'requests' must be a dictionary mapping threads to resources")

    # Sanitize and filter empty/null entries
    clean_alloc: Dict[str, str] = {}
    for r, t in allocations.items():
        if r is not None and t is not None:
            r_str = str(r).strip()
            t_str = str(t).strip()
            if r_str and t_str:
                clean_alloc[r_str] = t_str

    clean_req: Dict[str, str] = {}
    for t, r in requests.items():
        if t is not None and r is not None:
            t_str = str(t).strip()
            r_str = str(r).strip()
            if t_str and r_str:
                clean_req[t_str] = r_str

    adj: Dict[str, List[str]] = {}
    all_nodes: Set[str] = set()

    for r, t in clean_alloc.items():
        all_nodes.add(r)
        all_nodes.add(t)
        adj.setdefault(r, []).append(t)

    for t, r in clean_req.items():
        all_nodes.add(t)
        all_nodes.add(r)
        adj.setdefault(t, []).append(r)

    # DFS cycle detection
    visited: Set[str] = set()
    rec_stack: Set[str] = set()
    parent: Dict[str, Optional[str]] = {}
    cycle_path: List[str] = []

    def dfs(node: str, path: List[str]) -> bool:
        visited.add(node)
        rec_stack.add(node)
        path.append(node)

        for neighbor in adj.get(node, []):
            if neighbor not in visited:
                parent[neighbor] = node
                if dfs(neighbor, path):
                    return True
            elif neighbor in rec_stack:
                # Cycle found!
                idx = path.index(neighbor)
                cycle_path.extend(path[idx:] + [neighbor])
                return True

        path.pop()
        rec_stack.remove(node)
        return False

    has_deadlock = False
    for node in sorted(all_nodes):
        if node not in visited:
            if dfs(node, []):
                has_deadlock = True
                break

    deadlocked_threads = [n for n in cycle_path if n.startswith("T")]
    deadlocked_resources = [n for n in cycle_path if n.startswith("R")]

    if has_deadlock:
        cycle_str = " -> ".join(cycle_path)
        explanation = (
            f"Circular Wait detected along cycle: {cycle_str}. "
            f"Active threads hold assigned resources while waiting for other held resources. "
            f"None of these threads can proceed without preemption or external intervention."
        )
    else:
        explanation = "No circular wait detected. The system is in a safe/non-deadlocked state."

    return {
        "deadlock_detected": has_deadlock,
        "cycle_found": has_deadlock,
        "cycle_path": cycle_path,
        "deadlocked_threads": list(dict.fromkeys(deadlocked_threads)),
        "deadlocked_resources": list(dict.fromkeys(deadlocked_resources)),
        "explanation": explanation,
        "severity": "CRITICAL" if has_deadlock else "NORMAL"
    }
