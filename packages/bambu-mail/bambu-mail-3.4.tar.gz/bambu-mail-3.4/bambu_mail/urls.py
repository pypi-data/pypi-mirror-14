from django.conf.urls import url
from bambu_mail.views import subscribe

urlpatterns = (
    url(r'^subscirbe/$', subscribe, name = 'newsletter_subscribe'),
)
