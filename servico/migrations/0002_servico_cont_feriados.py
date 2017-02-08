# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('servico', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='servico',
            name='cont_feriados',
            field=models.IntegerField(default=0),
        ),
    ]
