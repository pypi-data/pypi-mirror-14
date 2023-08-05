# -.- coding: utf-8  -.-
from os import path 

from django import template
from django.template.loader import render_to_string

register = template.Library()

@register.simple_tag
def cajax(token):
	file_path = path.normpath(path.join(path.dirname(path.abspath(__file__)), '../templates/cajax.js'))
	return render_to_string(file_path, {'csrf_token': token})
