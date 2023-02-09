from django.contrib import admin
from .models import TgUser


class TGUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'tg_user_name', 'tg_chat_id', 'verification_code')
    search_fields = ('tg_user_name', 'user__username')


admin.site.register(TgUser, TGUserAdmin)
