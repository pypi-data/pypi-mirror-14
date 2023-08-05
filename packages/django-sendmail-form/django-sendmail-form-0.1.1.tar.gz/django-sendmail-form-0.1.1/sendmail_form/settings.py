# coding: utf-8
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import ugettext_lazy as _

__all__ = ("SITE_NAME", "SENDMAILFORM_FROM_EMAIL", "SENDMAILFORM_TO_EMAIL",
           "MAIN_MIRROR", "SENDMAILFORM_THREADED")


try:
    SITE_NAME = settings.SITE_NAME
except AttributeError:
    raise ImproperlyConfigured(_("You should set your SITE_NAME in your"
                                 " settings.py, e.g: example.com"))

try:
    SENDMAILFORM_FROM_EMAIL = settings.SENDMAILFORM_FROM_EMAIL
except AttributeError:
    try:
        SENDMAILFORM_FROM_EMAIL = settings.DEFAULT_FROM_EMAIL
    except AttributeError:
        raise ImproperlyConfigured(_("You should set either"
                                     " SENDMAILFORM_FROM_EMAIL or"
                                     " DEFAULT_FROM_EMAIL in your settings.py"))

try:
    SENDMAILFORM_TO_EMAIL = settings.SENDMAILFORM_TO_EMAIL
except AttributeError:
    raise ImproperlyConfigured(_("You should set"
                                 " SENDMAILFORM_TO_EMAIL in your settings.py"))

MAIN_MIRROR = getattr(settings, "MAIN_MIRROR", "http://{}".format(SITE_NAME))

SENDMAILFORM_THREADED = getattr(settings, "SENDMAILFORM_THREADED", True)