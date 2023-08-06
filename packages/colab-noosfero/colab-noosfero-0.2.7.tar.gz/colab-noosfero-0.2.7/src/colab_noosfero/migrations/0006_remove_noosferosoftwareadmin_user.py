# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('colab_noosfero', '0005_auto_20151123_1816'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='noosferosoftwareadmin',
            name='user',
        ),
    ]
