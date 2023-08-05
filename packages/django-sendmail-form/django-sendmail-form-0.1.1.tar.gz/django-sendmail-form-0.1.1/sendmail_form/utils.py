import threading

from django.core.mail import send_mail

from sendmail_form.settings import SENDMAILFORM_THREADED

__all__ = ("SendMailThread", "send_async_email")


class SendMailThread(threading.Thread):
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        threading.Thread.__init__(self)

    def run(self):
        send_mail(**self.kwargs)


def send_async_email(**kwargs):
    if SENDMAILFORM_THREADED:
        SendMailThread(**kwargs).start()
    else:
        send_mail(**kwargs)