# -*- coding: utf-8 -*-
from django.contrib import admin

from treenav.admin import MenuItemAdmin
from treenav.models import MenuItem

from .models import ItemExtra


class InlineExtraItemAdmin(admin.StackedInline):
    model = ItemExtra


class ExtraMenuItemAdmin(MenuItemAdmin):
    inlines = MenuItemAdmin.inlines + (InlineExtraItemAdmin,)


admin.site.unregister(MenuItem)
admin.site.register(MenuItem, ExtraMenuItemAdmin)
