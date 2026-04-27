import os
import re

templates_dir = r"c:\Users\asus\Desktop\VollProjeler\vollwebsite\templates"

# Regex pattern for attributes containing 'assets/...'
# e.g., src="assets/... " or data-background="assets/..." or href="assets/..."
pattern = re.compile(r'=(["\'])assets/(.*?)\1')

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content
    
    # Check if we need to add {% load static %}
    # If the file contains {% static ... %} or we are going to add it, we must have {% load static %}
    # Try finding an existing {% load static %}
    has_load_static = '{% load static %}' in content or '{%load static%}' in content
    
    # Replace the assets references
    new_content, count = pattern.subn(r'="\1{% static \'\2\' %}\1"', content)
    # Actually wait, the backref for \1 inside raw string:
    # r'="\1' -> no wait, it should just be:
    # If quote was \1, replacement: '="' + '{% static \'' + r'\2' + '\' %}' + '"'
    # Actually, a better approach using a function
    pass

def replacement_func(match):
    quote = match.group(1)
    path = match.group(2)
    return f'={quote}{{% static \'{path}\' %}}{quote}'

for filename in os.listdir(templates_dir):
    if filename.endswith(".html"):
        filepath = os.path.join(templates_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        has_load_static = '{% load static %}' in content
        
        # apply substitutions
        new_content, count = pattern.subn(replacement_func, content)
        
        if '<!doctype html>' in new_content.lower() and not has_load_static and (count > 0 or '{% static' in new_content):
            # insert {% load static %} right after doctype
            new_content = re.sub(r'(<!doctype html.*?>)', r'\1\n{% load static %}', new_content, flags=re.IGNORECASE)
        elif not has_load_static and (count > 0 or '{% static' in new_content):
            new_content = '{% load static %}\n' + new_content
            
        if new_content != content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Updated {filename} (replaced {count} matches)")

