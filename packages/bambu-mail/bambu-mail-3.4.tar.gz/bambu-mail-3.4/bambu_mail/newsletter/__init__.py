"""
A newsletter provider is a fairly simple class that exposes a ``subscribee()`` method. That method
calls an API to add the supplied email address to a mailing list. Which list to add the email address
to is determined by the value of the ``kwargs`` passed to that method. These should match settings
specified in the Django settings file for that newsletter provider.

The simplest way to setup a provider is to specify the following in your Django settings file:

>>> NEWSLETTER_SETTINGS = {
...     'API_KEY': 'mykey',
...     'LIST_IDS': {
...         'new_signup': '1234567890'
...     }
... }

The idea here is that the provider you use will translate the ``API_KEY`` argument to one which it
understands, and the same with the list IDs. That way you can refer to multiple mailing lists within your
application code without having to store the ID of that list in more than one place. Also, if you change
providers, you don't need to change anything other than the value of each item in the ``LIST_IDS`` dict.

"""

from copy import copy

class ProviderBase(object):
    """
    The provider class is instantiated by ``bambu_mail.shortcuts.subscribe``. Kwargs are gathered from
    the ``NEWSLETTER_SETTINGS`` variable within the Django settings file. Because Bambu Mail is
    provider agnostic, it's likely that one provider won't understand the kwargs of another, so a
    keyword argument of ``ARG_MAPPINGS`` can be set, where the key is the globally-recognised name for an
    argument, and the value is the name for that argument that only the specific provider understands.
    """
    
    def __init__(self, **kwargs):
        self.settings = copy(kwargs)
    
    def subscribe(self, email, **kwargs):
        raise NotImplementedError('Method not implemented.')
    
    def map_args(self, action, **kwargs):
        mappings = self.settings.get('ARG_MAPPING', {})
        result = [
            kwargs.get(mapping)
            for mapping in mappings.get(action)
        ]
        
        while len(result) > 0 and result[-1] is None:
            result.pop()
        
        return result