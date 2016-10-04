# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-02 22:03
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Campania',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.CharField(max_length=100, verbose_name='Descripción')),
                ('fecha_inicio', models.DateField(default=datetime.date.today, verbose_name='Fecha de inicio')),
                ('fecha_fin', models.DateField(verbose_name='Fecha de fin')),
            ],
        ),
    ]