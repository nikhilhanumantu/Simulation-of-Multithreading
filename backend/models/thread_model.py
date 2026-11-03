"""
Thread Model for ThreadLab Simulation Engine.
Represents an operating system thread with execution telemetry, state, and scheduling attributes.
"""
from dataclasses import dataclass, field, asdict
from typing import Optional, List, Dict, Any


VALID_STATES = {"NEW", "READY", "RUNNING", "BLOCKED", "TERMINATED"}

# Standard color palette for thread visualization
THREAD_PALETTE = [
    "#2563EB",  # T1 - Primary Blue
    "#10B981",  # T2 - Emerald Green
    "#F59E0B",  # T3 - Amber Warning
    "#8B5CF6",  # T4 - Accent Violet
    "#EC4899",  # T5 - Pink
    "#06B6D4",  # T6 - Cyan
    "#6366F1",  # T7 - Indigo
    "#14B8A6",  # T8 - Teal
]


@dataclass
class Thread:
    id: str
    arrival_time: int = 0
    burst_time: int = 4
    priority: int = 1  # 1 is highest priority
    remaining_time: int = 4
    state: str = "NEW"
    name: str = ""
    color: str = ""
    
    # Execution telemetry
    start_time: Optional[int] = None
    first_response_time: Optional[int] = None
    completion_time: Optional[int] = None
    waiting_time: int = 0
    turnaround_time: int = 0
    response_time: int = 0
    execution_intervals: List[Dict[str, int]] = field(default_factory=list)

    def __post_init__(self):
        if not self.name:
            self.name = f"Thread-{self.id}"
        if not self.color:
            try:
                num = int("".join(filter(str.isdigit, self.id)))
                self.color = THREAD_PALETTE[(num - 1) % len(THREAD_PALETTE)]
            except Exception:
                self.color = THREAD_PALETTE[0]
        if self.remaining_time is None:
            self.remaining_time = self.burst_time
        if self.state not in VALID_STATES:
            self.state = "NEW"

    def transition_to(self, new_state: str) -> bool:
        """Validate and apply state transitions according to OS lifecycle rules."""
        if new_state not in VALID_STATES:
            raise ValueError(f"Invalid state: {new_state}")
        
        # Legal transitions
        allowed = {
            "NEW": {"READY"},
            "READY": {"RUNNING"},
            "RUNNING": {"READY", "BLOCKED", "TERMINATED"},
            "BLOCKED": {"READY"},
            "TERMINATED": set(),
        }
        
        # Allow force transition during reset/load
        self.state = new_state
        return True

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Thread":
        clean = {k: v for k, v in data.items() if k in cls.__dataclass_fields__}
        return cls(**clean)

