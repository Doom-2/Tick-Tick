# Generated by Django 4.1.4 on 2023-02-02 21:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tguser',
            name='tg_user_id',
        ),
        migrations.AddField(
            model_name='tguser',
            name='tg_user_name',
            field=models.CharField(
                default=None, max_length=256, verbose_name='tg user name'
            ),
        ),
        migrations.AlterField(
            model_name='tguser',
            name='tg_chat_id',
            field=models.PositiveIntegerField(verbose_name='tg chat id'),
        ),
    ]