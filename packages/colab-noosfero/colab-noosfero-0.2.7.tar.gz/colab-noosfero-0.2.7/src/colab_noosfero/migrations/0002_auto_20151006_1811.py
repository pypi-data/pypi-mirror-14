# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('colab_noosfero', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='noosferocommunity',
            name='identifier',
            field=models.CharField(max_length=255),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='noosferocommunity',
            name='name',
            field=models.CharField(max_length=255),
            preserve_default=True,
        ),
    ]
