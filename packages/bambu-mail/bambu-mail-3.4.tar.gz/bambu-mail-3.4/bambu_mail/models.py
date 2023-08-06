from django.conf import settings

if 'bambu_saas' in settings.INSTALLED_APPS:
    from bambu_saas.signals import newsletter_optin
    from bambu_mail import receivers
    
    newsletter_optin.connect(receivers.newsletter_optin)