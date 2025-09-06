#!/usr/bin/env python3
"""
Comprehensive Bug and Performance Issue Checker
Scans all files for potential delays, bugs, and performance issues
"""

import os
import re
import glob
from pathlib import Path

def check_for_issues():
    """Check all files for potential bugs and performance issues"""
    
    script_dir = Path(__file__).parent
    issues_found = []
    
    print("🔍 Scanning for potential bugs and performance issues...\n")
    
    # Find all relevant files
    html_files = glob.glob(str(script_dir / "*.html"))
    js_files = glob.glob(str(script_dir / "*.js"))
    css_files = glob.glob(str(script_dir / "*.css"))
    
    # Skip backup and test files
    skip_files = ['.original.', 'test-mobile-performance.html', 'sitemap.html']
    html_files = [f for f in html_files if not any(skip in f for skip in skip_files)]
    
    print(f"📁 Checking {len(html_files)} HTML, {len(js_files)} JS, and {len(css_files)} CSS files\n")
    
    # Issues to check for
    performance_issues = [
        {
            'pattern': r'setTimeout\([^,]+,\s*([5-9]\d{2,}|\d{4,})\)',
            'description': 'Long setTimeout delays (>500ms) that could slow user experience',
            'severity': 'HIGH'
        },
        {
            'pattern': r'setInterval\([^,]+,\s*([1-9]\d{1,})\)',
            'description': 'Frequent setInterval calls (<100ms) that could cause performance issues',
            'severity': 'MEDIUM'
        },
        {
            'pattern': r'document\.write\(',
            'description': 'document.write() can block page rendering',
            'severity': 'HIGH'
        },
        {
            'pattern': r'@import\s+url\(',
            'description': 'CSS @import can block rendering and slow page load',
            'severity': 'MEDIUM'
        },
        {
            'pattern': r'pointer-events:\s*none.*!important',
            'description': 'Important pointer-events none that might break mobile touch',
            'severity': 'MEDIUM'
        },
        {
            'pattern': r'transition:\s*all\s+[1-9]\d*s',
            'description': 'Slow CSS transitions (>1s) that could feel laggy',
            'severity': 'LOW'
        },
        {
            'pattern': r'animation-duration:\s*[5-9]\d*s',
            'description': 'Very long animations that might annoy users',
            'severity': 'LOW'
        },
        {
            'pattern': r'\.preventDefault\(\)\s*;[^}]*return\s+false',
            'description': 'Both preventDefault and return false - redundant and potentially problematic',
            'severity': 'MEDIUM'
        }
    ]
    
    mobile_issues = [
        {
            'pattern': r'touch-action:\s*none',
            'description': 'touch-action: none might prevent scrolling on mobile',
            'severity': 'HIGH'
        },
        {
            'pattern': r'user-scalable\s*=\s*no',
            'description': 'user-scalable=no prevents zoom and hurts accessibility',
            'severity': 'MEDIUM'
        },
        {
            'pattern': r'min-height:\s*\d+px.*max-width:\s*768px',
            'description': 'Fixed heights on mobile can cause layout issues',
            'severity': 'LOW'
        },
        {
            'pattern': r'font-size:\s*[1-9][0-4]px.*max-width:\s*768px',
            'description': 'Font sizes below 15px on mobile might cause zoom on iOS',
            'severity': 'MEDIUM'
        }
    ]
    
    bug_patterns = [
        {
            'pattern': r'console\.log\(',
            'description': 'Console.log statements should be removed in production',
            'severity': 'LOW'
        },
        {
            'pattern': r'alert\(',
            'description': 'Alert dialogs can break mobile user experience',
            'severity': 'MEDIUM'
        },
        {
            'pattern': r'href\s*=\s*["\']javascript:',
            'description': 'javascript: hrefs can cause accessibility issues',
            'severity': 'LOW'
        },
        {
            'pattern': r'onclick\s*=',
            'description': 'Inline onclick handlers - better to use addEventListener',
            'severity': 'LOW'
        }
    ]
    
    all_issues = performance_issues + mobile_issues + bug_patterns
    
    # Check each file
    for file_path in html_files + js_files + css_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            file_issues = []
            
            for issue in all_issues:
                matches = re.finditer(issue['pattern'], content, re.IGNORECASE)
                for match in matches:
                    line_num = content[:match.start()].count('\\n') + 1
                    file_issues.append({
                        'file': os.path.basename(file_path),
                        'line': line_num,
                        'description': issue['description'],
                        'severity': issue['severity'],
                        'match': match.group(0)[:50] + '...' if len(match.group(0)) > 50 else match.group(0)
                    })
            
            if file_issues:
                issues_found.extend(file_issues)
                
        except Exception as e:
            print(f"❌ Error checking {os.path.basename(file_path)}: {e}")
    
    # Check for specific rep team box mobile issues
    print("🏀 Checking rep team box mobile functionality...\n")
    
    rep_team_issues = []
    for html_file in html_files:
        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check if rep team box exists
            if 'rep-team-box' in content:
                # Check if mobile touch is properly enabled
                if 'pointer-events: none' in content and 'rep-team-box' in content:
                    mobile_media_query = re.search(r'@media.*max-width:\s*768px.*?\{(.*?)\}', content, re.DOTALL)
                    if mobile_media_query and 'pointer-events: none' in mobile_media_query.group(1):
                        rep_team_issues.append({
                            'file': os.path.basename(html_file),
                            'issue': 'Rep team box has pointer-events: none on mobile',
                            'severity': 'HIGH'
                        })
        except Exception as e:
            continue
    
    # Report findings
    print("=" * 60)
    print("📋 ISSUE SUMMARY")
    print("=" * 60)
    
    if not issues_found and not rep_team_issues:
        print("✅ No significant issues found!")
        print("🚀 All files appear to be optimized for performance")
        return
    
    # Group issues by severity
    high_issues = [i for i in issues_found if i['severity'] == 'HIGH'] + rep_team_issues
    medium_issues = [i for i in issues_found if i['severity'] == 'MEDIUM']
    low_issues = [i for i in issues_found if i['severity'] == 'LOW']
    
    if high_issues:
        print("🚨 HIGH SEVERITY ISSUES (Need immediate attention):")
        for issue in high_issues:
            if 'file' in issue and 'line' in issue:
                print(f"  📄 {issue['file']}:{issue['line']}")
                print(f"     {issue['description']}")
                print(f"     Code: {issue['match']}")
            else:
                print(f"  📄 {issue['file']}")
                print(f"     {issue['issue']}")
            print()
    
    if medium_issues:
        print("⚠️ MEDIUM SEVERITY ISSUES (Should be addressed):")
        for issue in medium_issues:
            print(f"  📄 {issue['file']}:{issue['line']}")
            print(f"     {issue['description']}")
            print(f"     Code: {issue['match']}")
            print()
    
    if low_issues:
        print("💡 LOW SEVERITY ISSUES (Consider addressing):")
        for issue in low_issues:
            print(f"  📄 {issue['file']}:{issue['line']}")
            print(f"     {issue['description']}")
            print()
    
    print(f"📊 Total issues found: {len(issues_found + rep_team_issues)}")
    print(f"   🚨 High: {len(high_issues)}")
    print(f"   ⚠️ Medium: {len(medium_issues)}")
    print(f"   💡 Low: {len(low_issues)}")
    
    # Recommendations
    print("\\n" + "=" * 60)
    print("💡 RECOMMENDATIONS")
    print("=" * 60)
    
    if high_issues:
        print("🔥 URGENT FIXES NEEDED:")
        print("  • Fix rep team box mobile touch issues immediately")
        print("  • Remove any blocking setTimeout/setInterval calls")
        print("  • Fix touch-action and pointer-events on mobile")
        print()
    
    if medium_issues:
        print("🔧 PERFORMANCE IMPROVEMENTS:")
        print("  • Replace @import with <link> tags")
        print("  • Remove alert() dialogs")
        print("  • Optimize font sizes for mobile (minimum 16px)")
        print()
    
    print("✅ GENERAL OPTIMIZATIONS:")
    print("  • Remove console.log statements")
    print("  • Replace inline event handlers with addEventListener")
    print("  • Test all touch interactions on real mobile devices")
    print("  • Verify rep team box leads to rep-teams.html on mobile")

if __name__ == "__main__":
    check_for_issues()
