// ULTIMATE MOBILE SCROLLING PERFORMANCE JS - 2025 Edition
// Apply to ALL pages for ultra-smooth mobile scrolling
(function() {
  'use strict';
  
  // ======================== CORE UTILITIES ========================
  
  // Mobile detection
  const isMobile = () => window.innerWidth <= 768 || 
    /Android|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
  
  // Ultra-fast debounce - optimized for 60fps
  const debounce = (func, wait) => {
    let timeout;
    return (...args) => {
      clearTimeout(timeout);
      timeout = setTimeout(() => func(...args), wait);
    };
  };
  
  // Request animation frame throttle
  const throttleRAF = (func) => {
    let ticking = false;
    return (...args) => {
      if (!ticking) {
        requestAnimationFrame(() => {
          func(...args);
          ticking = false;
        });
        ticking = true;
      }
    };
  };
  
  // ======================== SCROLL OPTIMIZATION ========================
  
  function optimizeScrolling() {
    if (!isMobile()) return;
    
    // INSTANT SCROLL BEHAVIOR
    document.documentElement.style.scrollBehavior = 'auto';
    document.body.style.scrollBehavior = 'auto';
    
    // HARDWARE ACCELERATION
    document.documentElement.style.transform = 'translateZ(0)';
    document.body.style.transform = 'translateZ(0)';
    
    // OVERSCROLL BEHAVIOR
    document.documentElement.style.overscrollBehavior = 'contain';
    document.body.style.overscrollBehavior = 'contain';
    
    // WEBKIT OVERFLOW SCROLLING
    document.documentElement.style.webkitOverflowScrolling = 'touch';
    document.body.style.webkitOverflowScrolling = 'touch';
    
    // WILL CHANGE OPTIMIZATION
    document.body.style.willChange = 'scroll-position';
    
    // BACKFACE VISIBILITY
    document.body.style.backfaceVisibility = 'hidden';
    
    // PERSPECTIVE
    document.body.style.perspective = '1000px';
    
    // Mobile scroll optimization applied
  }
  
  // ======================== VIEWPORT OPTIMIZATION ========================
  
  function optimizeViewport() {
    if (!isMobile()) return;
    
    const updateViewport = () => {
      // CSS CUSTOM PROPERTY FOR DYNAMIC VIEWPORT
      const vh = window.innerHeight * 0.01;
      document.documentElement.style.setProperty('--vh', vh + 'px');
      
      // SAFE AREA INSET HANDLING
      const safeAreaTop = parseInt(getComputedStyle(document.documentElement)
        .getPropertyValue('env(safe-area-inset-top)')) || 0;
      const safeAreaBottom = parseInt(getComputedStyle(document.documentElement)
        .getPropertyValue('env(safe-area-inset-bottom)')) || 0;
      
      document.documentElement.style.setProperty('--safe-area-top', safeAreaTop + 'px');
      document.documentElement.style.setProperty('--safe-area-bottom', safeAreaBottom + 'px');
    };
    
    updateViewport();
    
    // OPTIMIZED RESIZE HANDLING - 30ms for smooth response
    const debouncedUpdate = debounce(updateViewport, 30);
    window.addEventListener('resize', debouncedUpdate, { passive: true });
    
    // ORIENTATION CHANGE HANDLING
    window.addEventListener('orientationchange', () => {
      setTimeout(debouncedUpdate, 100);
    }, { passive: true });
    
    // Mobile viewport optimization applied
  }
  
  // ======================== TOUCH OPTIMIZATION ========================
  
  function optimizeTouch() {
    if (!isMobile()) return;
    
    // PASSIVE TOUCH LISTENERS FOR BETTER PERFORMANCE
    const passiveSupported = checkPassiveSupport();
    
    // PREVENT DEFAULT TOUCH BEHAVIORS THAT INTERFERE WITH SCROLLING
    document.addEventListener('touchstart', () => {}, 
      passiveSupported ? { passive: true } : false);
    document.addEventListener('touchmove', () => {}, 
      passiveSupported ? { passive: true } : false);
    document.addEventListener('touchend', () => {}, 
      passiveSupported ? { passive: true } : false);
    
    // OPTIMIZE TAP HIGHLIGHT
    document.documentElement.style.webkitTapHighlightColor = 'transparent';
    
    // Touch optimization applied
  }
  
  // ======================== NAVIGATION OPTIMIZATION ========================
  
  function optimizeNavigation() {
    const menuToggle = document.getElementById('menu-toggle');
    const navLinks = document.getElementById('nav-links');
    const navLogo = document.querySelector('.nav-logo');
    
    if (!menuToggle || !navLinks) return;
    
    // ULTRA-FAST MENU TOGGLE - NO DELAYS
    const toggleMenu = () => {
      const isActive = navLinks.classList.contains('active');
      navLinks.classList.toggle('active');
      menuToggle.classList.toggle('active');
      if (navLogo) navLogo.classList.toggle('hidden');
      
      // ALLOW SCROLLING - Only prevent scroll on nav background if needed
      // Don't block main body scrolling on mobile
      if (!isMobile()) {
        document.body.style.overflow = isActive ? '' : 'hidden';
      }
    };
    
    // TOUCH-OPTIMIZED MENU TOGGLE
    if (isMobile()) {
      menuToggle.addEventListener('touchstart', (e) => {
        e.preventDefault();
        toggleMenu();
      }, { passive: false });
    }
    
    // FALLBACK CLICK HANDLER
    menuToggle.addEventListener('click', (e) => {
      e.preventDefault();
      toggleMenu();
    });
    
    // CLOSE MENU ON LINK CLICK
    navLinks.addEventListener('click', (e) => {
      if (e.target.tagName === 'A') {
        navLinks.classList.remove('active');
        menuToggle.classList.remove('active');
        if (navLogo) navLogo.classList.remove('hidden');
        if (!isMobile()) {
          document.body.style.overflow = '';
        }
      }
    });
    
    // CLOSE MENU ON OUTSIDE CLICK - OPTIMIZED DEBOUNCE
    document.addEventListener('click', debounce((e) => {
      const nav = document.querySelector('nav');
      if (nav && !nav.contains(e.target) && navLinks.classList.contains('active')) {
        navLinks.classList.remove('active');
        menuToggle.classList.remove('active');
        if (navLogo) navLogo.classList.remove('hidden');
        if (!isMobile()) {
          document.body.style.overflow = '';
        }
      }
    }, 10), { passive: true });
    
    // OPTIMIZE NAVIGATION SCROLLING
    if (navLinks) {
      navLinks.style.webkitOverflowScrolling = 'touch';
      navLinks.style.overscrollBehavior = 'contain';
      navLinks.style.contain = 'layout style';
      navLinks.style.transform = 'translateZ(0)';
    }
    
    // Navigation optimization applied
  }
  
  // ======================== FORM OPTIMIZATION ======================== 
  
  function optimizeForms() {
    if (!isMobile()) return;
    
    // PREVENT iOS ZOOM ON FORM INPUTS
    const inputs = document.querySelectorAll('input, select, textarea');
    inputs.forEach(input => {
      if (input.style.fontSize === '' || parseFloat(input.style.fontSize) < 16) {
        input.style.fontSize = '16px';
      }
      
      // OPTIMIZE FORM SCROLLING
      input.style.transform = 'translateZ(0)';
      input.style.contain = 'layout style';
    });
    
    // OPTIMIZE FORM CONTAINERS
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
      form.style.webkitOverflowScrolling = 'touch';
      form.style.contain = 'layout style';
      form.style.transform = 'translateZ(0)';
    });
    
    // Form optimization applied
  }
  
  // ======================== STAR ANIMATION OPTIMIZATION ========================
  
  function optimizeStars() {
    const starsContainer = document.getElementById('stars');
    if (!starsContainer) return;
    
    // DISABLE ALL STARS ON MOBILE FOR MAXIMUM PERFORMANCE
    if (isMobile()) {
      // Hide and disable star container completely on mobile
      starsContainer.style.display = 'none';
      starsContainer.style.visibility = 'hidden';
      starsContainer.innerHTML = ''; // Clear any existing stars
      
      // Stars disabled on mobile for optimal performance
      return; // Exit early - no stars on mobile
    }
    
    // DESKTOP ONLY - Create minimal stars for desktop users
    const starCount = 30; // Desktop gets some stars
    const fragment = document.createDocumentFragment();
    
    for (let i = 0; i < starCount; i++) {
      const star = document.createElement('div');
      star.className = 'star';
      
      // DESKTOP STAR STYLES
      star.style.cssText = `
        width: 2px;
        height: 2px;
        left: ${Math.random() * 100}%;
        top: ${Math.random() * 100}%;
        opacity: ${Math.random() * 0.4 + 0.2};
        position: absolute;
        background: #fff;
        border-radius: 50%;
        will-change: opacity;
        contain: layout;
        transform: translateZ(0);
        backface-visibility: hidden;
        animation: desktopStarFade ${4 + Math.random() * 3}s ease-in-out infinite;
        animation-delay: ${Math.random() * 3}s;
      `;
      
      fragment.appendChild(star);
    }
    
    starsContainer.appendChild(fragment);
    
    // ADD DESKTOP-ONLY STAR ANIMATION CSS
    if (!document.querySelector('#star-animation')) {
      const style = document.createElement('style');
      style.id = 'star-animation';
      style.textContent = `
        @keyframes desktopStarFade {
          0%, 100% { opacity: 0.2; transform: translateZ(0); }
          50% { opacity: 0.5; transform: translateZ(0); }
        }
        @media (max-width: 768px) {
          .star, .stars, #stars { 
            display: none !important; 
            visibility: hidden !important;
            animation: none !important;
          }
        }
        @media (prefers-reduced-motion: reduce) {
          .star { animation: none !important; opacity: 0.3 !important; }
        }
      `;
      document.head.appendChild(style);
    }
    
    // Desktop star animation applied (mobile disabled)
  }
  
  // ======================== LAZY LOADING OPTIMIZATION ========================
  
  function optimizeLazyLoading() {
    if (!('IntersectionObserver' in window)) return;
    
    // ULTRA-FAST INTERSECTION OBSERVER
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('animate-in');
          observer.unobserve(entry.target);
        }
      });
    }, {
      threshold: 0,
      rootMargin: '50px 0px'
    });
    
    // OBSERVE ELEMENTS
    const elements = document.querySelectorAll('section, .rep-team-box, .calendar-box, .card');
    elements.forEach(el => {
      el.classList.add('animate-on-scroll');
      observer.observe(el);
    });
    
    // ADD OPTIMIZED ANIMATION CSS
    if (!document.querySelector('#lazy-animation')) {
      const style = document.createElement('style');
      style.id = 'lazy-animation';
      style.textContent = `
        .animate-on-scroll {
          opacity: 0;
          transform: translateY(5px) translateZ(0);
          transition: opacity 0.2s ease, transform 0.2s ease;
        }
        .animate-on-scroll.animate-in {
          opacity: 1;
          transform: translateY(0) translateZ(0);
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
    
    // Lazy loading optimization applied
  }
  
  // ======================== PERFORMANCE MONITORING ========================
  
  function monitorPerformance() {
    if ('PerformanceObserver' in window) {
      // MONITOR LAYOUT SHIFTS
      const observer = new PerformanceObserver((list) => {
        list.getEntries().forEach(entry => {
          if (entry.hadRecentInput) return;
          if (entry.value > 0.1) {
            // Layout shift detected
          }
        });
      });
      
      observer.observe({ entryTypes: ['layout-shift'] });
    }
    
    // MONITOR SCROLL PERFORMANCE
    let isScrolling = false;
    const scrollMonitor = throttleRAF(() => {
      if (!isScrolling) {
        isScrolling = true;
        requestAnimationFrame(() => {
          isScrolling = false;
        });
      }
    });
    
    window.addEventListener('scroll', scrollMonitor, { passive: true });
    
    // Performance monitoring active
  }
  
  // ======================== UTILITY FUNCTIONS ========================
  
  function checkPassiveSupport() {
    let passiveSupported = false;
    try {
      const options = {
        get passive() {
          passiveSupported = true;
          return false;
        }
      };
      window.addEventListener('test', null, options);
      window.removeEventListener('test', null, options);
    } catch (err) {
      passiveSupported = false;
    }
    return passiveSupported;
  }
  
  // ======================== INITIALIZATION ========================
  
  function init() {
    // REMOVE LOADING STATE IMMEDIATELY
    document.body.classList.remove('loading');
    document.body.classList.add('loaded');
    
    // APPLY ALL OPTIMIZATIONS
    optimizeScrolling();
    optimizeViewport();
    optimizeTouch();
    optimizeNavigation();
    optimizeForms();
    
    if (isMobile()) {
      // MOBILE-SPECIFIC OPTIMIZATIONS
      optimizeStars();
      optimizeLazyLoading();
      monitorPerformance();
      
      // All mobile scroll optimizations applied
    } else {
      // DESKTOP OPTIMIZATIONS (MINIMAL)
      setTimeout(() => {
        optimizeStars();
        optimizeLazyLoading();
      }, 16);
      
      // Desktop optimizations applied
    }
  }
  
  // ======================== AUTO-START ========================
  
  // START IMMEDIATELY IF POSSIBLE
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else if (document.readyState === 'interactive') {
    // DOM is interactive - start immediately
    init();
  } else {
    // DOM is complete - start immediately  
    init();
  }
  
  // GLOBAL SCROLL UTILITIES
  window.scrollToTop = () => {
    if ('scrollTo' in window) {
      window.scrollTo({ top: 0, behavior: 'auto' });
    } else {
      window.scrollTo(0, 0);
    }
  };
  
  window.smoothScrollToTop = () => {
    if ('scrollTo' in window) {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    } else {
      window.scrollTo(0, 0);
    }
  };
  
})();
