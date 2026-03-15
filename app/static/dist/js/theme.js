/**
 * Theme Toggle Functionality using AdminLTE native dark mode
 * Centralized theme management for all templates
 */

// Theme Toggle Functionality using AdminLTE native dark mode
const lightModeBtn = document.getElementById('lightMode');
const darkModeBtn = document.getElementById('darkMode');
const autoModeBtn = document.getElementById('autoMode');
const themeIcon = document.getElementById('themeIcon');
const body = document.body;

// Check for saved theme preference
let currentTheme = localStorage.getItem('theme') || 'dark';

// Apply initial theme
applyTheme(currentTheme);

// If no saved preference and default is dark, ensure dark-mode is applied immediately
if (!localStorage.getItem('theme') && currentTheme === 'dark') {
  body.classList.add('dark-mode');
}

// Light mode click handler
if (lightModeBtn) {
  lightModeBtn.addEventListener('click', function(e) {
    e.preventDefault();
    setTheme('light');
  });
}

// Dark mode click handler
if (darkModeBtn) {
  darkModeBtn.addEventListener('click', function(e) {
    e.preventDefault();
    setTheme('dark');
  });
}

// Auto mode click handler
if (autoModeBtn) {
  autoModeBtn.addEventListener('click', function(e) {
    e.preventDefault();
    setTheme('auto');
  });
}

function setTheme(theme) {
  currentTheme = theme;
  localStorage.setItem('theme', theme);
  applyTheme(theme);
  
  // Show notification
  let themeName = theme === 'auto' ? 'Auto (System)' : theme.charAt(0).toUpperCase() + theme.slice(1) + ' Mode';
  console.log(`Switched to ${themeName}`);
  
  // Update charts for theme compatibility
  setTimeout(() => {
    updateChartsTheme();
  }, 300);
}

function applyTheme(theme) {
  // Remove all theme classes first
  body.classList.remove('dark-mode');
  
  if (theme === 'dark') {
    body.classList.add('dark-mode');
    if (themeIcon) themeIcon.className = 'fa-sharp fa-solid fa-moon-stars';
  } else if (theme === 'light') {
    if (themeIcon) themeIcon.className = 'fa-sharp fa-regular fa-brightness-low';
  } else {
    // Auto mode - check system preference
    if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
      body.classList.add('dark-mode');
      if (themeIcon) themeIcon.className = 'fa-sharp fa-solid fa-moon-stars';
    } else {
      if (themeIcon) themeIcon.className = 'fa-sharp fa-regular fa-brightness-low';
    }
  }
  
  // Update dropdown active state
  updateDropdownActive(theme);
}

function updateDropdownActive(theme) {
  // Remove active classes from all items
  if (lightModeBtn) lightModeBtn.classList.remove('active');
  if (darkModeBtn) darkModeBtn.classList.remove('active');
  if (autoModeBtn) autoModeBtn.classList.remove('active');
  
  // Add active class to current theme
  if (theme === 'light') {
    if (lightModeBtn) lightModeBtn.classList.add('active');
  } else if (theme === 'dark') {
    if (darkModeBtn) darkModeBtn.classList.add('active');
  } else {
    if (autoModeBtn) autoModeBtn.classList.add('active');
  }
}

function updateChartsTheme() {
  // Update all charts to ensure they work properly with theme
  const charts = ['clientGrowthChart', 'demoRequestsChart', 'revenueChart', 'conversionFunnel', 
                 'partnersStatusChart', 'usersStatusChart', 'trafficSources', 'topRequestsChart', 'salesChart'];
  
  charts.forEach(chartId => {
    const chart = Chart.getChart(chartId);
    if (chart) {
      chart.update();
    }
  });
}

// Listen for system theme changes
if (window.matchMedia) {
  const colorSchemeQuery = window.matchMedia('(prefers-color-scheme: dark)');
  colorSchemeQuery.addEventListener('change', (e) => {
    if (currentTheme === 'auto') {
      applyTheme('auto');
      updateChartsTheme();
    }
  });
}
