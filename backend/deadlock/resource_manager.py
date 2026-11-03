"""
Resource Manager for Deadlock Lab.
Maintains Resource Allocation Graph (RAG) state: thread nodes, resource nodes,
allocation edges (Resource -> Thread), and request edges (Thread -> Resource).
"""
from typing import Dict, List, Any


class ResourceManager:
    def __init__(self):
        # Default scenario matching Deadlock demonstration:
        # T1 holds R1, requests R2
        # T2 holds R2, requests R1
        # -> Circular Wait / Deadlock!
        self.threads = ["T1", "T2"]
        self.resources = ["R1", "R2"]
        self.allocations: Dict[str, str] = {"R1": "T1", "R2": "T2"}  # Resource -> Thread
        self.requests: Dict[str, str] = {"T1": "R2", "T2": "R1"}      # Thread -> Resource

    def get_graph_state(self) -> Dict[str, Any]:
        return {
            "threads": list(self.threads),
            "resources": list(self.resources),
            "allocations": dict(self.allocations),
            "requests": dict(self.requests),
            "edges": [
                {"from": r, "to": t, "type": "allocation", "label": f"{r} allocated to {t}"}
                for r, t in self.allocations.items()
            ] + [
                {"from": t, "to": r, "type": "request", "label": f"{t} waiting for {r}"}
                for t, r in self.requests.items()
            ]
        }

    def allocate(self, resource: str, thread: str):
        if resource in self.resources and thread in self.threads:
            self.allocations[resource] = thread
            if self.requests.get(thread) == resource:
                del self.requests[thread]

    def request(self, thread: str, resource: str):
        if thread in self.threads and resource in self.resources:
            self.requests[thread] = resource

    def release(self, resource: str):
        if resource in self.allocations:
            del self.allocations[resource]

    def terminate_thread(self, thread: str) -> List[str]:
        """Terminates thread and releases all its held resources."""
        freed = []
        for r, t in list(self.allocations.items()):
            if t == thread:
                del self.allocations[r]
                freed.append(r)
        if thread in self.requests:
            del self.requests[thread]
        return freed

