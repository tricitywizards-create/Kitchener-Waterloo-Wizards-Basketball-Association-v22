// Ultra-smooth mobile JS - Fixed scrolling delays
(function(){
'use strict';

// Mobile detection
const m=()=>window.innerWidth<=768||/Android|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);

// HIGH-PERFORMANCE DEBOUNCE - Reduced delay from 100ms to 16ms
const d=(f,w)=>{let t;return(...a)=>{clearTimeout(t);t=setTimeout(()=>f(...a),w)}}; 

// Mobile navigation - OPTIMIZED FOR TOUCH
function n(){
  const t=document.getElementById('menu-toggle'),
        l=document.getElementById('nav-links'),
        g=document.querySelector('.nav-logo');
  
  if(!t||!l)return;
  
  // INSTANT TOUCH RESPONSE - No preventDefault delays
  t.addEventListener('touchstart',()=>{
    const a=l.classList.contains('active');
    l.classList.toggle('active');
    t.classList.toggle('active');
    if(g)g.classList.toggle('hidden');
    if(!m())document.body.style.overflow=a?'':'hidden';
  },{passive:true});
  
  // Fallback for non-touch devices
  t.addEventListener('click',e=>{
    e.preventDefault();
    const a=l.classList.contains('active');
    l.classList.toggle('active');
    t.classList.toggle('active');
    if(g)g.classList.toggle('hidden');
    if(!m())document.body.style.overflow=a?'':'hidden';
  });
  
  l.onclick=e=>{
    if(e.target.tagName==='A'){
      l.classList.remove('active');
      t.classList.remove('active');
      if(g)g.classList.remove('hidden');
      if(!m())document.body.style.overflow='';
    }
  };
  
  // REDUCED DEBOUNCE - 16ms for 60fps responsiveness
  document.onclick=d(e=>{
    const nav=document.querySelector('nav');
    if(!nav.contains(e.target)&&l.classList.contains('active')){
      l.classList.remove('active');
      t.classList.remove('active');
      if(g)g.classList.remove('hidden');
      if(!m())document.body.style.overflow='';
    }
  },16);
}

// ULTRA-SMOOTH MOBILE VIEWPORT - REMOVED PROBLEMATIC SCROLL HANDLER
function v(){
  if(!m())return;
  
  const s=()=>{
    document.documentElement.style.setProperty('--vh',window.innerHeight*0.01+'px');
  };
  
  s();
  
  // OPTIMIZED RESIZE HANDLING - Reduced from 150ms to 50ms
  const ds=d(s,50);
  window.addEventListener('resize',ds,{passive:true});
  window.addEventListener('orientationchange',()=>setTimeout(ds,100),{passive:true});
  
  // REMOVED PROBLEMATIC SCROLL HANDLER - This was causing delays!
  // The height manipulation was interfering with smooth scrolling
}

// MINIMAL STAR ANIMATION - PERFORMANCE OPTIMIZED
function stars(){
  const c=document.getElementById('stars');
  if(!c)return;
  
  // EVEN FEWER STARS - Only 5 on mobile for maximum performance
  const count=m()?5:30;
  const f=document.createDocumentFragment();
  
  for(let i=0;i<count;i++){
    const s=document.createElement('div');
    s.className='star';
    // SIMPLIFIED ANIMATION - No transform/scale changes
    s.style.cssText=`width:1px;height:1px;left:${Math.random()*100}%;top:${Math.random()*100}%;opacity:${Math.random()*0.3+0.1};animation:fade ${4+Math.random()*2}s ease-in-out infinite;animation-delay:${Math.random()*2}s;position:absolute;background:#fff;border-radius:50%;will-change:opacity;contain:layout`;
    f.appendChild(s);
  }
  
  c.appendChild(f);
  
  // ULTRA-MINIMAL CSS ANIMATION - Only opacity changes
  if(!document.querySelector('#sa')){
    const st=document.createElement('style');
    st.id='sa';
    st.textContent='@keyframes fade{0%,100%{opacity:.1}50%{opacity:.3}}@media (prefers-reduced-motion:reduce){.star{animation:none!important;opacity:.2!important}}';
    document.head.appendChild(st);
  }
}

// INSTANT LAZY LOADING - NO DELAYS
function lazy(){
  if(!('IntersectionObserver' in window))return;
  
  // IMMEDIATE ACTIVATION - 0 threshold for instant response
  const o=new IntersectionObserver(e=>{
    e.forEach(t=>{
      if(t.isIntersecting){
        t.target.classList.add('ai');
        o.unobserve(t.target);
      }
    });
  },{threshold:0,rootMargin:'50px 0px'});
  
  document.querySelectorAll('section,.rep-team-box,.calendar-box').forEach(el=>{
    el.classList.add('aos');
    o.observe(el);
  });
  
  // ULTRA-FAST ANIMATIONS - Reduced from 400ms to 200ms
  if(!document.querySelector('#las')){
    const st=document.createElement('style');
    st.id='las';
    st.textContent='.aos{opacity:0;transform:translateY(5px);transition:opacity .2s ease,transform .2s ease}.aos.ai{opacity:1;transform:translateY(0)}@media (prefers-reduced-motion:reduce){.aos{opacity:1!important;transform:none!important;transition:none!important}}';
    document.head.appendChild(st);
  }
}

// SMOOTH SCROLL ENHANCEMENT FOR MOBILE
function smoothScroll(){
  if(!m())return;
  
  // ENABLE HARDWARE ACCELERATION FOR SCROLLING
  document.documentElement.style.scrollBehavior='smooth';
  
  // OPTIMIZE SCROLL CONTAINER
  const body=document.body;
  body.style.overscrollBehavior='contain';
  body.style.scrollSnapType='none'; // Remove any snap interference
  body.style.webkitOverflowScrolling='touch';
  
  // PREVENT MOMENTUM SCROLLING INTERFERENCE
  window.addEventListener('touchmove',()=>{},{ passive: true });
  
  // INSTANT SCROLL TO TOP FUNCTION
  window.scrollToTop=()=>{
    if('scrollTo' in window){
      window.scrollTo({top:0,behavior:'smooth'});
    }else{
      window.scrollTo(0,0);
    }
  };
}

// ULTRA-FAST INITIALIZATION
function init(){
  // IMMEDIATE VISIBILITY - No loading delay
  document.body.classList.remove('loading');
  document.body.classList.add('loaded');
  
  n(); // Navigation
  smoothScroll(); // Enable smooth scrolling
  
  if(m()){
    v(); // Mobile viewport optimization
    
    // IMMEDIATE FEATURE ACTIVATION - No setTimeout delay
    stars();
    lazy();
  }else{
    // Desktop gets full features with minimal delay
    setTimeout(()=>{
      stars();
      lazy();
    },16);
  }
}

// INSTANT START - Check for interactive state for faster loading
if(document.readyState==='loading'){
  document.addEventListener('DOMContentLoaded',init);
}else if(document.readyState==='interactive'){
  // Start immediately if DOM is interactive
  init();
}else{
  init();
}

})();
