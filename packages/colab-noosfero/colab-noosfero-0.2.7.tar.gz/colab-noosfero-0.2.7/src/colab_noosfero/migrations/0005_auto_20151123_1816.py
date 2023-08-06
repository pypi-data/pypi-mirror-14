# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('colab_noosfero', '0004_auto_20151112_1322'),
    ]

    operations = [
        migrations.CreateModel(
            name='NoosferoSoftwareAdmin',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name': 'Noosfero Admin',
                'verbose_name_plural': 'Noosfero Admins',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='noosferocommunity',
            name='admins',
            field=models.ManyToManyField(to='colab_noosfero.NoosferoSoftwareAdmin'),
            preserve_default=True,
        ),
    ]
