# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-11 01:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appencuesta', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='encuesta',
            name='hora_fin',
            field=models.DateTimeField(blank='true'),
        ),
        migrations.AlterField(
            model_name='encuesta',
            name='hora_inicio',
            field=models.DateTimeField(blank='true'),
        ),
    ]
