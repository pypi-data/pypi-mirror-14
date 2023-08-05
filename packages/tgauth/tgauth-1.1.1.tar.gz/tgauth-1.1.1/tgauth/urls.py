
from django.conf import settings
from django.conf.urls.defaults import url
urlpatterns = [

	## Telegram authentication urls
    url(r'^tgauth/$','tgauth.views.tgauth',name='tgauth'),
    url(r'^validate/otp/(?P<otp_telegram>\w+)/$', 'tgauth.views.otptg', name='otptgoauth'),
    url(r'^telegram/success/$','tgauth.views.telegramsuccess',name='telegramsuccess'),
    
]
