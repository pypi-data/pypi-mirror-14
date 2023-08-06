# -*- coding: utf-8 -*-
import random
import string

from django.test import TestCase
from treenav.models import MenuItem

from treenavext.forms import COLORS, DefaultExtraMetaForm
from treenavext.models import ItemExtra


class TreeNavExtTestCase(TestCase):
    """Base test case for creating TreeNav data."""

    def get_random_string(self, length=10):
        return ''.join(random.choice(string.ascii_letters)
                       for x in range(length))

    def create_menu_item_extra(self, **kwargs):
        """Create a random MenuItem."""
        menu_data = {
            'label': self.get_random_string(),
            'slug': self.get_random_string(),
            'order': 0,
            'extra': {
                'height': random.randint(0, 900),
                'width': random.randint(0, 900),
                'color': random.choice(COLORS)[0],
                'title': self.get_random_string()
            }
        }
        menu_data.update(kwargs)
        form_data = menu_data.pop('extra')

        menu = MenuItem.objects.create(**menu_data)
        extra = ItemExtra.objects.create(item=menu, extra=form_data)
        return menu


class TreeOrder(TreeNavExtTestCase):
    def setUp(self):
        self.form = DefaultExtraMetaForm
        self.root = self.create_menu_item_extra(**{
            'label': 'Primary Navigation',
            'slug': 'primary-nav',
            'order': 0,
            'extra': {
                'height': random.randint(0, 900),
                'width': random.randint(0, 900),
                'color': random.choice(COLORS)[0],
                'title': self.get_random_string()
            }
        })
        self.menu1 = self.create_menu_item_extra(**{
            'parent': self.root,
            'label': 'Menu1',
            'slug': 'menu1',
            'order': 0,
            'extra': {
                'height': 100,
                'width': 200,
                'color': '#000000',
                'title': 'Menu Item 1'
            }
        })
        self.menu1_1 = self.create_menu_item_extra(**{
            'parent': self.menu1,
            'label': 'Menu1.1',
            'slug': 'menu1_1',
            'order': 0,
            'extra': {
                'height': 800,
                'width': 400,
                'color': '#FFFF00',
                'title': 'Menu Item 1.1'
            }
        })

    def test_root_menu(self):
        self.assertIsInstance(self.root, MenuItem)
        self.assertIsInstance(self.root.itemextra.extra, dict)
        form = self.form(self.root.itemextra.extra)
        self.assertEquals(form.is_valid(), True)

    def test_menu_item1(self):
        menu1 = MenuItem.objects.get(slug=self.menu1.slug)
        self.assertIsInstance(menu1, MenuItem)
        self.assertEquals(menu1.parent, self.root)
        self.assertIsInstance(menu1.itemextra, ItemExtra)
        self.assertIsInstance(menu1.itemextra.extra, dict)
        self.assertEquals(menu1.itemextra.extra['height'], 100)
        self.assertEquals(menu1.itemextra.extra['width'], 200)
        self.assertEquals(menu1.itemextra.extra['color'], '#000000')

        form = self.form(menu1.itemextra.extra)
        self.assertEquals(form.is_valid(), True)

    def test_menu_item1_1(self):
        menu1_1 = MenuItem.objects.get(slug=self.menu1_1.slug)
        self.assertIsInstance(menu1_1, MenuItem)
        self.assertEquals(menu1_1.parent, self.menu1)
        self.assertIsInstance(menu1_1.itemextra, ItemExtra)
        self.assertIsInstance(menu1_1.itemextra.extra, dict)
        self.assertEquals(menu1_1.itemextra.extra['height'], 800)
        self.assertEquals(menu1_1.itemextra.extra['width'], 400)
        self.assertEquals(menu1_1.itemextra.extra['color'], '#FFFF00')

        form = self.form(menu1_1.itemextra.extra)
        self.assertEquals(form.is_valid(), True)
