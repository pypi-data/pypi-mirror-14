from django.shortcuts import render_to_response
from django.template import RequestContext
import json

# Create your views here.
import importlib
from django.http import HttpResponse
from django_markup.markup import formatter

def build_doc(request):
    try:
        from project.settings import API_OBJECT_LOCATION
        app, module, obj_name = API_OBJECT_LOCATION.split(".")
        module = importlib.import_module(app + "." + module)
        obj = getattr(module, obj_name)
        api_json = obj.top_level(request)
        api_json = json.loads(api_json.content)
        resources_docstrings = get_resources_docstrings(obj.__dict__['_registry'])
        resources_prepend_urls = get_resources_prepend_urls(obj.__dict__['_registry'])
        return render_to_response('index.html', {'api': {'data': api_json, 'name': obj.api_name,
                                                         'docstrings': resources_docstrings, 'prepend_urls': resources_prepend_urls}},
                                                            context_instance=RequestContext(request))
    except ImportError:
        return HttpResponse("No donuts for you. You have to create API_OBJECT_LOCATION in settings.py")


def get_resources_docstrings(resources):
    resources_docstrings = {}
    for key, value in resources.items():
        resources_docstrings[key] = formatter(value.__doc__.replace('<','&lt').replace('>','&gt'), filter_name='linebreaks') if value.__doc__ else "No docstring"
    return resources_docstrings

def get_resources_prepend_urls(resources):
    resources_prepend_urls = {}
    from django_markup.markup import formatter
    for key, value in resources.items():
        urls = value.prepend_urls()
        resources_prepend_urls[key] = []
        for u in urls:
            resources_prepend_urls[key].append(u.__dict__['name'])
    return resources_prepend_urls
