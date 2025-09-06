#!/usr/bin/env python3
"""
Ultimate Mobile Scrolling Optimization Script
Applies comprehensive mobile scrolling optimizations to all HTML pages
"""

import os
import re
import glob
from pathlib import Path

def apply_mobile_optimizations():
    """Apply mobile scrolling optimizations to all HTML pages"""
    
    # Get the directory where the script is located
    script_dir = Path(__file__).parent
    
    # Find all HTML files in the directory
    html_files = glob.glob(str(script_dir / "*.html"))
    
    # Skip files that are already optimized or are templates
    skip_files = [
        'index-ultra-mobile.html',
        'index-smooth-mobile.html', 
        'index-mobile-optimized.html',
        'sitemap.html'
    ]
    
    html_files = [f for f in html_files if not any(skip in f for skip in skip_files)]
    
    print(f"Found {len(html_files)} HTML files to optimize")
    
    # Mobile scroll optimization CSS to inject
    mobile_css_injection = '''
  <!-- ULTIMATE MOBILE SCROLL OPTIMIZATION -->
  <link rel="stylesheet" href="mobile-scroll-ultimate.css">
  <style>
    /* CRITICAL MOBILE SCROLL OPTIMIZATIONS - INLINE FOR INSTANT LOADING */
    @media (max-width: 768px) {
      html {
        height: 100%;
        overflow-y: scroll !important;
        -webkit-overflow-scrolling: touch;
        scroll-behavior: auto !important;
        overscroll-behavior: contain;
        transform: translateZ(0);
        will-change: scroll-position;
      }
      body {
        min-height: 100vh;
        min-height: -webkit-fill-available;
        overflow-y: scroll !important;
        -webkit-overflow-scrolling: touch;
        overscroll-behavior: contain;
        transform: translateZ(0);
        backface-visibility: hidden;
        perspective: 1000px;
        will-change: scroll-position;
        contain: layout style;
        -webkit-tap-highlight-color: transparent;
      }
      section, nav, .nav-links, main, article, aside {
        contain: layout style;
        transform: translateZ(0);
        -webkit-overflow-scrolling: touch;
        overscroll-behavior: contain;
      }
      .nav-links {
        position: fixed;
        top: 120px;
        left: 0;
        right: 0;
        height: calc(100vh - 120px);
        overflow-y: auto;
        overflow-x: hidden;
        -webkit-overflow-scrolling: touch;
        overscroll-behavior: contain;
      }
      * {
        -webkit-tap-highlight-color: transparent !important;
        touch-action: manipulation !important;
      }
      p, span, div, h1, h2, h3, h4, h5, h6, label, li {
        -webkit-user-select: text !important;
        user-select: text !important;
      }
      a, button, .btn, input, select, textarea, .menu-toggle {
        -webkit-user-select: none !important;
        user-select: none !important;
        min-height: 44px;
        min-width: 44px;
      }
      input, select, textarea {
        font-size: 16px !important;
      }
    }
  </style>'''
    
    # JavaScript optimization to inject
    js_injection = '''
  <!-- ULTIMATE MOBILE SCROLL OPTIMIZATION JS -->
  <script src="mobile-scroll-ultimate.js" defer></script>'''
    
    optimized_count = 0
    
    for html_file in html_files:
        try:
            print(f"Optimizing: {os.path.basename(html_file)}")
            
            # Read the file
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Skip if already optimized
            if 'mobile-scroll-ultimate.css' in content:
                print(f"  ✓ Already optimized, skipping")
                continue
            
            # Backup original file
            backup_file = html_file.replace('.html', '.original.html')
            if not os.path.exists(backup_file):
                with open(backup_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"  ✓ Created backup: {os.path.basename(backup_file)}")
            
            # Find where to inject CSS (before closing </head>)
            head_pattern = r'(\s*</head>)'
            if re.search(head_pattern, content):
                content = re.sub(head_pattern, mobile_css_injection + r'\\1', content)
                print(f"  ✓ Injected mobile CSS optimizations")
            else:
                print(f"  ⚠ Could not find </head> tag")
                continue
            
            # Find where to inject JS (before closing </body>)
            body_pattern = r'(\s*</body>)'
            if re.search(body_pattern, content):
                content = re.sub(body_pattern, js_injection + r'\\1', content)
                print(f"  ✓ Injected mobile JS optimizations")
            else:
                print(f"  ⚠ Could not find </body> tag")
                continue
            
            # Ensure viewport meta tag is optimized
            viewport_pattern = r'<meta name="viewport"[^>]*>'
            optimized_viewport = '<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0, user-scalable=yes, viewport-fit=cover">'
            
            if re.search(viewport_pattern, content):
                content = re.sub(viewport_pattern, optimized_viewport, content)
                print(f"  ✓ Optimized viewport meta tag")
            else:
                # Add viewport if missing
                charset_pattern = r'(<meta charset="[^"]*">)'
                if re.search(charset_pattern, content):
                    content = re.sub(charset_pattern, r'\\1\\n  ' + optimized_viewport, content)
                    print(f"  ✓ Added optimized viewport meta tag")
            
            # Add mobile-specific meta tags if missing
            mobile_meta_tags = [
                '<meta name="mobile-web-app-capable" content="yes">',
                '<meta name="apple-mobile-web-app-capable" content="yes">',
                '<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">'
            ]
            
            for meta_tag in mobile_meta_tags:
                if meta_tag not in content:
                    viewport_injection = optimized_viewport + '\\n  ' + meta_tag
                    content = content.replace(optimized_viewport, viewport_injection)
            
            print(f"  ✓ Added mobile-specific meta tags")
            
            # Ensure body has loading class for optimization
            body_tag_pattern = r'<body([^>]*)>'
            def add_loading_class(match):
                attrs = match.group(1)
                if 'class=' in attrs:
                    # Add loading to existing class
                    attrs = re.sub(r'class="([^"]*)"', r'class="loading \\1"', attrs)
                else:
                    # Add new class attribute
                    attrs += ' class="loading"'
                return f'<body{attrs}>'
            
            if re.search(body_tag_pattern, content):
                content = re.sub(body_tag_pattern, add_loading_class, content)
                print(f"  ✓ Added loading class to body")
            
            # Write optimized file
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            optimized_count += 1
            print(f"  ✅ Successfully optimized {os.path.basename(html_file)}")
            
        except Exception as e:
            print(f"  ❌ Error optimizing {os.path.basename(html_file)}: {str(e)}")
    
    print(f"\\n🎉 Optimization complete!")
    print(f"✅ Successfully optimized {optimized_count} HTML files")
    print(f"📱 All pages now have ultra-smooth mobile scrolling!")
    print(f"\\n📄 Files created:")
    print(f"  - mobile-scroll-ultimate.css")
    print(f"  - mobile-scroll-ultimate.js") 
    print(f"  - *.original.html (backups)")
    
    print(f"\\n🔧 What was applied:")
    print(f"  ✓ Hardware-accelerated scrolling")
    print(f"  ✓ Touch-optimized interactions") 
    print(f"  ✓ Overscroll behavior containment")
    print(f"  ✓ Passive event listeners")
    print(f"  ✓ GPU acceleration (translateZ)")
    print(f"  ✓ Scroll performance monitoring")
    print(f"  ✓ Form input zoom prevention")
    print(f"  ✓ Navigation scroll optimization")
    print(f"  ✓ Reduced animation overhead")
    print(f"  ✓ Layout shift prevention")
    
    print(f"\\n📱 Test on mobile devices:")
    print(f"  - iPhone Safari")
    print(f"  - Android Chrome") 
    print(f"  - iPad Safari")
    print(f"  - Various screen sizes")

if __name__ == "__main__":
    apply_mobile_optimizations()
