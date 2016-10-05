# -- coding: utf-8 --
import uuid
from django.contrib.auth.models import User
from django.db import models
from datetime import date
from django.utils.encoding import python_2_unicode_compatible

@python_2_unicode_compatible
class Campania (models.Model):
  descripcion = models.CharField('Descripción',max_length=100)
  fecha_inicio = models.DateField('Fecha de inicio', default=date.today)
  fecha_fin = models.DateField('Fecha de fin')
  def __str__(self):
    return self.descripcion

@python_2_unicode_compatible
class Encuestador (models.Model):
  usuario = models.ForeignKey(User)

@python_2_unicode_compatible
class Parada (models.Model):
  numero = models.CharField('Número',max_length=10)

@python_2_unicode_compatible
class Encuesta (models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  encuestador = models.ForeignKey(Encuestador, on_delete= models.PROTECT)
  cargaonline = models.BooleanField('Encuesta cargada en línea',default=True)
  dia_realizada = models.DateField('fecha de realización', default=date.today)
  hora_inicio = models.DateTimeField()
  hora_fin = models.DateTimeField()
  
  
  
