# -- coding: utf-8 --
from django.db import models
from datetime import date
from django.utils.encoding import python_2_unicode_compatible

@python_2_unicode_compatible
class Campania (models.Model):
  descripcion = models.CharField('Descripción',max_length=100)
  fecha_inicio = DateField('Fecha de inicio', default=date.today)
  fecha_fin = DateField('Fecha de fin')
  def __str__(self):
    return self.descripcion

