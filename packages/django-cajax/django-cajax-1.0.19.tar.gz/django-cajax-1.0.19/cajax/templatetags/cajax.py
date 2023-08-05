# -.- coding: utf-8  -.-
from django import template
from django.template.loader import render_to_string

register = template.Library()

@register.simple_tag
def cajax(token):
	return render_to_string('cajax.js', {'csrf_token': token})
