# Generated by Django 4.1.4 on 2023-01-23 11:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('goals', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Board',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='is_deleted')),
            ],
            options={
                'verbose_name': 'Board',
                'verbose_name_plural': 'Boards',
            },
        ),
        migrations.AddField(
            model_name='goalcategory',
            name='board',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='categories',
                                    to='goals.board', verbose_name='board'),
        ),
        migrations.CreateModel(
            name='BoardParticipant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('role',
                 models.PositiveSmallIntegerField(choices=[(1, 'Owner'), (2, 'Writer'), (3, 'Reader')], default=1,
                                                  verbose_name='role')),
                ('board', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='participants',
                                            to='goals.board', verbose_name='board')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='participants',
                                           to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'verbose_name': 'Participant',
                'verbose_name_plural': 'Participants',
                'unique_together': {('board', 'user')},
            },
        ),
    ]
