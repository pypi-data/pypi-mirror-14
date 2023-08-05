from django.conf import settings
from django.http import HttpResponseBadRequest, HttpResponseForbidden

from cajax.__core__ import Cajax

for x in settings.INSTALLED_APPS:  # import of all apps
    try:
        exec "from "+x+".cajax import *"
    except ImportError:
        pass

def cajax_view(request):
    if request.method == 'POST' and request.is_ajax():
        try:
            instance = Cajax(request)
            globals()[request.POST['url']](request, instance)
            return instance.get_response()
        except KeyError:
            return HttpResponseBadRequest()
    else:
        return HttpResponseForbidden()
