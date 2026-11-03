# 🧵 ThreadLab – Simulation of Multithreading

> **Individual Operating Systems Project**  
> An advanced, interactive, full-stack Operating Systems simulation platform into a production-grade educational environment.


## 🌟 Executive Summary

**ThreadLab** is a comprehensive multithreading and operating systems simulation platform. It models core OS primitives including thread state machines, CPU scheduling algorithms, race conditions, mutual exclusion locks, counting semaphores, deadlock graphs, and hardware context switching overhead with architectural fidelity.

### Design System Integrity
All screens strictly implement a modern, cohesive design language:
- **Theme**:light mode (`#F7F9FF` canvas, `#FFFFFF` surface cards, soft ambient blue/violet drop shadows).
- **Typography**: Inter (UI / Display) and JetBrains Mono (registers, assembly, telemetry metrics).
- **Iconography**: Material Symbols Outlined.
- **Frontend Framework**: HTML5, Tailwind CSS (via CDN), and Vanilla JavaScript (zero React/framework overhead).
- **Backend Architecture**: Python + Flask REST APIs, modular deterministic scheduling algorithms, and simulated register banks.

---

## 🏛 Architecture & Simplified 7-Pillar Navigation

The application simplifies the navigation structure into **7 core pedagogical pillars** with unified routing, while maintaining dedicated deep-dive modes:

1. **Dashboard** (`/dashboard`): Real-time telemetry, thread state counts, live CPU utilization gauge, and active simulation status.
2. **Thread Manager** (`/thread-manager` or `/threads`): Thread pool CRUD, arrival/burst/priority controls, presets, JSON import/export.
3. **CPU Scheduling** (`/cpu-scheduling` or `/scheduler`): FCFS, SJF, Priority, and Round Robin with interactive Gantt timeline, playback controls, and embedded hardware Context Switch execution inspector (4-phase stepper & register banks).
4. **Thread Lifecycle** (`/thread-lifecycle` or `/lifecycle`): 5-state state machine (`NEW`, `READY`, `RUNNING`, `BLOCKED`, `TERMINATED`) with step-by-step transition playback.
5. **Synchronization Lab** (`/synchronization` or `/synchronization-lab`): Hardware-accurate race conditions, binary mutex locks, counting semaphores, and producer-consumer bounded buffers.
6. **Deadlock Lab** (`/deadlock` or `/deadlock-lab`): Resource Allocation Graph (RAG), DFS cycle detection, Banker's safety algorithm, and victim-thread recovery.
7. **Performance Analytics** (`/analytics` or `/performance-analytics`): Multi-algorithm benchmark comparison on identical workloads, normalized metric charts, and CSV report export.

```
OS_Project/
├── frontend/                      # Complete integrated frontend application
│   ├── index.html                 # Hero Landing Page with interactive feature tours
│   ├── pages/
│   │   ├── login.html             # Authentication & user profile entry
│   │   ├── dashboard.html         # Live telemetry & KPI overview
│   │   ├── thread-manager.html    # Thread CRUD, affinity, memory footprint, import/export
│   │   ├── cpu-scheduling.html    # Scheduling algorithms, interactive Gantt & Context Switch panel
│   │   ├── thread-lifecycle.html  # Interactive State Machine (New, Ready, Running, Blocked, Terminated)
│   │   ├── synchronization.html   # Race Condition, Mutex Lock, Semaphore, Producer-Consumer
│   │   ├── deadlock.html          # Resource Allocation Graph (RAG), Banker's Algorithm, Recovery
│   │   ├── context-switching.html # 4-Phase Stepper, Register Banks, Timeline Gap Analysis
│   │   ├── analytics.html         # Comparative Bar Charts, CPU Saturation Donut, Scorecard
│   │   └── learning.html          # Pedagogical Mode with animated theory & quizzes
│   ├── js/
│   │   ├── api.js                 # Unified REST client with fallback resiliency
│   │   └── navigation.js          # Shared sidebar, search shortcuts (⌘K), 7-pillar navigation
│   ├── assets/
│   │   └── screenshots/           # UI screen reference captures
│   └── docs/
│       └── DESIGN.md              # Design system tokens & specification
│
├── backend/                       # Python Flask REST API & Simulation Engine
│   ├── app.py                     # Flask factory serving APIs, aliases, and frontend static files
│   ├── config.py                  # Environment settings & directory mappings
│   ├── models/
│   │   ├── thread_model.py        # Thread dataclass & state machine definitions
│   │   └── simulation_model.py    # GanttSegment & SchedulingResult dataclasses (dual-key support)
│   ├── engine/
│   │   ├── thread_manager.py      # Thread pool manager with strict validation & presets
│   │   └── context_switch.py     # 4-Phase hardware context switcher & register dumps
│   ├── scheduling/
│   │   ├── fcfs.py                # First-Come First-Served scheduling
│   │   ├── sjf.py                 # Shortest Job First scheduling
│   │   ├── priority.py            # Priority scheduling (Priority 1 = Highest)
│   │   ├── round_robin.py         # Preemptive Round Robin with Quantum & Switch Overhead
│   │   └── scheduler.py           # Unified dispatcher & comparative benchmark runner
│   ├── synchronization/
│   │   ├── race_condition.py      # Dual-thread counter race emulator & lost write tracker
│   │   ├── mutex.py               # Binary mutex lock & blocked queue simulator
│   │   ├── semaphore.py           # Counting semaphore permit manager & wait queue
│   │   └── producer_consumer.py   # Bounded buffer synchronization with 3 semaphores
│   ├── deadlock/
│   │   ├── resource_manager.py    # Resource Allocation Graph (RAG) bipartite state
│   │   ├── detection.py           # DFS cycle detection finding exact circular paths
│   │   ├── banker_algorithm.py    # Banker's Safety Algorithm & strict matrix validation
│   │   └── recovery.py            # Process termination & resource reclamation
│   ├── analytics/
│   │   └── metrics.py             # TAT, WT, RT, Throughput, and CPU utilization formulas
│   └── routes/                    # Flask REST API Blueprints
│       ├── thread_routes.py       # /api/threads CRUD & presets
│       ├── scheduling_routes.py   # /api/scheduling execution & comparisons
│       ├── synchronization_routes.py # /api/synchronization race & primitives
│       ├── deadlock_routes.py     # /api/deadlock detection & Banker's validation
│       ├── context_routes.py      # /api/context-switch stepper & hardware registers
│       ├── analytics_routes.py    # /api/analytics benchmark reports
│       └── system_routes.py       # /api/system dynamic overview & live telemetry
│
├── tests/                         # Complete automated test suite (Pytest)
│   ├── test_scheduling.py         # Scheduling correctness & mathematical formula verification
│   ├── test_synchronization.py    # Race condition, mutex, semaphore, and buffer tests
│   ├── test_deadlock.py           # RAG cycles, Banker's validation, recovery tests
│   ├── test_api.py                # REST endpoints, input rejection (400), data contract checks
│   └── test_all_pages.py          # E2E tests verifying all 16 page routes & aliases
│
├── run.py                         # Single-command server launcher
├── requirements.txt               # Python package dependencies
└── README.md                      # Documentation
```

---

## 🚀 Key Modules & Simulation Features

### 1. Dashboard
- **Live Statistics**: Displays real-time counts for Total, Running, Ready, Blocked, and Terminated threads.
- **CPU Utilization Gauge**: SVG radial meter dynamically showing processor load.
- **Current Simulation Card**: Live status of active scheduling algorithm, quantum, and execution progress.
- **Quick Action Bar**: One-click actions to initialize simulations, load presets, reset state, and view analytics.

### 2. Thread Manager
- **Full CRUD Support**: Add custom threads with ID, Arrival Time, Burst Time, and Priority (1 = Highest).
- **Advanced Attributes**: CPU Core Affinity (Any, Core 0, Core 1), Memory Stack Footprint (16KB to 2MB).
- **Import & Export**: Export thread configurations as JSON and import existing workload profiles.
- **Batch Controls**: Quick presets (Balanced, CPU-Bound, I/O-Bound, Priority Stress) and Clear All.

### 3. CPU Scheduling Engine & Interactive Gantt Chart
- **Algorithms**: FCFS, SJF (Non-preemptive), Priority (1 = Highest), and Preemptive Round Robin.
- **Customizable Parameters**: Dynamic Time Quantum slider (1-10 units) and Context Switch Overhead (0-5 units).
- **Interactive Visual Gantt Chart**: Color-coded segments, idle periods, timeline scrubbing, step-by-step playback, and speed control.
- **Real-Time KPIs**: Average Waiting Time, Average Turnaround Time, Total Duration, and Response Times.

### 4. Thread Lifecycle State Machine
- **Interactive States**: Animated SVG transition graph traversing `NEW` ➔ `READY` ➔ `RUNNING` ➔ `BLOCKED` ➔ `TERMINATED`.
- **Live Thread Inspection**: Step-by-step event simulation (`Start`, `Preempt`, `Block I/O`, `Wakeup`, `Terminate`).
- **Telemetry Stream**: Visual progress bar showing remaining burst units and real-time transition logs.

### 5. Synchronization Lab
- **Race Condition Demo**: Concurrent dual-thread incrementation (`T1` and `T2`) demonstrating lost updates caused by overlapping x86-64 `MOV/ADD/MOV` memory instructions without atomic locks.
- **Interactive Reservoir**: 3D-effect liquid cylinder showing real-time counter accumulation and dropped writes.
- **Binary Mutex**: Strict serialization using `pthread_mutex_lock` semantics preventing lost writes.
- **Counting Semaphores**: Resource pool with interactive `Wait (P)` and `Signal (V)` operations.
- **Producer-Consumer**: Bounded circular buffer coordinated via mutex, empty semaphore, and full semaphore.

### 6. Deadlock Lab
- **Resource Allocation Graph (RAG)**: Bipartite directed graph displaying processes (`T1`, `T2`) and resources (`R1`, `R2`) with allocation and request edges.
- **Cycle Detection**: Real-time Depth-First Search (DFS) detecting circular wait paths (`T1 → R2 → T2 → R1 → T1`).
- **Banker's Algorithm**: Dynamic avoidance calculating safe state execution sequences (`Available ≥ Need`).
- **Deadlock Recovery**: Interactive process termination (`SIGKILL T2`) releasing contested resources to resolve the deadlock.

### 7. Context Switching Simulator
- **4-Phase Hardware Stepper**:
  1. *Interrupt Trigger* (Timer tick / Syscall entering Ring 0).
  2. *Save State* (Pushing PC, SP, and registers into outgoing TCB).
  3. *Scheduler Dispatch* (Round Robin candidate selection).
  4. *Restore State* (Popping registers and returning to User Mode Ring 3 via `iretq`).
- **Register Dump**: Live hex inspector for `PC`, `SP`, `AX`, `BX`, `CX`, `DX`, and `Flags (PSW)`.
- **Overhead Decomposition**: Direct register saving cost vs indirect cache/TLB invalidation penalties.

### 8. Performance Analytics
- **Side-by-Side Bar Charts**: Normalized comparisons for Average Waiting Time and Average Turnaround Time.
- **CPU Core Saturation**: Donut gauge decomposing execution time, context-switch waste, and idle cycles.
- **Throughput & Jitter Sparklines**: Real-time ops/ms trends and scheduling jitter.
- **Comprehensive Scorecard Table**: Filterable matrix with one-click CSV report export.

### 9. Learning Mode
- **Structured Curriculum**: Multithreading basics, Amdahl's Law, Coffman conditions, and hardware registers.
- **Interactive Knowledge Checks**: End-of-module quizzes with instant grading and pedagogical explanations.

---

## 🛠 Getting Started

### Prerequisites
- Python 3.10+ (e.g. `py -3.10` or `python`)
- Modern web browser (Chrome, Edge, Firefox, Safari)

### Installation

1. Open a terminal in the project directory:
   ```powershell
   cd "C:\Users\nikhi\OneDrive\Desktop\OS_Project"
   ```

2. Install dependencies:
   ```powershell
   py -3.10 -m pip install -r requirements.txt
   ```

### Running the Application

Launch the platform with the root launcher:
```powershell
py run.py
```

Open your browser and navigate to:
```
http://127.0.0.1:5000
```

---

## 🧪 Automated Testing

ThreadLab includes a comprehensive test suite covering scheduling correctness, synchronization integrity, deadlock detection, REST API status codes, and frontend asset delivery.

Run the test suite:
```powershell
py -3.10 -m pytest tests/ -v
```

**Test Results**:
```
tests/test_all_pages.py .....              [100% Pass]
tests/test_api.py ..........               [100% Pass]
tests/test_deadlock.py .......             [100% Pass]
tests/test_scheduling.py ........          [100% Pass]
tests/test_synchronization.py .....        [100% Pass]

======================== 35 passed in 0.29s ========================
```

---

## 📡 REST API Reference

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/threads` | Get all active threads in the pool |
| `POST` | `/api/threads` | Create a new thread |
| `DELETE` | `/api/threads/<id>` | Delete a thread |
| `POST` | `/api/threads/presets/<name>` | Load workload preset (`balanced`, `cpu`, `io`, `priority`) |
| `POST` | `/api/scheduling/run` | Execute algorithm (`fcfs`, `sjf`, `priority`, `round_robin`) |
| `GET` | `/api/scheduling/compare` | Run all 4 algorithms on identical thread set |
| `POST` | `/api/synchronization/race-condition` | Simulate concurrent counter race with/without mutex |
| `POST` | `/api/deadlock/detect` | Run DFS cycle search on current RAG |
| `POST` | `/api/deadlock/bankers` | Execute Banker's safety check and find safe sequence |
| `POST` | `/api/deadlock/recover` | Terminate thread and reclaim held resources |
| `POST` | `/api/context-switch/step` | Advance hardware context switch step (1 to 4) |
| `GET` | `/api/analytics` | Fetch normalized comparative scorecard |
| `GET` | `/api/system/overview` | Fetch global telemetry and live stats |

---

## 📄 License & Academic Integrity

Developed for the **Individual Operating Systems Project** (2026). All original design assets, color tokens, and simulation primitives are implemented in accordance with academic engineering requirements.

