import json
from django.http import HttpResponse
from django.template.loader import render_to_string

from cajax.utils import get_secure_html

class Cajax(object):

    __http_response = None
    __string_response = ""
    __request = None

    def __init__(self, request):
        self.data = json.loads(request.POST['data'])
        self.__http_response = HttpResponse()
        self.__request = request

    def get_response(self):
        self.__http_response.write(self.__string_response)
        return self.__http_response

    def clean(self):
        self.__string_response = ""
        self.__http_response = HttpResponse()

    def script(self, code):
        self.__string_response += code

    def redirect(self, url):
        self.clean()
        self.script('document.location.href=\''+ url +'\';')

    def show(self, id):
        self.script('$(\''+ id +'\').show();')

    def hide(self, id):
        self.script('$(\''+ id +'\').hide();')

    def prepend(self, id, value):
        self.script('$(\''+ id +'\').prepend(\''+ get_secure_html(value) +'\');')

    def append(self, id, value):
        self.script('$(\''+ id +'\').append(\''+ get_secure_html(value) +'\');')

    def assign(self, id, attibute, value):
        self.script('$(\''+ id +'\').prop(\''+ attribute +'\', \'' + value +'\');')

    def add_css_class(self, id, value):
        self.script('$(\''+ id +'\').addClass(\''+ value +'\');')

    def remove_css_class(self, id, value):
        self.script('$(\''+ id +'\').removeClass(\''+ value +'\');')

    def html(self, id, value):
        self.script('$(\''+ id +'\').html(\''+ get_secure_html(value) +'\');')

    def render(self, id, template, context={}):
        self.html(id, render_to_string(template, context=context, request=self.__request))
