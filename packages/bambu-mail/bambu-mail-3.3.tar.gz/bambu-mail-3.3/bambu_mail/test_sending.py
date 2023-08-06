from django.test import TestCase
from django.utils.timezone import now, utc
from bambu_mail.shortcuts import render_to_mail

class SendMailTest(TestCase):
    def setUp(self):
        pass
    
    def tearDown(self):
        pass
    
    def test_send(self):
        render_to_mail(
            u'Test email',
            'mail/test.txt',
            {
                'current_utc_time': now().replace(tzinfo = utc)
            },
            'test@example.com'
        )