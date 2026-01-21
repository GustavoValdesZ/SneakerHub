import os
import django
from django.conf import settings
from django.template import Template, Context
from django import forms

# Minimal Django setup
if not settings.configured:
    settings.configure(
        TEMPLATES=[{
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [],
        }]
    )
    django.setup()

class FakeField:
    def __init__(self, label, id_for_label):
        self.label = label
        self.id_for_label = id_for_label
    def __str__(self):
        return "<input>"

# Read the actual template line
filepath = r'c:\Users\gusta\.gemini\antigravity\scratch\sneakers-shop\shop\templates\shop\register.html'
with open(filepath, 'r', encoding='utf-8') as f:
    lines = f.readlines()
    # The line in question is around 26-27
    target_line = ""
    for line in lines:
        if 'field.label' in line:
            target_line = line
            break

print(f"Original line: {repr(target_line)}")

# Try to render it
template_string = "{% for field in form %}" + target_line + "{% endfor %}"
t = Template(template_string)
c = Context({'form': [FakeField("Nombre", "id_nombre")]})
rendered = t.render(c)
print(f"Rendered: {repr(rendered)}")

# Check for hidden characters
for i, char in enumerate(target_line):
    print(f"Pos {i}: {char} (hex: {hex(ord(char))})")
