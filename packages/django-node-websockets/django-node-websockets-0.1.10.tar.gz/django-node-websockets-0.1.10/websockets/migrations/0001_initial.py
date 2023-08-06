# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('socket', models.CharField(max_length=255, null=True, blank=True)),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(null=True, blank=True)),
                ('link', models.CharField(max_length=255, null=True, blank=True)),
                ('link_text', models.CharField(max_length=255, null=True, blank=True)),
                ('tag', models.CharField(max_length=255, null=True, blank=True)),
                ('user', models.ForeignKey(related_name='messages', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
    ]
