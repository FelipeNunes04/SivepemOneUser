# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cliente', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pagamento',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('valor_pagamento', models.FloatField()),
                ('data_pagamento', models.DateField(auto_now_add=True, verbose_name='Data do pagamento')),
            ],
        ),
        migrations.CreateModel(
            name='ParcelaExtra',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('numero_parcela_extra', models.IntegerField()),
                ('valor_parcela_extra', models.DecimalField(max_digits=10, decimal_places=2)),
                ('servico', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Saldo',
            fields=[
                ('codigo', models.IntegerField(primary_key=True, default=1, serialize=False)),
                ('codigo_cliente', models.ForeignKey(to='cliente.Cliente')),
            ],
        ),
        migrations.CreateModel(
            name='Servico',
            fields=[
                ('codigo', models.CharField(primary_key=True, max_length=50, serialize=False)),
                ('valor_servico', models.FloatField()),
                ('juros', models.FloatField()),
                ('valor_total', models.FloatField()),
                ('numero_parcelas', models.IntegerField()),
                ('valor_parcela', models.FloatField()),
                ('tipo_parcelamento', models.CharField(choices=[('Diario', 'Diario'), ('Semanal', 'Semanal'), ('Quizenal', 'Quizenal'), ('Mensal', 'Mensal')], max_length=25)),
                ('data_servico', models.DateField(auto_now_add=True, verbose_name='Data do serviço')),
                ('vencimento_parcela', models.DateField(auto_now_add=True, verbose_name='Vencimento da Parcela')),
                ('vencimento_ultima_parcela', models.DateField(auto_now_add=True)),
                ('pago', models.BooleanField(default=False)),
                ('numero_parcelas_extra', models.IntegerField(default=0)),
                ('valor_parcela_extra', models.DecimalField(decimal_places=2, max_digits=10, default=0)),
                ('codigo_cliente', models.ForeignKey(to='cliente.Cliente', related_name='codigo_cliente')),
            ],
        ),
        migrations.AddField(
            model_name='pagamento',
            name='codigo_servico',
            field=models.ForeignKey(to='servico.Servico', related_name='codigo_servico'),
        ),
    ]
