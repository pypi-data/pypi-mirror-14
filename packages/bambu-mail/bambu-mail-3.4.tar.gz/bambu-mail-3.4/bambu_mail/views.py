from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.http import HttpResponseRedirect
from bambu_mail import shortcuts

def subscribe(request):
    """
    Takes POST data (``email`` and optional ``next`` fields), submitting the ``email`` field to
    the newsletter provider for subscription to a mailing list, and redirecting the user to the value
    of ``next`` (this can also be provided in the querystring), or the homepage if no follow-on URL is
    supplied, with a message in the ``django.contrib.messages`` queue to let them know it was successful.
    
    If the email address is invalid or the subscription process was unsuccessful, the user is redirected
    to the follow-on URL and a message placed in the ``django.contrib.messages`` queue letting them know
    what the issue was.
    """
    
    email = request.POST.get('email')
    next = request.POST.get('next', request.GET.get('next', '/'))
    valid = False
    
    if not email:
        messages.error(request, u'Please enter your email address')
    else:
        try:
            validate_email(email)
            valid = True
        except ValidationError:
            messages.error(request, u'Please enter a valid email address')
    
    if valid:
        shortcuts.subscribe(email, list_id = 'newsletter')
        messages.success(request, u'Thanks for subscribing to our newsletter.')
    
    return HttpResponseRedirect(next)