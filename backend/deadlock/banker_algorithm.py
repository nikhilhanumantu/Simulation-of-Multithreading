"""
Banker's Algorithm for Deadlock Avoidance.
Determines whether a resource allocation leaves the system in a safe state and computes the safe execution sequence.
Includes comprehensive input validation to protect against malformed or out-of-bounds matrices.
"""
from typing import Dict, List, Any


def run_bankers_algorithm(
    available: Any,
    max_matrix: Any,
    allocation_matrix: Any,
    process_names: Any = None
) -> Dict[str, Any]:
    """
    Standard Banker's Algorithm safety check with input validation:
    - Available: vector of length M of available instances of each resource type
    - Max: N x M matrix defining the maximum demand of each process
    - Allocation: N x M matrix defining the number of resources currently allocated to each process
    - Need: Max - Allocation

    Rejects negative values, dimension mismatches, and allocations exceeding maximum demands.
    """
    # Validation
    if not isinstance(available, (list, tuple)) or len(available) == 0:
        raise ValueError("Invalid Available Vector: 'available' must be a non-empty list of integers")

    if not isinstance(max_matrix, (list, tuple)) or len(max_matrix) == 0:
        raise ValueError("Invalid Max Matrix: 'max_matrix' must be a non-empty 2D list of integers")

    if not isinstance(allocation_matrix, (list, tuple)) or len(allocation_matrix) == 0:
        raise ValueError("Invalid Allocation Matrix: 'allocation_matrix' must be a non-empty 2D list of integers")

    num_processes = len(allocation_matrix)
    num_resources = len(available)

    if len(max_matrix) != num_processes:
        raise ValueError(
            f"Dimension Mismatch: 'max_matrix' has {len(max_matrix)} processes, but 'allocation_matrix' has {num_processes}"
        )

    # Validate elements and dimensions
    for j, a in enumerate(available):
        if not isinstance(a, int) or a < 0:
            raise ValueError(f"Invalid Available Resource: Available instance count at index {j} must be a non-negative integer")

    for i in range(num_processes):
        max_row = max_matrix[i]
        alloc_row = allocation_matrix[i]

        if not isinstance(max_row, (list, tuple)) or len(max_row) != num_resources:
            raise ValueError(f"Row Length Mismatch: Max matrix row {i} has {len(max_row)} items, expected {num_resources}")
        if not isinstance(alloc_row, (list, tuple)) or len(alloc_row) != num_resources:
            raise ValueError(f"Row Length Mismatch: Allocation matrix row {i} has {len(alloc_row)} items, expected {num_resources}")

        for j in range(num_resources):
            m_val = max_row[j]
            a_val = alloc_row[j]

            if not isinstance(m_val, int) or m_val < 0:
                raise ValueError(f"Invalid Max Demand: Process {i}, Resource {j} must be a non-negative integer")
            if not isinstance(a_val, int) or a_val < 0:
                raise ValueError(f"Invalid Allocation: Process {i}, Resource {j} must be a non-negative integer")

            if a_val > m_val:
                p_name = process_names[i] if (process_names and i < len(process_names)) else f"P{i}"
                raise ValueError(
                    f"Protocol Violation: Process {p_name} allocation ({a_val}) cannot exceed its maximum claim ({m_val}) for Resource R{j}"
                )

    if not process_names or len(process_names) != num_processes:
        process_names = [f"P{i}" for i in range(num_processes)]

    # Compute Need matrix = Max - Allocation
    need_matrix: List[List[int]] = []
    for i in range(num_processes):
        need_row = []
        for j in range(num_resources):
            need_row.append(max_matrix[i][j] - allocation_matrix[i][j])
        need_matrix.append(need_row)

    work = list(available)
    finish = [False] * num_processes
    safe_sequence: List[str] = []
    step_log: List[Dict[str, Any]] = []

    changed = True
    step_num = 1

    while changed:
        changed = False
        for i in range(num_processes):
            if not finish[i]:
                # Check if Need[i] <= Work
                can_allocate = all(need_matrix[i][j] <= work[j] for j in range(num_resources))
                if can_allocate:
                    # Process can finish and release its allocated resources
                    for j in range(num_resources):
                        work[j] += allocation_matrix[i][j]
                    finish[i] = True
                    safe_sequence.append(process_names[i])
                    changed = True

                    step_log.append({
                        "step": step_num,
                        "process": process_names[i],
                        "need": need_matrix[i],
                        "allocated": allocation_matrix[i],
                        "work_after": list(work),
                        "description": (
                            f"Step {step_num}: Process {process_names[i]} can be satisfied (Need {need_matrix[i]} <= Work). "
                            f"{process_names[i]} finishes and releases allocation {allocation_matrix[i]}. New Available Work: {work}."
                        )
                    })
                    step_num += 1

    is_safe = all(finish)

    return {
        "is_safe": is_safe,
        "safe_sequence": safe_sequence if is_safe else [],
        "steps": step_log,
        "available": available,
        "max_matrix": max_matrix,
        "allocation_matrix": allocation_matrix,
        "need_matrix": need_matrix,
        "process_names": process_names,
        "summary": (
            f"Safe state confirmed! Valid safe execution sequence: {' -> '.join(safe_sequence)}."
            if is_safe
            else "Unsafe state! No safe sequence could be constructed; deadlock may occur if requested resources cannot be reclaimed."
        )
    }
