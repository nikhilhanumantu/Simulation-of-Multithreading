"""
Producer-Consumer Bounded Buffer Synchronization Simulator.
Uses mutex (binary lock), empty semaphore (counting), and full semaphore (counting).
"""
from typing import List, Dict, Any


def simulate_producer_consumer(buffer_size: int = 5, operations_count: int = 8) -> Dict[str, Any]:
    buf_size = max(3, min(buffer_size, 8))
    ops = max(4, min(operations_count, 15))

    buffer: List[Dict[str, Any]] = []
    mutex = 1
    empty_sem = buf_size
    full_sem = 0
    events: List[Dict[str, Any]] = []
    tick = 0
    item_id_counter = 1

    events.append({
        "tick": tick,
        "action": "INIT",
        "buffer": [],
        "buffer_size": buf_size,
        "mutex": mutex,
        "empty_sem": empty_sem,
        "full_sem": full_sem,
        "description": f"Bounded buffer initialized with {buf_size} slots. Semaphores: Mutex=1, Empty={empty_sem}, Full=0."
    })

    # Sequence of interleaved producer and consumer steps
    action_plan = ["P", "P", "P", "C", "P", "C", "C", "P", "P", "C"][:ops]

    for op in action_plan:
        tick += 1
        if op == "P":  # Producer
            if empty_sem > 0:
                empty_sem -= 1
                mutex = 0  # lock acquired
                item = f"Item-{item_id_counter}"
                item_id_counter += 1
                buffer.append({"id": item, "producer": "Producer-1"})
                mutex = 1  # lock released
                full_sem += 1
                events.append({
                    "tick": tick,
                    "action": "PRODUCE",
                    "actor": "Producer-1",
                    "item": item,
                    "buffer": list(buffer),
                    "buffer_size": buf_size,
                    "mutex": mutex,
                    "empty_sem": empty_sem,
                    "full_sem": full_sem,
                    "description": f"Producer-1 produced {item} into slot {len(buffer)}. Buffer: {len(buffer)}/{buf_size} full."
                })
            else:
                events.append({
                    "tick": tick,
                    "action": "PRODUCER_BLOCKED",
                    "actor": "Producer-1",
                    "item": None,
                    "buffer": list(buffer),
                    "buffer_size": buf_size,
                    "mutex": mutex,
                    "empty_sem": empty_sem,
                    "full_sem": full_sem,
                    "description": "Producer-1 blocked! Buffer is completely full (Empty=0). Waiting for consumer signal."
                })
        else:  # Consumer
            if full_sem > 0:
                full_sem -= 1
                mutex = 0
                consumed_item = buffer.pop(0)
                mutex = 1
                empty_sem += 1
                events.append({
                    "tick": tick,
                    "action": "CONSUME",
                    "actor": "Consumer-1",
                    "item": consumed_item["id"],
                    "buffer": list(buffer),
                    "buffer_size": buf_size,
                    "mutex": mutex,
                    "empty_sem": empty_sem,
                    "full_sem": full_sem,
                    "description": f"Consumer-1 consumed {consumed_item['id']} from buffer. Buffer: {len(buffer)}/{buf_size} full."
                })
            else:
                events.append({
                    "tick": tick,
                    "action": "CONSUMER_BLOCKED",
                    "actor": "Consumer-1",
                    "item": None,
                    "buffer": list(buffer),
                    "buffer_size": buf_size,
                    "mutex": mutex,
                    "empty_sem": empty_sem,
                    "full_sem": full_sem,
                    "description": "Consumer-1 blocked! Buffer is empty (Full=0). Waiting for producer signal."
                })

    return {
        "buffer_size": buf_size,
        "total_operations": len(action_plan),
        "final_buffer": buffer,
        "events": events
    }

