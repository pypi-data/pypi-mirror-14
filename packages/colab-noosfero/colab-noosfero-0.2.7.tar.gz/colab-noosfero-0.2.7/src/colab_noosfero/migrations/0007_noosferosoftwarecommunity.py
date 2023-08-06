# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import colab_noosfero.models


class Migration(migrations.Migration):

    dependencies = [
        ('colab_noosfero', '0006_remove_noosferosoftwareadmin_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='NoosferoSoftwareCommunity',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('finality', models.CharField(max_length=255)),
                ('repository_link', models.CharField(max_length=255, null=True)),
                ('features', models.TextField(null=True)),
                ('license_info', models.CharField(max_length=255)),
                ('software_languages', colab_noosfero.models.ListField()),
                ('software_databases', colab_noosfero.models.ListField()),
                ('operating_system_names', colab_noosfero.models.ListField()),
                ('community', models.ForeignKey(to='colab_noosfero.NoosferoCommunity')),
            ],
            options={
                'verbose_name': 'Software Community',
                'verbose_name_plural': 'Software Communities',
            },
            bases=(models.Model,),
        ),
    ]
