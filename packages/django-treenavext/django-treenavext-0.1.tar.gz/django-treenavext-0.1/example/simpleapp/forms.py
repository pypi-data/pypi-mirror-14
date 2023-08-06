# -*- coding: utf-8 -*-
from django import forms


class ExtraMetaForm(forms.Form):
    num = forms.IntegerField()
    choice = forms.ChoiceField(choices=((1, 'male'), (2, 'female')),
                               required=False)
