# coding: utf-8
from __future__ import unicode_literals

import warnings

from django import forms
from django.core.urlresolvers import reverse
from django.core.exceptions import DjangoRuntimeWarning
from django.utils.html import strip_tags
from django.utils.translation import ugettext_lazy as _

from sendmail_form import settings
from sendmail_form.utils import send_async_email

__all__ = ("SendMailFormMixin",)


class SendMailFormMixin(object):
    mail_template = _("Admin link: <a href='{admin_link}'>{admin_link}</a><br>"
                      "{fields}")

    field_template = "{title}: {value}<br>"

    subject_template = _("Feedback on {site_name}")
    message_template = _("Somebody left a message on {site}.<br>"
                         "You can read it in admin panel.<br>"
                         "{message}")

    def __init__(self, *args, **kwargs):
        super(SendMailFormMixin, self).__init__(*args, **kwargs)
        if 'subject_template' not in self.__dict__:
            warnings.warn("You have not set `subject_template` attribute"
                          " of class `{}`. Are you okay with"
                          " the default value?".format(type(self).__name__),
                          DjangoRuntimeWarning)

        if 'message_template' not in self.__dict__:
            warnings.warn("You have not set `message_template` attribute"
                          " of class `{}`. Are you okay with"
                          " the default value?".format(type(self).__name__),
                          DjangoRuntimeWarning)

    def save(self, commit=True):
        is_send_mail = not self.instance.pk
        instance = super(SendMailFormMixin, self).save(commit=True)
        if is_send_mail:
            admin_url = reverse(
                'admin:{}_{}_change'.format(instance._meta.app_label,
                                            instance._meta.model_name),
                args=[instance.pk]
            )
            admin_link = settings.MAIN_MIRROR + admin_url

            rendered_field_values = ""
            for key, field in self.fields.items():
                    value = self.cleaned_data[key]
                    if isinstance(field, forms.BooleanField):
                        value = value and _("Yes") or _("No")
                    rendered_field_values += self.field_template.format(
                        title=field.label, value=value)

            mail_text = self.mail_template.format(admin_link=admin_link,
                                                  fields=rendered_field_values)
            message = self.message_template.format(site=settings.SITE_NAME,
                                                   message=mail_text)
            subject = self.subject_template.format(site_name=settings.SITE_NAME)

            send_async_email(subject=subject, message=strip_tags(message),
                             from_email=settings.SENDMAILFORM_FROM_EMAIL,
                             recipient_list=settings.SENDMAILFORM_TO_EMAIL,
                             fail_silently=True, html_message=message)
        return instance
