from django.shortcuts import render_to_response
from django.template import RequestContext
import json

# Create your views here.
import importlib
from django.http import HttpResponse

def build_doc(request):
    try:
        from project.settings import API_OBJECT_LOCATION
        app, module, obj_name = API_OBJECT_LOCATION.split(".")
        module = importlib.import_module(app + "." + module)
        obj = getattr(module, obj_name)
        api_json = obj.top_level(request)
        api_json = json.loads(api_json.content)
        # print api_json
        return render_to_response('templates/index.html', {'api': {'data': api_json, 'name': obj.api_name}}, context_instance=RequestContext(request))
    except ImportError:
        return HttpResponse("No donuts for you. You have to create API_OBJECT_LOCATION in settings.py")
