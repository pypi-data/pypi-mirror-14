import logging
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from importlib import import_module

def render_to_mail_task(subject, template, context, recipient, fail_silently = False, headers = None):
    from django.contrib.auth.models import User
    from django.contrib.sites.models import Site

    if headers is None:
        headers = {}

    from_email = getattr(settings, 'DEFAULT_FROM_EMAIL')
    site = Site.objects.get_current()

    if isinstance(recipient, User):
        if recipient.email:
            recipients = [
                '%s <%s>' % (
                    recipient.get_full_name() or recipient.username,
                    recipient.email
                )
            ]
        else:
            raise Exception('Recipient does not have an email address')
    elif isinstance(recipient, (str, unicode)):
        recipients = [recipient]
    elif isinstance(recipient, (list, tuple)):
        recipients = []

        for rec in recipient:
            if isinstance(rec, User) and rec.email:
                recipients.append(
                    u'%s <%s>' % (
                        rec.get_full_name() or rec.username,
                        rec.email
                    )
                )
            elif isinstance(rec, (str, unicode)):
                recipients.append(rec)
            elif isinstance(rec, (list, tuple)):
                recipients.append(
                    u'%s: <%s>' % rec
                )

            if len(recipients) == 0:
                raise Exception('No recipients found with email addresses')
    else:
        raise Exception('recipient argument must be User, string, list or tuple')

    media_url = settings.MEDIA_URL
    static_url = getattr(settings, 'STATIC_URL', '/static')

    if media_url.startswith('//'):
        media_url = 'http:%s' % media_url
    elif not (media_url.startswith('http://') or media_url.startswith('https://')):
        media_url = 'http://%s%s' % (site.domain, media_url)

    if static_url.startswith('//'):
        static_url = 'http:%s' % static_url
    elif not (static_url.startswith('http://') or static_url.startswith('https://')):
        static_url = 'http://%s%s' % (site.domain, static_url)

    ctx = {
        'MEDIA_URL': media_url,
        'STATIC_URL': static_url,
        'SITE': site
    }

    ctx.update(context)
    ctx['body'] = render_to_string(template, ctx)

    email = EmailMultiAlternatives(
        subject,
        render_to_string('mail/base.txt', ctx),
        from_email, recipients, headers = headers
    )

    email.attach_alternative(
        render_to_string('mail/base.html', ctx),
        "text/html"
    )

    logger = logging.getLogger('bambu_mail')

    try:
        email.send()
    except:
        if not fail_silently:
            raise

def subscribe_task(email, **kwargs):
    provider = getattr(settings, 'NEWSLETTER_PROVIDER')
    module, dot, klass = provider.rpartition('.')
    ps = getattr(settings,
        'NEWSLETTER_SETTINGS', {
            klass: {}
        }
    ).get(klass)

    module = import_module(module)
    klass = getattr(module, klass)
    provider = klass(**ps)
    return provider.subscribe(email, **kwargs)

if 'djcelery' in settings.INSTALLED_APPS:
    from celery import task
    render_to_mail_task = task(render_to_mail_task)
    subscribe_task = task(subscribe_task)
