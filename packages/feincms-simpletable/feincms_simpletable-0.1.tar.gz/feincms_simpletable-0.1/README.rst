===================
feincms_simpletable
===================

feincms_simpletable is a feincms plugin that adds a new content type for 
tables. Just copy-paste your data from Calc or Office spreadsheet into
SimpleTableContent in admin, and it will be automatically converted
to html and rendered as such on your website

**Current limitation**: merged cells are not supported

Quick start
-----------

1. Add "feincms_simpletable" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = (
        ...
        'feincms_simpletable',
    )

2. If you intend to use it as feincms content type, register SimpleTableContent 
   for your Page model (or any other Base-derived model) like this::

    from feincms_simpletable.models import SimpleTableContent
    # ...
    Page.create_content_type(SimpleTableContent)


3. If you want to add SimpleTable fields to your existing models, simply 
   subclass it::

    class Product(Base, SimpleTable):
        # ...

3. Migrate your models

Usage
-----

1. Add a SimpleTableContent to any feincms page in admin, then add data 
   by copying it from your Calc or Excel spreadsheet into content field

2. Models inheriting from SimpleTable are editable just like any other 
   django model
