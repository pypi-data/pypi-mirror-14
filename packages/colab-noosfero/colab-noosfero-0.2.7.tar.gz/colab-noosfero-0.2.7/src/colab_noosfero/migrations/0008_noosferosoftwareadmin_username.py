# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('colab_noosfero', '0007_noosferosoftwarecommunity'),
    ]

    operations = [
        migrations.AddField(
            model_name='noosferosoftwareadmin',
            name='username',
            field=models.CharField(default='username', max_length=255),
            preserve_default=False,
        ),
    ]
