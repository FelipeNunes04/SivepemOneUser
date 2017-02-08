# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('codigo', models.CharField(primary_key=True, serialize=False, verbose_name='Código', max_length=20)),
                ('nome', models.CharField(max_length=50)),
                ('cpf', models.ImageField(upload_to='cpfs')),
                ('telefone', models.CharField(max_length=20)),
                ('endereco', models.CharField(max_length=70)),
                ('limite', models.FloatField()),
                ('devendo', models.BooleanField(default=False)),
            ],
        ),
    ]
