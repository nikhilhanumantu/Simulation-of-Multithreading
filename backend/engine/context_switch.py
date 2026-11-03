"""
Context Switching Engine for ThreadLab.
Simulates CPU register saving, PCB/TCB updates, scheduler dispatch, and context restoration.
"""
from typing import Dict, Any, List


class ContextSwitchSimulator:
    def __init__(self):
        # Simulated CPU registers for Thread 1 and Thread 2
        self.t1_context = {
            "thread_id": "T1",
            "name": "Worker-Compute",
            "pc": "0x00401A20",
            "sp": "0x7FFF08C0",
            "ax": "0x00000042",
            "bx": "0x00001000",
            "cx": "0x00000008",
            "dx": "0x7FFF0040",
            "flags": "ZF=0, CF=0, SF=0",
            "state": "RUNNING"
        }

        self.t2_context = {
            "thread_id": "T2",
            "name": "Renderer-Sync",
            "pc": "0x00402F80",
            "sp": "0x7FFF09E0",
            "ax": "0x000000FA",
            "bx": "0x00002040",
            "cx": "0x00000002",
            "dx": "0x7FFF0058",
            "flags": "ZF=1, CF=0, SF=0",
            "state": "READY"
        }

        self.active_cpu_registers = dict(self.t1_context)
        self.total_switches = 1420
        self.switch_latency_us = 1.82
        self.overhead_penalty_pct = 4.2

    def get_simulation_state(self, step: int = 1) -> Dict[str, Any]:
        """
        Returns full hardware registers and explanation for the chosen phase (1-4).
        """
        step = max(1, min(step, 4))
        phases = {
            1: {
                "step": 1,
                "name": "1. Interrupt / Syscall",
                "phase_category": "Trigger Phase",
                "active_thread": "T1",
                "target_thread": "T2",
                "cpu_mode": "USER -> KERNEL",
                "description": "Hardware timer interrupt fires (Quantum expired). CPU transfers control to Kernel interrupt handler via IDT.",
                "registers": self.t1_context,
                "tcb_status": "Active CPU registers still reflect Thread 1 in User mode."
            },
            2: {
                "step": 2,
                "name": "2. Save T1 State",
                "phase_category": "Kernel Mode",
                "active_thread": "T1",
                "target_thread": "T2",
                "cpu_mode": "KERNEL MODE",
                "description": "Kernel pushes T1's Program Counter, Stack Pointer, and General Purpose Registers (AX, BX, CX, DX) into T1's Thread Control Block (TCB).",
                "registers": self.t1_context,
                "tcb_status": "T1 TCB updated. State set to READY."
            },
            3: {
                "step": 3,
                "name": "3. Select Next Thread",
                "phase_category": "Scheduler Core",
                "active_thread": "KERNEL SCHEDULER",
                "target_thread": "T2",
                "cpu_mode": "KERNEL MODE",
                "description": "Scheduler algorithm (Round Robin) queries ready queue, preempts T1, and selects T2 as next thread to execute.",
                "registers": {
                    "thread_id": "OS_KERNEL",
                    "name": "Scheduler",
                    "pc": "0xFFFFF800",
                    "sp": "0xFFFFF900",
                    "ax": "0x00000000",
                    "bx": "0x00000000",
                    "cx": "0x00000000",
                    "dx": "0x00000000",
                    "flags": "INTERRUPTS_DISABLED",
                    "state": "DISPATCHING"
                },
                "tcb_status": "Ready queue updated: T1 placed at tail, T2 popped from head."
            },
            4: {
                "step": 4,
                "name": "4. Restore T2 Context",
                "phase_category": "Restore Stage",
                "active_thread": "T2",
                "target_thread": "T2",
                "cpu_mode": "KERNEL -> USER",
                "description": "Registers loaded from T2's TCB into CPU registers. Program Counter set to 0x00402F80. T2 resumes seamlessly.",
                "registers": self.t2_context,
                "tcb_status": "T2 TCB state set to RUNNING. Switch complete."
            }
        }

        phase_data = phases[step]
        phase_data.update({
            "t1": self.t1_context,
            "t2": self.t2_context,
            "latency": f"{self.switch_latency_us} µs",
            "total_switches": self.total_switches,
            "overhead_penalty": f"{self.overhead_penalty_pct}% Waste"
        })
        return phase_data

