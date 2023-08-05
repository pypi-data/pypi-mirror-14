#~*~ coding: utf-8 ~*~
from django.conf import settings


def virtenviro_context_processor(request):
    context = {'settings': settings}
    return context