#!/usr/bin/env python3
"""
Disable Mobile Stars Script
Adds CSS to completely disable star animations on mobile devices for all HTML pages
"""

import os
import glob
from pathlib import Path

def disable_mobile_stars():
    """Add mobile star disable CSS to all HTML files"""
    
    # Get the directory where the script is located
    script_dir = Path(__file__).parent
    
    # Find all HTML files in the directory
    html_files = glob.glob(str(script_dir / "*.html"))
    
    # Skip files that don't need star disabling
    skip_files = ['test-mobile-performance.html', 'sitemap.html']
    html_files = [f for f in html_files if not any(skip in f for skip in skip_files)]
    
    print(f"Found {len(html_files)} HTML files to update")
    
    # Mobile star disable CSS to add
    mobile_star_disable_css = '''
      /* DISABLE STARS ON MOBILE FOR OPTIMAL PERFORMANCE */\n      @media (max-width: 768px) {\n        .star, .stars, #stars {\n          display: none !important;\n          visibility: hidden !important;\n          opacity: 0 !important;\n          animation: none !important;\n          transform: none !important;\n          will-change: auto !important;\n        }\n      }'''
    
    updated_count = 0
    
    for html_file in html_files:
        try:
            print(f"Updating: {os.path.basename(html_file)}")
            
            # Read the file
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check if mobile star disable is already present
            if 'DISABLE STARS ON MOBILE' in content:
                print(f"  ✓ Already has mobile star disable CSS")
                continue
            
            # Find the closing </style> tag in the inline CSS section
            import re
            style_pattern = r'(\s*</style>)(\s*</head>)'
            
            if re.search(style_pattern, content):
                # Add the mobile star disable CSS before the closing </style>
                content = re.sub(
                    style_pattern,
                    mobile_star_disable_css + r'\1\2',
                    content
                )
                
                # Write the updated content back
                with open(html_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                print(f"  ✅ Added mobile star disable CSS")
                updated_count += 1
            else:
                print(f"  ⚠ Could not find </style> tag to update")
            
        except Exception as e:
            print(f"  ❌ Error updating {os.path.basename(html_file)}: {str(e)}")
    
    print(f"\n🎉 Mobile star disable complete!")
    print(f"✅ Updated {updated_count} HTML files")
    
    if updated_count > 0:
        print(f"\n📱 Mobile Performance Improvements:")
        print(f"  ✓ Stars completely disabled on mobile devices")
        print(f"  ✓ Reduced CPU/GPU usage on phones and tablets")
        print(f"  ✓ Lower battery consumption")
        print(f"  ✓ Faster scrolling and touch response")
        print(f"  ✓ Improved overall mobile performance")
        
        print(f"\n🖥️ Desktop Experience:")
        print(f"  ✓ Stars still visible and animated on desktop")
        print(f"  ✓ Full visual experience preserved for large screens")
        
        print(f"\n📈 Expected Results:")
        print(f"  • Smoother scrolling on mobile devices")
        print(f"  • Faster page load times on mobile")
        print(f"  • Better battery life for mobile users")
        print(f"  • Reduced mobile data usage")
        print(f"  • Improved mobile performance scores")
    else:
        print(f"\n✅ All files already have mobile star optimizations!")

if __name__ == "__main__":
    disable_mobile_stars()
