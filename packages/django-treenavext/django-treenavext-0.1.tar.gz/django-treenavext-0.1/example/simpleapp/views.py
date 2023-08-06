# -*- coding: utf-8 -*-
from django.views.generic import ListView
from treenav.models import MenuItem


class MenuView(ListView):
    model = MenuItem
    template_name = 'simpleapp/index.html'

    def get_queryset(self):
        return MenuItem.objects.filter(parent=None).order_by('order')
