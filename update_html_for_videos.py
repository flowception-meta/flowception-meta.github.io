#!/usr/bin/env python3
"""
Updates index.html to use <video> tags instead of <img> tags for GIFs
Run this after converting GIFs to MP4/WebM
"""

import re
import sys

def convert_img_to_video(html_content):
    """Convert <img src="*.gif"> to <video> tags with MP4/WebM sources"""
    
    # Pattern to match img tags with .gif sources
    pattern = r'<img\s+src="([^"]+\.gif)"\s+alt="([^"]*)"\s+([^>]*)/>'
    
    def replace_with_video(match):
        gif_path = match.group(1)
        alt_text = match.group(2)
        attributes = match.group(3)
        
        # Generate video paths
        mp4_path = gif_path.replace('.gif', '.mp4')
        webm_path = gif_path.replace('.gif', '.webm')
        
        # Extract loading and other attributes
        loading_match = re.search(r'loading="([^"]*)"', attributes)
        loading = loading_match.group(1) if loading_match else 'lazy'
        
        fetchpriority_match = re.search(r'fetchpriority="([^"]*)"', attributes)
        fetchpriority = f' fetchpriority="{fetchpriority_match.group(1)}"' if fetchpriority_match else ''
        
        # Create video tag
        video_tag = f'''<video autoplay loop muted playsinline{fetchpriority} preload="{loading}">
            <source src="{webm_path}" type="video/webm">
            <source src="{mp4_path}" type="video/mp4">
            <!-- Fallback to GIF for older browsers -->
            <img src="{gif_path}" alt="{alt_text}" loading="{loading}"/>
          </video>'''
        
        return video_tag
    
    # Replace all img tags
    updated_html = re.sub(pattern, replace_with_video, html_content)
    
    return updated_html

def main():
    input_file = 'index.html'
    output_file = 'index.html.new'
    
    try:
        # Read original HTML
        with open(input_file, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Convert img tags to video tags
        updated_html = convert_img_to_video(html_content)
        
        # Count replacements
        gif_count = html_content.count('.gif"')
        
        # Write to new file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(updated_html)
        
        print(f"✓ Successfully updated HTML")
        print(f"✓ Found {gif_count} GIF references")
        print(f"✓ Output written to: {output_file}")
        print(f"\nNext steps:")
        print(f"1. Review the changes: diff index.html index.html.new")
        print(f"2. If satisfied, replace: mv index.html.new index.html")
        
    except FileNotFoundError:
        print(f"Error: {input_file} not found")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()

