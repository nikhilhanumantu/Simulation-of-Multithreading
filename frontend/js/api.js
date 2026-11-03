/**
 * ThreadLab Central API Client.
 * Communicates with the Python Flask simulation engine.
 */
const API_BASE = window.location.origin.includes('http') 
  ? (window.location.origin.includes(':5000') ? window.location.origin : 'http://127.0.0.1:5000')
  : 'http://127.0.0.1:5000';

class ThreadLabAPI {
  static async request(endpoint, options = {}) {
    const url = `${API_BASE}${endpoint}`;
    const defaultHeaders = {
      'Content-Type': 'application/json',
      'Accept': 'application/json'
    };
    try {
      const response = await fetch(url, {
        ...options,
        headers: { ...defaultHeaders, ...options.headers }
      });
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.error || `HTTP ${response.status}: ${response.statusText}`);
      }
      return await response.json();
    } catch (err) {
      console.warn(`[API] Error on ${endpoint}:`, err.message);
      throw err;
    }
  }

  // === THREADS ===
  static async getThreads() {
    return this.request('/api/threads');
  }

  static async createThread(data) {
    return this.request('/api/threads', {
      method: 'POST',
      body: JSON.stringify(data)
    });
  }

  static async updateThread(id, data) {
    return this.request(`/api/threads/${id}`, {
      method: 'PUT',
      body: JSON.stringify(data)
    });
  }

  static async deleteThread(id) {
    return this.request(`/api/threads/${id}`, {
      method: 'DELETE'
    });
  }

  static async clearThreads() {
    return this.request('/api/threads/clear', { method: 'POST' });
  }

  static async loadPresetThreads() {
    return this.request('/api/threads/preset', { method: 'POST' });
  }

  static async getThreadStats() {
    return this.request('/api/threads/stats');
  }

  // === CPU SCHEDULING ===
  static async runScheduling(algorithm = 'Round Robin', timeQuantum = 2, contextSwitchOverhead = 0, threads = null) {
    return this.request('/api/scheduling/run', {
      method: 'POST',
      body: JSON.stringify({
        algorithm,
        time_quantum: timeQuantum,
        context_switch_overhead: contextSwitchOverhead,
        threads
      })
    });
  }

  static async compareScheduling(timeQuantum = 2, contextSwitchOverhead = 0, threads = null) {
    return this.request('/api/scheduling/compare', {
      method: 'POST',
      body: JSON.stringify({
        time_quantum: timeQuantum,
        context_switch_overhead: contextSwitchOverhead,
        threads
      })
    });
  }

  // === SYNCHRONIZATION ===
  static async runRaceCondition(iterations = 1000, withMutex = false, delayMode = 'normal') {
    return this.request('/api/synchronization/race-condition', {
      method: 'POST',
      body: JSON.stringify({
        iterations,
        with_mutex: withMutex,
        delay_mode: delayMode
      })
    });
  }

  static async runMutexDemo(numThreads = 3, workDuration = 2) {
    return this.request('/api/synchronization/mutex', {
      method: 'POST',
      body: JSON.stringify({ num_threads: numThreads, work_duration: workDuration })
    });
  }

  static async runSemaphoreDemo(initialPermits = 2, totalThreads = 4) {
    return this.request('/api/synchronization/semaphore', {
      method: 'POST',
      body: JSON.stringify({ initial_permits: initialPermits, total_threads: totalThreads })
    });
  }

  static async runProducerConsumer(bufferSize = 5, operationsCount = 8) {
    return this.request('/api/synchronization/producer-consumer', {
      method: 'POST',
      body: JSON.stringify({ buffer_size: bufferSize, operations_count: operationsCount })
    });
  }

  // === DEADLOCK ===
  static async getDeadlockGraph() {
    return this.request('/api/deadlock/graph');
  }

  static async detectDeadlock(allocations = null, requests = null) {
    return this.request('/api/deadlock/detect', {
      method: 'POST',
      body: JSON.stringify({ allocations, requests })
    });
  }

  static async runBankers(available = null, maxMatrix = null, allocationMatrix = null, processNames = null) {
    return this.request('/api/deadlock/banker', {
      method: 'POST',
      body: JSON.stringify({
        available,
        max_matrix: maxMatrix,
        allocation_matrix: allocationMatrix,
        process_names: processNames
      })
    });
  }

  static async recoverDeadlock(victimThread = 'T2') {
    return this.request('/api/deadlock/recover', {
      method: 'POST',
      body: JSON.stringify({ victim_thread: victimThread })
    });
  }

  static async resetDeadlockGraph() {
    return this.request('/api/deadlock/reset', { method: 'POST' });
  }

  // === CONTEXT SWITCHING ===
  static async getContextSwitchState(step = 1) {
    return this.request(`/api/context-switching/state?step=${step}`);
  }

  static async stepContextSwitch(step = 1) {
    return this.request('/api/context-switching/step', {
      method: 'POST',
      body: JSON.stringify({ step })
    });
  }

  // === ANALYTICS & SYSTEM ===
  static async getAnalytics(timeQuantum = 2, contextSwitchOverhead = 0) {
    return this.request(`/api/analytics?quantum=${timeQuantum}&overhead=${contextSwitchOverhead}`);
  }

  static async getComparison(timeQuantum = 2, contextSwitchOverhead = 0) {
    return this.request(`/api/analytics/comparison?quantum=${timeQuantum}&overhead=${contextSwitchOverhead}`);
  }

  static async getSystemOverview() {
    return this.request('/api/system/overview');
  }

  static async resetSystem() {
    return this.request('/api/system/reset', { method: 'POST' });
  }
}

// Make globally accessible
window.ThreadLabAPI = ThreadLabAPI;
