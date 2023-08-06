====================
feincms_richtextplus
====================

feincms_richtextplus is a feincms plugin that copies the functionality of 
the original RichTextContent, and adds TYPE_CHOICES configuration option

Convenient when you need to render RichText data using different templates
which you can pick from admin page

Installation
------------

1. Add "feincms_richtextplus" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = (
        ...
        'feincms_richtextplus',
    )

2. Create RichTextPlusContent for your Page model (or any other Base-derived 
   model) like this::

    from feincms_richtextplus.models import RichTextPlusContent
    # ...
    Page.create_content_type(SimpleTableContent, TYPE_CHOICES=(
        ('default', 'default richtextplus'),
        ('wrapped', 'wrapped data'),
        # ... (other TYPE_CHOICES)
    ))

3. Define templates for every TYPE_CHOICES entry, i.e.::
   project_dir/app/templates/content/richtextplus/default.html
   project_dir/app/templates/content/richtextplus/wrapped.html

4. Migrate Page
