from bambu_mail.tasks import render_to_mail_task, subscribe_task
from django.conf import settings

def render_to_mail(subject, template, context, recipient, fail_silently = False, headers = None):
    """
    :param subject: The subject line of the email
    :param template: The name of the template to render the HTML email with
    :param context: The context data to pass to the template
    :param recipient: The email address or ``django.contrib.auth.User`` object to send the email to
    :param fail_silently: Set to ``True`` to avoid errors being raised by the sender
    :param headers: An optional dictionary of email headers

    This function acts as an alias to one of two functions, depending on your setup. If you use
    `Celery <http://www.celeryproject.org/>`_,
    this function will perform the compositing and sending of the email asynchronously. Otherwise
    the process will take place on the same thread.
    """

    if 'djcelery' in settings.INSTALLED_APPS:
        render_to_mail_task.delay(
            subject,
            template,
            context,
            recipient,
            fail_silently,
            headers
        )
    else:
        render_to_mail_task(
            subject,
            template,
            context,
            recipient,
            fail_silently,
            headers
        )

def subscribe(email, **kwargs):
    """
    :param email: The email address of the user to add to the mailing list
    :param kwargs: Keyword arguments to pass to the individual newsletter provider

    This function acts as an alias to one of two functions, depending on your setup. If you use
    `Celery <http://www.celeryproject.org/>`_,
    this function will perform the API calls asynchronously. Otherwise the process will take place
    on the same thread.
    """
    if 'djcelery' in settings.INSTALLED_APPS:
        subscribe_task.delay(
            email,
            **kwargs
        )
    else:
        subscribe_task(
            email,
            **kwargs
        )
