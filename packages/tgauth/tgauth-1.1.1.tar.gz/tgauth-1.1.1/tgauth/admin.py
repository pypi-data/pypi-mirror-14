from django.contrib import admin
from tgauth.models import TelegramKey,TempTelegramUser
admin.site.register(TelegramKey)
admin.site.register(TempTelegramUser)



