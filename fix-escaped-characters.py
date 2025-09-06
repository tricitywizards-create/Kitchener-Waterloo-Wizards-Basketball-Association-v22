#!/usr/bin/env python3
"""
Fix Escaped Characters in HTML Files
Removes literal \n and \1 characters that were incorrectly inserted by the optimization script
"""

import os
import glob
from pathlib import Path

def fix_escaped_characters():
    """Fix escaped characters in all HTML files"""
    
    # Get the directory where the script is located
    script_dir = Path(__file__).parent
    
    # Find all HTML files in the directory
    html_files = glob.glob(str(script_dir / "*.html"))
    
    # Skip the test file
    skip_files = ['test-mobile-performance.html']
    html_files = [f for f in html_files if not any(skip in f for skip in skip_files)]
    
    print(f"Found {len(html_files)} HTML files to fix")
    
    fixed_count = 0
    total_replacements = 0
    
    for html_file in html_files:
        try:
            print(f"Fixing: {os.path.basename(html_file)}")
            
            # Read the file
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Track original content to see if changes were made
            original_content = content
            file_replacements = 0
            
            # Fix literal \1 characters (regex backreferences that got escaped)
            while '\\1' in content:
                content = content.replace('\\1', '')
                file_replacements += 1
                total_replacements += 1
            
            # Fix literal \n characters in meta tags (but preserve actual newlines)
            # Replace \\n with actual newlines in meta tag content
            import re
            
            # Fix viewport meta tags with \\n
            content = re.sub(
                r'(<meta name="viewport"[^>]+>)\\n\s*(<meta[^>]+>)\\n\s*(<meta[^>]+>)\\n\s*(<meta[^>]+>)',
                r'\1\n  \2\n  \3\n  \4',
                content
            )
            
            # Count additional replacements
            if content != original_content:
                # Count how many \\n were replaced
                original_count = original_content.count('\\n')
                new_count = content.count('\\n')
                if original_count > new_count:
                    additional_replacements = original_count - new_count
                    file_replacements += additional_replacements
                    total_replacements += additional_replacements
            
            # Write the fixed content back to the file
            if content != original_content:
                with open(html_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                print(f"  ✅ Fixed {file_replacements} escaped characters")
                fixed_count += 1
            else:
                print(f"  ✓ No escaped characters found")
            
        except Exception as e:
            print(f"  ❌ Error fixing {os.path.basename(html_file)}: {str(e)}")
    
    print(f"\n🎉 Character fix complete!")
    print(f"✅ Fixed {fixed_count} HTML files")
    print(f"🔧 Removed {total_replacements} escaped characters total")
    
    if total_replacements > 0:
        print(f"\n📝 What was fixed:")
        print(f"  • Removed literal '\\1' characters from HTML")
        print(f"  • Fixed escaped '\\n' in meta tags")
        print(f"  • Cleaned up regex artifacts from optimization script")
        
        print(f"\n✅ All pages should now display correctly!")
        print(f"📱 The \\n and \\1 characters should no longer appear on screen")
    else:
        print(f"\n✅ No escaped characters found - files are already clean!")

if __name__ == "__main__":
    fix_escaped_characters()
