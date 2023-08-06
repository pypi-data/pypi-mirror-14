django-treenavext
=================

Addding extra features to the treenav project.


Settings:
---------

The following form shows up in the admin interface to extend the MenuItem of
 the *django-treenav* project. It  defaults to 'treenavext.forms
 .DefaultExtraMetaForm'


    TREENAVEXT_EXTRA_FORM = 'simpleapp.forms.ExtraMetaForm'



Installation
------------

Install the app with:

    cd django-treenavext

    python setup.py install


Settings
--------

Add to your INSTALLED_APPS and run syncdb:

    INSTALLED_APPS = (
        ...,
        'mptt',
        'treenav',
        'treenvext',
    )

