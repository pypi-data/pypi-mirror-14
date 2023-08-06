# -*- coding: utf-8 -*-
from django import forms

COLORS = (
    ('#000000', 'Black'),
    ('#FF0000', 'Red'),
    ('#800000', 'Maroon'),
    ('#FFFF00', 'Yellow'),
)


class DefaultExtraMetaForm(forms.Form):
    height = forms.IntegerField()
    width = forms.IntegerField()
    color = forms.ChoiceField(choices=COLORS, required=False)
    title = forms.CharField()
