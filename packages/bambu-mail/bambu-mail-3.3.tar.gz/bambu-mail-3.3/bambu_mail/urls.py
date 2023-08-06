from django.conf.urls import patterns, include, url

urlpatterns = patterns('bambu_mail.views',
    url(r'^subscirbe/$', 'subscribe', name = 'newsletter_subscribe')
)