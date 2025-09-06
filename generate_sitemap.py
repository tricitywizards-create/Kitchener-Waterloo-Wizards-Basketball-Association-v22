#!/usr/bin/env python3
"""
Sitemap Generator for Kitchener-Waterloo Wizards Basketball Association
This script automatically generates both XML and HTML sitemaps based on HTML files in the directory.

Usage:
    python3 generate_sitemap.py

The script will:
1. Scan for all HTML files in the current directory
2. Generate an XML sitemap for search engines
3. Update the HTML sitemap with new pages
4. Set appropriate priorities and change frequencies based on page type
"""

import os
import datetime
from pathlib import Path
import xml.etree.ElementTree as ET
from xml.dom import minidom

# Configuration
DOMAIN = "https://kitchener-waterloo-wizards.com"
CURRENT_DIR = Path(__file__).parent

# Page priorities and change frequencies based on content type
PAGE_CONFIG = {
    'index.html': {'priority': '1.0', 'changefreq': 'weekly', 'description': 'Welcome to the Wizards - Magic on the Court!', 'icon': '🏠', 'category': 'Main Pages'},
    'about.html': {'priority': '0.9', 'changefreq': 'monthly', 'description': 'Learn about our basketball association and mission', 'icon': 'ℹ️', 'category': 'Main Pages'},
    'registration.html': {'priority': '0.9', 'changefreq': 'weekly', 'description': 'Sign up for programs and teams', 'icon': '📝', 'category': 'Registration & Events'},
    'rep-teams.html': {'priority': '0.8', 'changefreq': 'monthly', 'description': 'Competitive basketball teams and tryout information', 'icon': '🏆', 'category': 'Programs & Training'},
    'development.html': {'priority': '0.8', 'changefreq': 'monthly', 'description': 'Skill development programs for all ages', 'icon': '📈', 'category': 'Programs & Training'},
    'individual-training.html': {'priority': '0.7', 'changefreq': 'monthly', 'description': 'One-on-one coaching and personal development', 'icon': '👤', 'category': 'Programs & Training'},
    'upcoming-events.html': {'priority': '0.6', 'changefreq': 'weekly', 'description': 'Games, tournaments, and special events', 'icon': '📅', 'category': 'Registration & Events'},
    'photo-gallery.html': {'priority': '0.5', 'changefreq': 'monthly', 'description': 'Photos from games, events, and team activities', 'icon': '📷', 'category': 'Media'},
    'u11-rep-tryouts-flyer.html': {'priority': '0.4', 'changefreq': 'yearly', 'description': 'Information about U11 rep team tryouts', 'icon': '🔥', 'category': 'Registration & Events'},
    'sitemap.html': {'priority': '0.3', 'changefreq': 'monthly', 'description': 'Complete site navigation and page directory', 'icon': '🗺️', 'category': 'Navigation'}
}

# Default configuration for new pages
DEFAULT_CONFIG = {'priority': '0.5', 'changefreq': 'monthly', 'description': 'Basketball association page', 'icon': '🏀', 'category': 'Other Pages'}

def get_html_files():
    """Get all HTML files in the current directory."""
    html_files = []
    # Files to exclude from sitemap
    excluded_files = {
        'sitemap.html',  # Don't include the sitemap itself
        'index-mobile-optimized.html',  # Mobile variants should not be in sitemap
        'index-smooth-mobile.html',
        'index-ultra-mobile.html'
    }
    
    for file in CURRENT_DIR.glob('*.html'):
        if file.name not in excluded_files:
            html_files.append(file.name)
    return sorted(html_files)

def get_file_modified_date(filename):
    """Get the last modified date of a file."""
    try:
        timestamp = os.path.getmtime(CURRENT_DIR / filename)
        return datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
    except:
        return datetime.datetime.now().strftime('%Y-%m-%d')

def generate_xml_sitemap():
    """Generate XML sitemap for search engines."""
    print("🔄 Generating XML sitemap...")
    
    # Create root element
    urlset = ET.Element('urlset')
    urlset.set('xmlns', 'http://www.sitemaps.org/schemas/sitemap/0.9')
    urlset.set('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')
    urlset.set('xsi:schemaLocation', 'http://www.sitemaps.org/schemas/sitemap/0.9 http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd')
    
    html_files = get_html_files()
    
    for filename in html_files:
        config = PAGE_CONFIG.get(filename, DEFAULT_CONFIG)
        
        # Create URL element
        url = ET.SubElement(urlset, 'url')
        
        # Add location
        if filename == 'index.html':
            loc = ET.SubElement(url, 'loc')
            loc.text = f"{DOMAIN}/"
        else:
            loc = ET.SubElement(url, 'loc')
            loc.text = f"{DOMAIN}/{filename}"
        
        # Add last modified date
        lastmod = ET.SubElement(url, 'lastmod')
        lastmod.text = get_file_modified_date(filename)
        
        # Add change frequency
        changefreq = ET.SubElement(url, 'changefreq')
        changefreq.text = config['changefreq']
        
        # Add priority
        priority = ET.SubElement(url, 'priority')
        priority.text = config['priority']
    
    # Create pretty XML
    rough_string = ET.tostring(urlset, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    pretty_xml = reparsed.toprettyxml(indent='    ')
    
    # Remove empty lines and fix formatting
    lines = [line for line in pretty_xml.split('\\n') if line.strip()]
    pretty_xml = '\\n'.join(lines)
    
    # Write to file
    sitemap_path = CURRENT_DIR / 'sitemap.xml'
    with open(sitemap_path, 'w', encoding='utf-8') as f:
        f.write(pretty_xml)
    
    print(f"✅ XML sitemap generated with {len(html_files)} pages")
    return html_files

def generate_html_sitemap(html_files):
    """Generate HTML sitemap for users."""
    print("🔄 Generating HTML sitemap...")
    
    # Group pages by category
    categories = {}
    for filename in html_files:
        config = PAGE_CONFIG.get(filename, DEFAULT_CONFIG)
        category = config['category']
        if category not in categories:
            categories[category] = []
        categories[category].append({
            'filename': filename,
            'config': config
        })
    
    # Generate category sections
    category_sections = []
    
    # Define category order and icons
    category_info = {
        'Main Pages': '🏠',
        'Programs & Training': '🏀',
        'Registration & Events': '📝',
        'Media': '📸',
        'Navigation': '🗺️',
        'Other Pages': '📄'
    }
    
    for category_name in category_info.keys():
        if category_name in categories:
            category_icon = category_info[category_name]
            pages = categories[category_name]
            
            # Sort pages by priority (highest first)
            pages.sort(key=lambda x: float(x['config']['priority']), reverse=True)
            
            page_links = []
            for page in pages:
                filename = page['filename']
                config = page['config']
                
                # Determine the href
                if filename == 'index.html':
                    href = 'index.html'
                else:
                    href = filename
                
                # Create nice title from filename
                if filename in PAGE_CONFIG:
                    title = {
                        'index.html': 'Homepage',
                        'about.html': 'About Us',
                        'registration.html': 'Registration',
                        'rep-teams.html': 'Rep Teams',
                        'development.html': 'Development Program',
                        'individual-training.html': 'Individual Training',
                        'upcoming-events.html': 'Upcoming Events',
                        'photo-gallery.html': 'Photo Gallery',
                        'u11-rep-tryouts-flyer.html': 'U11 Rep Tryouts',
                        'sitemap.html': 'Site Map'
                    }.get(filename, filename.replace('.html', '').replace('-', ' ').title())
                else:
                    title = filename.replace('.html', '').replace('-', ' ').title()
                
                page_links.append(f'''                    <li>
                        <a href="{href}">
                            <span class="page-icon">{config['icon']}</span>
                            <div>
                                <strong>{title}</strong>
                                <div class="page-description">{config['description']}</div>
                            </div>
                        </a>
                    </li>''')
            
            category_sections.append(f'''            <!-- {category_name} -->
            <div class="page-category">
                <h2 class="category-title">{category_icon} {category_name}</h2>
                <ul class="page-list">
{chr(10).join(page_links)}
                </ul>
            </div>''')
    
    # Read the existing sitemap.html template or create it
    sitemap_html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Complete sitemap of Kitchener-Waterloo Wizards Basketball Association website - find all our pages and services.">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="https://kitchener-waterloo-wizards.com/sitemap.html">
    <link rel="icon" type="image/png" href="images/wizard-logo.png">
    <title>Site Map - Kitchener-Waterloo Wizards Basketball Association</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Arial', sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            color: #fff;
            line-height: 1.6;
            min-height: 100vh;
            padding: 2rem;
        }}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: rgba(0, 0, 0, 0.3);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 3rem;
            border: 1px solid rgba(137, 207, 240, 0.2);
        }}

        h1 {{
            color: #89CFF0;
            text-align: center;
            margin-bottom: 0.5rem;
            font-size: 2.5rem;
            text-shadow: 0 0 10px rgba(137, 207, 240, 0.3);
        }}

        .subtitle {{
            text-align: center;
            color: #ccc;
            margin-bottom: 3rem;
            font-size: 1.1rem;
        }}

        .last-updated {{
            text-align: center;
            color: #89CFF0;
            margin-bottom: 2rem;
            font-size: 0.9rem;
            opacity: 0.8;
        }}

        .sitemap-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 2rem;
            margin-bottom: 3rem;
        }}

        .page-category {{
            background: rgba(137, 207, 240, 0.1);
            border-radius: 10px;
            padding: 2rem;
            border: 1px solid rgba(137, 207, 240, 0.2);
            transition: all 0.3s ease;
        }}

        .page-category:hover {{
            transform: translateY(-5px);
            box-shadow: 0 10px 30px rgba(137, 207, 240, 0.2);
        }}

        .category-title {{
            color: #89CFF0;
            font-size: 1.4rem;
            margin-bottom: 1rem;
            padding-bottom: 0.5rem;
            border-bottom: 2px solid rgba(137, 207, 240, 0.3);
        }}

        .page-list {{
            list-style: none;
        }}

        .page-list li {{
            margin-bottom: 0.8rem;
        }}

        .page-list a {{
            color: #fff;
            text-decoration: none;
            display: flex;
            align-items: center;
            padding: 0.8rem;
            border-radius: 8px;
            transition: all 0.3s ease;
            background: rgba(255, 255, 255, 0.05);
        }}

        .page-list a:hover {{
            background: rgba(137, 207, 240, 0.2);
            color: #89CFF0;
            text-shadow: 0 0 5px rgba(137, 207, 240, 0.5);
            transform: translateX(10px);
        }}

        .page-icon {{
            margin-right: 0.8rem;
            font-size: 1.2rem;
            width: 24px;
            text-align: center;
        }}

        .page-description {{
            font-size: 0.9rem;
            color: #bbb;
            margin-top: 0.3rem;
            padding-left: 32px;
        }}

        .back-to-home {{
            text-align: center;
            margin-top: 2rem;
        }}

        .back-to-home a {{
            display: inline-block;
            background: linear-gradient(45deg, #89CFF0, #4a9eff);
            color: #fff;
            text-decoration: none;
            padding: 1rem 2rem;
            border-radius: 25px;
            font-weight: bold;
            transition: all 0.3s ease;
            box-shadow: 0 5px 15px rgba(137, 207, 240, 0.3);
        }}

        .back-to-home a:hover {{
            transform: translateY(-3px);
            box-shadow: 0 10px 25px rgba(137, 207, 240, 0.4);
        }}

        .page-count {{
            text-align: center;
            color: #89CFF0;
            margin-bottom: 1rem;
            font-size: 1rem;
        }}

        @media (max-width: 768px) {{
            body {{
                padding: 1rem;
            }}
            
            .container {{
                padding: 1.5rem;
            }}
            
            h1 {{
                font-size: 2rem;
            }}
            
            .sitemap-grid {{
                grid-template-columns: 1fr;
                gap: 1.5rem;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🏀 Site Map</h1>
        <p class="subtitle">Find everything on the Kitchener-Waterloo Wizards Basketball Association website</p>
        <p class="page-count">Total Pages: {len(html_files)}</p>
        <p class="last-updated">Last Updated: {datetime.datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
        
        <div class="sitemap-grid">
{chr(10).join(category_sections)}
        </div>

        <div class="back-to-home">
            <a href="index.html">← Back to Homepage</a>
        </div>
    </div>
</body>
</html>'''
    
    # Write HTML sitemap
    html_sitemap_path = CURRENT_DIR / 'sitemap.html'
    with open(html_sitemap_path, 'w', encoding='utf-8') as f:
        f.write(sitemap_html_content)
    
    print(f"✅ HTML sitemap generated with {len(html_files)} pages in {len(categories)} categories")

def main():
    """Main function to generate both sitemaps."""
    print("🏀 Kitchener-Waterloo Wizards Basketball Association")
    print("🗺️  Sitemap Generator")
    print("=" * 50)
    
    try:
        # Generate XML sitemap
        html_files = generate_xml_sitemap()
        
        # Generate HTML sitemap
        generate_html_sitemap(html_files)
        
        print("\\n✨ Sitemap generation completed successfully!")
        print(f"📁 Files generated:")
        print(f"   • sitemap.xml ({len(html_files)} pages)")
        print(f"   • sitemap.html (user-friendly version)")
        print(f"\\n🔗 Next steps:")
        print(f"   1. Upload these files to your website root directory")
        print(f"   2. Submit sitemap.xml to Google Search Console")
        print(f"   3. Link to sitemap.html from your main navigation if desired")
        print(f"\\n🌐 Sitemap URL: {DOMAIN}/sitemap.xml")
        
    except Exception as e:
        print(f"❌ Error generating sitemaps: {str(e)}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
