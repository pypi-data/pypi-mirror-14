# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('colab_noosfero', '0003_auto_20151006_1946'),
    ]

    operations = [
        migrations.AddField(
            model_name='noosferoarticle',
            name='username',
            field=models.CharField(max_length=255, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='noosferocommunity',
            name='thumb_url',
            field=models.CharField(max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
    ]
