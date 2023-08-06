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

    def create_menu_item(self, **kwargs):
        """Create a random MenuItem."""
        defaults = {
            'label': self.get_random_string(),
            'slug': self.get_random_string(),
            'order': 0
        }
        defaults.update(kwargs)
        return MenuItem.objects.create(**defaults)

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
        print ''
        print form_data
        print menu_data
        print ''
        return ItemExtra.objects.create(item=menu, extra=form_data)


class TreeOrder(TreeNavExtTestCase):
    """

    """

    def setUp(self):
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


        '''
        self.create_menu_item(**{
            'parent': self.root,
            'label': 'Our Blog',
            'slug': 'our-blog',
            'order': 4,
        })
        self.create_menu_item(**{
            'parent': self.root,
            'label': 'Home',
            'slug': 'home',
            'order': 0,
        })
        self.child = self.create_menu_item(**{
            'parent': self.root,
            'label': 'About Us',
            'slug': 'about-us',
            'order': 9,
        })
        self.second_level = self.create_menu_item(**{
            'parent': self.child,
            'label': 'Second',
            'slug': 'second',
            'order': 0,
        })
        self.third_level = self.create_menu_item(**{
            'parent': self.second_level,
            'label': 'Third',
            'slug': 'third',
            'order': 0,
        })
        '''

    def test_root_menu(self):
        self.assertIsInstance(self.root, ItemExtra)

