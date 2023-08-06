from bambu_mail.newsletter import ProviderBase
from django.conf import settings
from xmlrpclib import ServerProxy

API_URL = 'http://%s.api.mailchimp.com/1.3/'

class MailChimpProvider(ProviderBase):
    """
    Mailchimp provider that allows new signups to be automatically added to a Mailchimp list.
    
    :param email: The email address to add to the mailing list
    :param list_id: The mailing list to subscribe the user to (as defined in the ``NEWSLETTER_SETTINGS`` setting)
    :param kwargs: Additional arguments to be passed to the subscription system
    """
    
    def subscribe(self, email, list_id, **kwargs):
        key, dash, dc = self.settings.get('API_KEY', '').rpartition('-')
        if not key or not dc:
            raise Exception('Missing or invalid API key')
        
        url = API_URL % dc
        proxy = ServerProxy(url, allow_none = True)
        
        proxy.listSubscribe(
            key,
            self.settings.get('LIST_IDS', {}).get(list_id, None),
            email,
            *self.map_args('subscribe', **kwargs)
        )