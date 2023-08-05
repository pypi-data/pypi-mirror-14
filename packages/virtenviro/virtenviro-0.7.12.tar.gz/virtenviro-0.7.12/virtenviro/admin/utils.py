# ~*~ coding: utf-8 ~*~
__author__ = 'Kamo Petrosyan'
from django.apps import apps


'''
This is the best way to accomplish what you want to do:

from django.apps import apps

app = apps.get_app('my_application_name')
for model in get_models(app):
    # do something with the model

In this example, model is the actual model, so you can do plenty of things with it:

for model in apps.get_models(app):
    new_object = model() # Create an instance of that model
    model.objects.filter(...) # Query the objects of that model
    model._meta.db_table # Get the name of the model in the database
    model._meta.verbose_name # Get a verbose name of the model
    # ...
'''


def get_apps():
    """
    Returns a list of all installed modules that contain models.
    """
    return apps.get_apps()


def get_models():
    return apps.get_models