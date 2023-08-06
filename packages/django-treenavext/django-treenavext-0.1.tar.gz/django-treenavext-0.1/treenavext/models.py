# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings as site_settings
from formfield import ModelFormField
from treenav.models import MenuItem

extra_form = getattr(site_settings, "TREENAVEXT_EXTRA_FORM",
                     'treenavext.forms.DefaultExtraMetaForm')


class ItemExtra(models.Model):
    item = models.OneToOneField(MenuItem, on_delete=models.CASCADE,
                                primary_key=True)
    extra = ModelFormField(form=extra_form)
