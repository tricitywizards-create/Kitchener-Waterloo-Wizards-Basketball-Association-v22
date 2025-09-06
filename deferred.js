// Deferred JavaScript - Load after critical content
// Performance-optimized animations and interactions

(function() {
  'use strict';
  
  // Utility functions
  function isMobile() {
    return window.innerWidth <= 768 || /Android|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
  }
  
  function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
      const later = () => {
        clearTimeout(timeout);
        func(...args);
      };
      clearTimeout(timeout);
      timeout = setTimeout(later, wait);
    };
  }
  
  // Reduced star animation for mobile performance
  function initStarField() {
    const starsContainer = document.getElementById('stars');
    if (!starsContainer) return;
    
    // Reduce stars on mobile for better performance
    const starCount = isMobile() ? 25 : 100;
    
    // Create stars with better performance
    const fragment = document.createDocumentFragment();
    
    for (let i = 0; i < starCount; i++) {
      const star = document.createElement('div');
      star.className = 'star';
      
      // Randomize position and size
      const size = Math.random() * 2 + 0.5;
      const x = Math.random() * 100;
      const y = Math.random() * 100;
      const opacity = Math.random() * 0.6 + 0.2;
      
      // Use CSS custom properties for better performance
      star.style.cssText = `
        width: ${size}px;
        height: ${size}px;
        left: ${x}%;
        top: ${y}%;
        opacity: ${opacity};
        animation: twinkle ${3 + Math.random() * 4}s linear infinite;
        animation-delay: ${Math.random() * 5}s;
      `;
      
      fragment.appendChild(star);
    }
    
    starsContainer.appendChild(fragment);
    
    // Add CSS animation for stars (only if not already present)
    if (!document.querySelector('#star-animation-style')) {
      const style = document.createElement('style');
      style.id = 'star-animation-style';
      style.textContent = `
        @keyframes twinkle {
          0%, 100% { opacity: 0.2; transform: scale(1); }
          50% { opacity: 0.8; transform: scale(1.1); }
        }
        
        .star {
          will-change: opacity, transform;
          backface-visibility: hidden;
        }
        
        /* Pause animations when not visible for battery saving */
        @media (prefers-reduced-motion: reduce) {
          .star { animation: none !important; }
        }
      `;
      document.head.appendChild(style);
    }
  }
  
  // Mobile navigation functionality
  function initMobileNav() {
    const menuToggle = document.getElementById("menu-toggle");
    const navLinks = document.getElementById("nav-links");
    const navLogo = document.querySelector(".nav-logo");
    
    if (!menuToggle || !navLinks) return;
    
    // Menu toggle with better touch handling
    menuToggle.addEventListener("click", (e) => {
      e.preventDefault();
      e.stopPropagation();
      
      const isActive = navLinks.classList.contains("active");
      
      if (isActive) {
        navLinks.classList.remove("active");
        menuToggle.classList.remove("active");
        if (navLogo) navLogo.classList.remove("hidden");
        document.body.style.overflow = '';
      } else {
        navLinks.classList.add("active");
        menuToggle.classList.add("active");
        if (navLogo) navLogo.classList.add("hidden");
        // Prevent body scroll when menu is open
        document.body.style.overflow = 'hidden';
      }
    });
    
    // Close menu when clicking navigation links
    navLinks.addEventListener("click", (e) => {
      if (e.target.tagName === 'A') {
        navLinks.classList.remove("active");
        menuToggle.classList.remove("active");
        if (navLogo) navLogo.classList.remove("hidden");
        document.body.style.overflow = '';
      }
    });
    
    // Close mobile menu when clicking outside (debounced)
    const closeMenuOnOutsideClick = debounce((e) => {
      const nav = document.querySelector("nav");
      if (!nav.contains(e.target) && navLinks.classList.contains("active")) {
        navLinks.classList.remove("active");
        menuToggle.classList.remove("active");
        if (navLogo) navLogo.classList.remove("hidden");
        document.body.style.overflow = '';
      }
    }, 100);
    
    document.addEventListener("click", closeMenuOnOutsideClick);
  }
  
  // Enhanced mobile viewport handling
  function initMobileViewport() {
    if (!isMobile()) return;
    
    // Set CSS custom properties for dynamic viewport
    const setVH = () => {
      const vh = window.innerHeight * 0.01;
      document.documentElement.style.setProperty('--vh', `${vh}px`);
    };
    
    setVH();
    
    // Debounced resize handler
    const debouncedSetVH = debounce(setVH, 150);
    window.addEventListener('resize', debouncedSetVH);
    
    // Handle orientation changes
    window.addEventListener('orientationchange', () => {
      setTimeout(debouncedSetVH, 200);
    });
    
    // Optimized scroll handling for better performance - removed layout thrashing
    let lastScrollY = window.scrollY;
    let ticking = false;
    
    const handleScroll = () => {
      if (!ticking) {
        requestAnimationFrame(() => {
          // Simple scroll direction tracking without layout manipulation
          const isScrollingDown = window.scrollY > lastScrollY && window.scrollY > 100;
          if (isScrollingDown) {
            // Use CSS class instead of style manipulation
            document.body.classList.add('scrolling-down');
          } else {
            document.body.classList.remove('scrolling-down');
          }
          lastScrollY = window.scrollY;
          ticking = false;
        });
        ticking = true;
      }
    };
    
    window.addEventListener('scroll', handleScroll, { passive: true });
    
    // Prevent zoom on double-tap for interactive elements
    const preventZoomElements = document.querySelectorAll('a, button, .btn, .rep-team-box, .calendar-box');
    preventZoomElements.forEach(element => {
      let touchTime = 0;
      
      element.addEventListener('touchend', function(e) {
        const currentTime = new Date().getTime();
        const tapLength = currentTime - touchTime;
        
        if (tapLength < 500 && tapLength > 0) {
          e.preventDefault();
          
          // Handle the click after preventing default
          setTimeout(() => {
            if (this.href) {
              if (this.target === '_blank') {
                window.open(this.href, '_blank');
              } else {
                window.location.href = this.href;
              }
            } else if (this.onclick) {
              this.onclick();
            }
          }, 10);
        }
        touchTime = currentTime;
      }, { passive: false });
    });
  }
  
  // Intersection Observer for lazy loading animations
  function initLazyAnimations() {
    if (!('IntersectionObserver' in window)) return;
    
    const observerOptions = {
      threshold: 0.1,
      rootMargin: '50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('animate-in');
          observer.unobserve(entry.target);
        }
      });
    }, observerOptions);
    
    // Observe elements that should animate in
    document.querySelectorAll('section, .rep-team-box, .calendar-box').forEach(el => {
      el.classList.add('animate-on-scroll');
      observer.observe(el);
    });
    
    // Add animation styles if not already present
    if (!document.querySelector('#lazy-animation-style')) {
      const style = document.createElement('style');
      style.id = 'lazy-animation-style';
      style.textContent = `
        .animate-on-scroll {
          opacity: 0;
          transform: translateY(20px);
          transition: opacity 0.6s ease, transform 0.6s ease;
        }
        
        .animate-on-scroll.animate-in {
          opacity: 1;
          transform: translateY(0);
        }
        
        @media (prefers-reduced-motion: reduce) {
          .animate-on-scroll {
            opacity: 1 !important;
            transform: none !important;
            transition: none !important;
          }
        }
      `;
      document.head.appendChild(style);
    }
  }
  
  // Skip external font loading to prevent blocking - use system fonts only
  function loadWebFont() {
    // Use system fonts for maximum performance
    document.documentElement.classList.add('fonts-loaded');
    // No external font loading to prevent render blocking
  }
  
  // Initialize all deferred functionality
  function init() {
    // Remove loading class if present
    document.body.classList.remove('loading');
    document.body.classList.add('loaded');
    
    // Initialize components
    initMobileNav();
    
    if (isMobile()) {
      initMobileViewport();
    }
    
    // Initialize animations with a delay to ensure critical content is rendered
    setTimeout(() => {
      initStarField();
      initLazyAnimations();
      loadWebFont();
    }, 100);
  }
  
  // Start initialization
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
  
})();
