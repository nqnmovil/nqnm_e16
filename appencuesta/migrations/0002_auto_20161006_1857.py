# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-06 21:57
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('appencuesta', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Encuesta',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('cargaonline', models.BooleanField(default=True, verbose_name='Encuesta cargada en línea')),
                ('dia_realizada', models.DateField(default=datetime.date.today, verbose_name='fecha de realización')),
                ('hora_inicio', models.DateTimeField()),
                ('hora_fin', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Encuestador',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Parada',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero', models.CharField(max_length=10, verbose_name='Número')),
            ],
        ),
        migrations.AddField(
            model_name='encuesta',
            name='encuestador',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='appencuesta.Encuestador'),
        ),
    ]
