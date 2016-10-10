# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-10 17:23
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appencuesta', '0008_auto_20161010_0016'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='encuesta',
            name='destino_lugar',
        ),
        migrations.RemoveField(
            model_name='encuesta',
            name='destino_motivo',
        ),
        migrations.RemoveField(
            model_name='encuesta',
            name='encuestador',
        ),
        migrations.RemoveField(
            model_name='encuesta',
            name='linea',
        ),
        migrations.RemoveField(
            model_name='encuesta',
            name='origen_lugar',
        ),
        migrations.RemoveField(
            model_name='encuesta',
            name='origen_motivo',
        ),
        migrations.RemoveField(
            model_name='encuesta',
            name='parada_encuesta',
        ),
        migrations.DeleteModel(
            name='Encuesta',
        ),
    ]