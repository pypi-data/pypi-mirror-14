A Django app to generate a simple and automatic api documentation with Tastypie.

Installation
============
::

  pip install django-tastypie-simple-api-doc


Usage
============

First, you need to tell me where is your Tastypie Api object that will be documented. Put it's path in *settings.py* like this:

::

  API_OBJECT_LOCATION = "app.module.object_name"


In mais test projetc was like this:

::

   API_OBJECT_LOCATION = "project.urls.v1_api"

Got it? Now go to your urls module and goes like this:

::

  from tastypie_api_doc.views import build_doc

  urlpatterns = [
    ...
    url(r'^choose_your_url', build_doc),
  ]


And....We are almost there. Now, you need to "collect your static" if you know what I mean. :P

::

   python manage.py collectstatic


And this is it. :)

For now, this django app just create a table with your Tastypie Endpoints. Feel free to contribute to get this app way more better. 
