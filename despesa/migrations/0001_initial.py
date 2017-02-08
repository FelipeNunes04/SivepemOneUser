# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Despesa',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('gasolina', models.FloatField()),
                ('comida', models.FloatField()),
                ('outros', models.FloatField()),
                ('data_despesa', models.DateField(auto_now_add=True)),
            ],
        ),
    ]
