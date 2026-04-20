// Theme Toggle
// Respects system preference with manual override stored in localStorage
(function() {
  const STORAGE_KEY = 'theme';

  function getSystemTheme() {
    return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  }

  function getStoredTheme() {
    try {
      return localStorage.getItem(STORAGE_KEY);
    } catch {
      return null;
    }
  }

  function setTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    try {
      localStorage.setItem(STORAGE_KEY, theme);
    } catch {
      // localStorage unavailable
    }
  }

  function initTheme() {
    const stored = getStoredTheme();
    const theme = stored || getSystemTheme();
    document.documentElement.setAttribute('data-theme', theme);
  }

  // Set theme immediately to prevent flash
  initTheme();

  // Listen for system theme changes
  window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
    // Only auto-switch if user hasn't manually set a preference
    if (!getStoredTheme()) {
      document.documentElement.setAttribute('data-theme', e.matches ? 'dark' : 'light');
    }
  });

  // Toggle button handler
  document.addEventListener('DOMContentLoaded', () => {
    const toggle = document.querySelector('.theme-toggle');
    if (toggle) {
      toggle.addEventListener('click', () => {
        const current = document.documentElement.getAttribute('data-theme');
        const next = current === 'dark' ? 'light' : 'dark';
        setTheme(next);
      });
    }
  });
})();

// Keyboard navigation detection
document.addEventListener('keydown', (e) => {
  if (e.key === 'Tab') document.body.classList.add('using-keyboard');
});
document.addEventListener('mousedown', () => {
  document.body.classList.remove('using-keyboard');
});

// Post filtering
document.addEventListener('DOMContentLoaded', () => {
  const filters = document.querySelectorAll('.filter-btn');
  const posts = document.querySelectorAll('.post-item[data-type]');
  const yearGroups = document.querySelectorAll('.year-group');

  if (filters.length === 0) return;

  filters.forEach(btn => {
    btn.addEventListener('click', () => {
      const filter = btn.dataset.filter;

      // Update active state
      filters.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');

      // Filter posts
      posts.forEach(post => {
        if (filter === 'all' || post.dataset.type === filter) {
          post.style.display = '';
        } else {
          post.style.display = 'none';
        }
      });

      // Hide empty year groups
      yearGroups.forEach(group => {
        const visiblePosts = group.querySelectorAll('.post-item[data-type]:not([style*="display: none"])');
        group.style.display = visiblePosts.length > 0 ? '' : 'none';
      });

      // Update URL without reload
      const url = new URL(window.location);
      if (filter === 'all') {
        url.searchParams.delete('type');
      } else {
        url.searchParams.set('type', filter);
      }
      history.replaceState({}, '', url);
    });
  });

  // Apply filter from URL on load
  const urlParams = new URLSearchParams(window.location.search);
  const typeParam = urlParams.get('type');
  if (typeParam) {
    const matchingBtn = document.querySelector(`.filter-btn[data-filter="${typeParam}"]`);
    if (matchingBtn) {
      matchingBtn.click();
    }
  }
});
