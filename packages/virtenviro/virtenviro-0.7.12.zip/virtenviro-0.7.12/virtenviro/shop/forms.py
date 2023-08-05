#~*~ coding: utf-8 ~*~
from django import forms
from virtenviro.shop.models import *


class SimpleXmlImportForm(forms.Form):
    # file to parse
    xml_file = forms.FileField()


