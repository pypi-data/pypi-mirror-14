
from __future__ import absolute_import, unicode_literals
from itertools import count

from django import forms
from django.contrib import admin
from django.core.exceptions import ImproperlyConfigured
from django.core.mail import send_mail
from django.db import models
from django.db.models import AutoField
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.conf import settings

from feincms.content.richtext.models import *

class RichTextPlusAdminForm(RichTextContentAdminForm):
    radio_fields = {'type': admin.VERTICAL}

    seen_tidy_warnings = forms.BooleanField(
        required=False,
        label=_("HTML Tidy"),
        help_text=_("Ignore the HTML validation warnings"),
        widget=forms.HiddenInput
    )

    def clean(self):
        cleaned_data = super().clean()

        if settings.FEINCMS_TIDY_HTML:
            text, errors, warnings = get_object(
                settings.FEINCMS_TIDY_FUNCTION)(cleaned_data['text'])

            # Ick, but we need to be able to update text and seen_tidy_warnings
            self.data = self.data.copy()

            # We always replace the HTML with the tidied version:
            cleaned_data['text'] = text
            self.data['%s-text' % self.prefix] = text

            if settings.FEINCMS_TIDY_SHOW_WARNINGS and (errors or warnings):
                if settings.FEINCMS_TIDY_ALLOW_WARNINGS_OVERRIDE:
                    # Convert the ignore input from hidden to Checkbox so the
                    # user can change it:
                    self.fields['seen_tidy_warnings'].widget =\
                        forms.CheckboxInput()

                if errors or not (
                        settings.FEINCMS_TIDY_ALLOW_WARNINGS_OVERRIDE
                        and cleaned_data['seen_tidy_warnings']):
                    self._errors["text"] = self.error_class([mark_safe(
                        _(
                            "HTML validation produced %(count)d warnings."
                            " Please review the updated content below before"
                            " continuing: %(messages)s"
                        ) % {
                            "count": len(warnings) + len(errors),
                            "messages": '<ul><li>%s</li></ul>' % (
                                "</li><li>".join(
                                    map(escape, errors + warnings))),
                        }
                    )])

                # If we're allowed to ignore warnings and we don't have any
                # errors we'll set our hidden form field to allow the user to
                # ignore warnings on the next submit:
                if (not errors
                        and settings.FEINCMS_TIDY_ALLOW_WARNINGS_OVERRIDE):
                    self.data["%s-seen_tidy_warnings" % self.prefix] = True

        return cleaned_data

class RichTextPlusContent(RichTextContent):
    class Meta:
        abstract = True
        verbose_name = _('RichText+')
        verbose_name_plural = _('RichTexts+')

    @classmethod
    def rt_to_rtplus(cls, bases):
        for base in bases:
            for p in base.objects.all(): 
                rts = p.content.all_of_type(RichTextContent)
                for rt in rts:
                    exclude = ('id', )
                    initial = dict(
                        (f.name, getattr(rt, f.name)) for f in rt._meta.fields
                        if not isinstance(f, AutoField) and f.name not in exclude
                        and f not in rt._meta.parents.values())
                    # print(initial)
                    rtplus_cls_concrete = base.content_type_for(cls)
                    try:
                        rtplus = rtplus_cls_concrete(**initial)
                    except TypeError:
                        raise ImproperlyConfigured(
                            '%s class has no %s attached to it' % (
                                base.__name__,
                                cls.__name__,
                                )
                            )
                    # rtplus = copy_model_instance(rt, exclude=('id'))
                    # rtplus.text = rt.text
                    # rtplus.id = None
                    # NOTE: replace with your default type
                    rtplus.type = 'default'
                    # save our new RichTextPlusContent with data from its original
                    # RichTextContent counterpart
                    rtplus.save() 
                    # delete original
                    rt.delete()



    @classmethod
    def initialize_type(cls, cleanse=None, TYPE_CHOICES=None):
        def to_instance_method(func):
            def func_im(self, *args, **kwargs):
                return func(*args, **kwargs)
            return func_im

        if cleanse:
            cls.cleanse = to_instance_method(cleanse)

        # TODO: Move this into somewhere more generic:
        if settings.FEINCMS_TIDY_HTML:
            # Make sure we can load the tidy function without dependency
            # failures:
            try:
                get_object(settings.FEINCMS_TIDY_FUNCTION)
            except ImportError as e:
                raise ImproperlyConfigured(
                    "FEINCMS_TIDY_HTML is enabled but the HTML tidy function"
                    " %s could not be imported: %s" % (
                        settings.FEINCMS_TIDY_FUNCTION, e))
        if TYPE_CHOICES is None:
            raise ImproperlyConfigured(
                'You have to set TYPE_CHOICES when'
                ' creating a %s' % cls.__name__)

        cls.add_to_class(
            'type',
            models.CharField(
                _('type'),
                max_length=20,
                choices=TYPE_CHOICES,
                default=TYPE_CHOICES[0][0],
            )
        )

    def render(self, **kwargs):
        ctx = {'content': self}
        ctx.update(kwargs)
        return render_to_string([
            'content/richtextplus/%s.html' % self.type,
            'content/richtextplus/default.html',
        ], ctx, context_instance=kwargs.get('context'))

