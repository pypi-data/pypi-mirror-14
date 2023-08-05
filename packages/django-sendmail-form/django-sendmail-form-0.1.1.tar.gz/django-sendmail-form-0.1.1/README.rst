=====
Django SendMail Form
=====

This Django app provides the ability to send an email containing info about an object, that is created using form.


Example
-----------

1. Install the package using pip::

    pip install django-sendmail-form

2. Add the "sendmail_form" to your INSTALLED_APPS setting::

    INSTALLED_APPS = (
        ...
        'sendmail_form',
    )

3. import the SendMailFormMixin::

    from sendmail_form.forms import SendMailFormMixin

4. Inherit your form::

    class MyForm(SendMailFormMixin, forms.ModelForm):
        ...
        subject_template = "My feedback on {site_name}"
        message_template = "Somebody left a message on {site}.<br>" \
                           "You can read it in admin panel.<br>" \
                           "{message}"

5. Have fun!