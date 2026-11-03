/**
 * ThreadLab Unified Navigation & Application Shell Script.
 * Manages sidebar, header, active navigation states, and mobile responsive behavior.
 * Simplified to the 7 core pillars:
 * 1. Dashboard
 * 2. Thread Manager
 * 3. CPU Scheduler (with integrated Context Switching panel)
 * 4. Thread Lifecycle
 * 5. Synchronization Lab
 * 6. Deadlock Lab
 * 7. Analytics
 */

(function initNavigation() {
  function getPageKey() {
    const path = window.location.pathname.toLowerCase();
    if (path.includes('thread-manager') || path.includes('threads')) return 'thread-manager';
    if (path.includes('cpu-scheduling') || path.includes('scheduling') || path.includes('scheduler')) return 'cpu-scheduling';
    if (path.includes('thread-lifecycle') || path.includes('lifecycle')) return 'thread-lifecycle';
    if (path.includes('synchronization') || path.includes('sync')) return 'synchronization';
    if (path.includes('deadlock')) return 'deadlock';
    if (path.includes('context-switching') || path.includes('context')) return 'cpu-scheduling';
    if (path.includes('analytics') || path.includes('performance')) return 'analytics';
    if (path.includes('learning')) return 'learning';
    if (path.includes('login')) return 'login';
    if (path.includes('index') || path === '/' || path.includes('landing')) return 'dashboard';
    return 'dashboard';
  }

  function resolveHref(targetPath) {
    const isServed = window.location.protocol.startsWith('http');
    if (isServed) {
      if (targetPath === 'context-switching') return '/cpu-scheduling?tab=context-switch';
      if (targetPath === 'synchronization-lab') return '/synchronization';
      if (targetPath === 'deadlock-lab') return '/deadlock';
      if (targetPath === 'performance-analytics') return '/analytics';
      if (targetPath === 'learning-mode') return '/learning';
      return `/${targetPath}`;
    } else {
      // Local file system fallback
      const inPagesDir = window.location.pathname.includes('/pages/');
      const prefix = inPagesDir ? '' : 'pages/';
      const fileMap = {
        'dashboard': 'dashboard.html',
        'thread-manager': 'thread-manager.html',
        'cpu-scheduling': 'cpu-scheduling.html',
        'thread-lifecycle': 'thread-lifecycle.html',
        'synchronization': 'synchronization.html',
        'synchronization-lab': 'synchronization.html',
        'deadlock': 'deadlock.html',
        'deadlock-lab': 'deadlock.html',
        'context-switching': 'cpu-scheduling.html',
        'analytics': 'analytics.html',
        'performance-analytics': 'analytics.html',
        'learning': 'learning.html',
        'learning-mode': 'learning.html',
      };
      return prefix + (fileMap[targetPath] || `${targetPath}.html`);
    }
  }

  document.addEventListener('DOMContentLoaded', () => {
    const currentKey = getPageKey();
    const navLinks = document.querySelectorAll('aside nav a[data-path]');

    navLinks.forEach(link => {
      let path = link.getAttribute('data-path');
      if (path === 'synchronization-lab') path = 'synchronization';
      if (path === 'deadlock-lab') path = 'deadlock';
      if (path === 'performance-analytics') path = 'analytics';

      link.href = resolveHref(path);

      if (path === currentKey) {
        link.className = "flex items-center gap-space-sm px-space-md py-2 rounded-xl transition-all bg-gradient-to-r from-primary-container to-secondary text-on-primary shadow-[0_4px_12px_rgba(37,99,235,0.25)] font-semibold";
        link.setAttribute('aria-current', 'page');
        const icon = link.querySelector('.material-symbols-outlined');
        if (icon) {
          icon.style.color = '#ffffff';
        }
      } else {
        link.className = "flex items-center gap-space-sm px-space-md py-2 rounded-xl text-on-surface-variant hover:bg-surface-container-low hover:text-primary transition-all";
        link.removeAttribute('aria-current');
      }
    });

    // Top Search input shortcuts (Ctrl+K / Cmd+K)
    const searchInputs = document.querySelectorAll('header input[type="text"]');
    document.addEventListener('keydown', (e) => {
      if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') {
        e.preventDefault();
        if (searchInputs.length > 0) searchInputs[0].focus();
      }
    });

    searchInputs.forEach(input => {
      input.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
          handleSearchQuery(input.value.trim());
        }
      });
    });
  });

  function handleSearchQuery(query) {
    if (!query) return;
    const q = query.toLowerCase();
    if (q.includes('sched') || q.includes('fcfs') || q.includes('sjf') || q.includes('round') || q.includes('rr')) {
      window.location.href = resolveHref('cpu-scheduling');
    } else if (q.includes('context') || q.includes('switch') || q.includes('register') || q.includes('tcb')) {
      window.location.href = resolveHref('context-switching');
    } else if (q.includes('thread') || q.includes('burst')) {
      window.location.href = resolveHref('thread-manager');
    } else if (q.includes('sync') || q.includes('race') || q.includes('mutex') || q.includes('sem') || q.includes('consumer')) {
      window.location.href = resolveHref('synchronization');
    } else if (q.includes('deadlock') || q.includes('banker') || q.includes('rag') || q.includes('cycle')) {
      window.location.href = resolveHref('deadlock');
    } else if (q.includes('lifecycle') || q.includes('state') || q.includes('ready') || q.includes('blocked')) {
      window.location.href = resolveHref('thread-lifecycle');
    } else if (q.includes('analytic') || q.includes('metric') || q.includes('compare') || q.includes('utilization')) {
      window.location.href = resolveHref('analytics');
    }
  }

  // Toast Notification helper
  window.showToast = function(message, type = 'info') {
    let container = document.getElementById('toast-container');
    if (!container) {
      container = document.createElement('div');
      container.id = 'toast-container';
      container.className = 'fixed bottom-5 right-5 z-50 flex flex-col gap-2 pointer-events-none';
      document.body.appendChild(container);
    }
    const toast = document.createElement('div');
    const bg = type === 'success' ? 'bg-emerald-600 text-white' : (type === 'error' ? 'bg-rose-600 text-white' : 'bg-slate-800 text-white');
    const icon = type === 'success' ? 'check_circle' : (type === 'error' ? 'error' : 'info');
    toast.className = `${bg} px-4 py-2.5 rounded-xl shadow-lg flex items-center gap-2 text-xs font-semibold pointer-events-auto transform transition-all duration-300 translate-y-2 opacity-0`;
    toast.innerHTML = `<span class="material-symbols-outlined text-[18px]">${icon}</span><span>${message}</span>`;
    container.appendChild(toast);
    setTimeout(() => {
      toast.classList.remove('translate-y-2', 'opacity-0');
    }, 10);
    setTimeout(() => {
      toast.classList.add('opacity-0', 'translate-y-2');
      setTimeout(() => toast.remove(), 300);
    }, 3200);
  };
})();
