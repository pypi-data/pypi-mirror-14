A Django app to generate a simple and automatic api documentation with Tastypie.

Installation
============
::

  pip install django-tastypie-simple-api-doc


Usage
============

First, add this to installed app and django_markup (we use this package to format classes docstrings). 

::

	INSTALLED_APPS = (
		'tastypie_api_doc',
		'django_markup',
	)

Then you need to tell me where is your Tastypie Api object that will be documented. Put it's path in *settings.py* like this:

::

  API_OBJECT_LOCATION = "app.module.object_name"


In my test project was like this:

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

This is a work in progress but it can be already used in your projects. So, stay tuned. Feel free to contribute to get this app way more better. =D
