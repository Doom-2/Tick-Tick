from django.db import models

from core.models import User


class TgUser(models.Model):
    class Meta:
        verbose_name = 'TgUser'
        verbose_name_plural = 'TgUsers'

    tg_chat_id = models.PositiveIntegerField(verbose_name='tg chat id')
    tg_user_name = models.CharField(verbose_name='tg user name', max_length=256, default=None)
    user = models.ForeignKey(User, verbose_name='user', on_delete=models.PROTECT, null=True)
    verification_code = models.CharField(max_length=20, null=True)
