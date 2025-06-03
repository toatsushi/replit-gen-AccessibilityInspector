#!/usr/bin/env python3
"""
Script to add version information to all WCAG criteria entries
"""

import re

def update_wcag_criteria():
    with open('wcag_criteria.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Pattern to find criteria definitions that don't have versions
    pattern = r'(\s+"[^"]+": \{\s*\n\s+"id": "[^"]+",\s*\n\s+"title": "[^"]+",\s*\n\s+"level": "[^"]+",)(\s*\n\s+"description":)'
    
    # Replacement to add versions line
    replacement = r'\1\n        "versions": ["2.0", "2.1", "2.2"],\2'
    
    updated_content = re.sub(pattern, replacement, content)
    
    with open('wcag_criteria.py', 'w', encoding='utf-8') as f:
        f.write(updated_content)
    
    print("Updated wcag_criteria.py with version information")

if __name__ == "__main__":
    update_wcag_criteria()