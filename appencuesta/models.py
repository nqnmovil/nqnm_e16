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
  def __str__(self):
    return self.numero

@python_2_unicode_compatible
class Linea (models.Model):
  nombre = models.CharField('nombre de la línea',max_length=10)
  def __str__(self):
    return self.nombre

@python_2_unicode_compatible
class Lugar (models.Model):
  #tipo de lugar
  ZONA= 'Z'
  HITO = 'H'
  PARADA = 'P'
  CALLE = 'C'
  BARRIO = 'B'
  TIPO_LUGAR = (
    (ZONA, 'Zona'),
    (HITO, 'Hito'),
    (PARADA, 'Parada'),
    (CALLE, 'Calle'),
    (BARRIO, 'Barrio')
  )
  tipo = models.CharField('Tipo de lugar',max_length=1, choices=TIPO_LUGAR, blank='true')
  nombre = models.CharField('Nombre del lugar',max_length=100)
  def __str__(self):
    return self.nombre

@python_2_unicode_compatible
class Motivo (models.Model):
  nombre = models.CharField('nombre del motivo',max_length=100)
  def __str__(self):
    return self.nombre
"""
@python_2_unicode_compatible
class Encuesta (models.Model):
  #calidad del servicio
  MUY_BUENO = 'MB'
  BUENO = 'BU'
  REGULAR = 'RE'
  MALO = 'MA'
  NS_NC = 'NS'
  CALIFICA_CALIDAD = (
    (MUY_BUENO, 'muy bueno'),
    (BUENO, 'bueno'),
    (REGULAR, 'regular'),
    (MALO, 'malo'),
    (NS_NC, 'Ns/Nc'),
  )
  #momento de la encuesta
  ANTES_ASCENDER = 'AA'
  LUEGO_DESCENDER = 'LD'
  MOMENTO = (
    (ANTES_ASCENDER, 'antes de ascender'),
    (LUEGO_DESCENDER, 'luego de descender'),
  )
  #sexo
  FEMENINO = 'F'
  MASCULINO = 'M'
  SEXO = (
    (FEMENINO, 'Femenino'),
    (MASCULINO, 'Masculino'),
  )
  #rango de edad
  JOVEN = 'JO'
  ADULTO = 'A1'
  ADULTO2 = 'A2'
  ADULTO_MAYOR = 'AM'
  RANGO_EDAD = (
    (JOVEN,'Jóven (18-25 años)'),
    (ADULTO,'Adulto (25-40 años)'),
    (ADULTO2,'Adulto II (40-60 años)'),
    (ADULTO_MAYOR,'Adulto mayor (más de 60 años)'),
  )
  #tipo de lugar
  ZONA= 'Z'
  HITO = 'H'
  PARADA = 'P'
  TIPO_LUGAR = (
    (ZONA, 'Zona'),
    (HITO, 'Hito'),
    (PARADA, 'Parada'),
  )
  #veces por semana
  TODOS_LOS_DIAS = 'TODOS'
  TRES_O_MAS = '3OMAS'
  MENOS_DE_TRES = 'MENOS3'
  VECES_SEMANA = (
    (TODOS_LOS_DIAS, 'Todos los días'),
    (TRES_O_MAS, 'Tres o más'),
    (MENOS_DE_TRES, 'Menos de tres'),
  )
  #veces por día
  DOS_O_MAS  = '2OMAS'
  MENOS_DE_DOS = 'MENOS2'
  VECES_DIA = (
    (DOS_O_MAS, 'Dos o más'),
    (MENOS_DE_DOS, 'Menos de dos'),
  )
  #otros medios de transporte
  NO_OTRO_MEDIO = 'NO'
  OTRA_LINEA = 'OLINEA'
  AUTO = 'AUTO'
  TAXI_REMIS = 'TAXREM'
  OTRO = 'OTRO'
  OTRO_MEDIO = (
    (NO_OTRO_MEDIO,'No'),
    (OTRA_LINEA,'Otra línea'),
    (AUTO,'Automóvil'),
    (TAXI_REMIS,'Taxi o Remis'),
    (OTRO,'Otro medio'),
  )
  #Interes en servicios anexos
  SI = 'SI'
  NO = 'NO'
  NO_ME_INTERESA = 'NI'
  NO_LO_CONOZCO = 'NC'
  INTERES_SERVICIOS_ANEXOS = (
    (SI,'Si'),
    (NO,'No'),
    (NO_ME_INTERESA,'No me interesa'),
    (NO_LO_CONOZCO,'No lo conozco'),
  )
  #
  MEJORO_BASTANTE = 'MB'
  MEJORO_MEDIANAMENTE = 'MM'
  MEJORO_POCO = 'MP'
  NO_MEJORO = 'NM'
  MEJORA_SERVICIO = (
    (MEJORO_BASTANTE,'Mejoró bastante'),
    (MEJORO_MEDIANAMENTE,'Mejoró medianamente'),
    (MEJORO_POCO,'Mejoró poco'),
    (NO_MEJORO,'No mejoró'),
    (NS_NC, 'Ns/Nc'),
  )
  #datos sobre el procedimiento de encuesta
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  encuestador = models.ForeignKey('Encuestador',Encuestador, null='true')
  parada_encuesta = models.ForeignKey(Parada, null='true')
  cargaonline = models.BooleanField('Encuesta cargada en línea',default=True)
  dia_realizada = models.DateField('fecha de realización', default=date.today)
  hora_inicio = models.DateTimeField()
  hora_fin = models.DateTimeField()
  momento = models.CharField('Momento de la encuesta',max_length=2, choices=MOMENTO, blank='true')
  #perfil del usuario
  sexo = models.CharField('Sexo',max_length=1, choices=SEXO, blank='true')
  rango_edad = models.CharField('Rango de edad',max_length=2, choices=RANGO_EDAD, blank='true')
  #origen del viaje
  origen_lugar = models.ForeignKey(Lugar, related_name='encuesta_origen_lugar', null='true')
  origen_motivo = models.ForeignKey(Motivo,related_name='encuesta_origen_motivo', null='true')
  origen_parada =  models.CharField('Parada de origen (opcional)',max_length=10, blank='true') #solo se carga si el tipo de lugar es parada
  #destino del viaje
  destino_lugar = models.ForeignKey(Lugar,related_name='encuesta_destino_lugar', null='true')
  destino_motivo = models.ForeignKey(Motivo,related_name='encuesta_destino_motivo', null='true')
  origen_parada =  models.CharField('Parada de destino (opcional)',max_length=10, blank='true') #solo se carga si el tipo de lugar es parada
  #detalles del viaje
  veces_semana = models.CharField('Veces por semana en que realiza este viaje',max_length=6, choices=VECES_SEMANA, blank='true')
  veces_dia = models.CharField('Veces por día en que realiza este viaje',max_length=6, choices=VECES_DIA, blank='true')
  otro_medio = models.CharField('Para completar el viaje usa otro medio de transporte?',max_length=6, choices=OTRO_MEDIO, blank='true')
  linea = models.ForeignKey(Linea, null='true')
  #calidad del servicio
  estado_unidad =  models.CharField('Estado general de la unidad',max_length=2, choices=CALIFICA_CALIDAD, default = NS_NC)
  comodidad =  models.CharField('Comodidad con la que viaja',max_length=2, choices=CALIFICA_CALIDAD, default = NS_NC)
  higiene_unidad =  models.CharField('Higiene de la unidad',max_length=2, choices=CALIFICA_CALIDAD, default = NS_NC)
  trato_choferes =  models.CharField('Trato y atención por parte de choferes',max_length=2, choices=CALIFICA_CALIDAD, default = NS_NC)
  conduccion_choferes =  models.CharField('¿Cómo calificaría el desempeño de los choferes en la conducción?',max_length=2, choices=CALIFICA_CALIDAD, default = NS_NC)
  info_choferes =  models.CharField('¿Cómo calificaría el nivel de información general de los choferes?',max_length=2, choices=CALIFICA_CALIDAD, default = NS_NC)
  usa_medio_informacion = models.CharField('¿Utiliza algún medio de información de transporte?',max_length=2, choices=INTERES_SERVICIOS_ANEXOS, default = NO)
  usa_trasbordo = models.CharField('¿Utiliza el servicio de trasbordo?',max_length=2, choices=INTERES_SERVICIOS_ANEXOS, default = NO)
  usa_recarga_sube = models.CharField('¿Utiliza el servicio de recarga Sube con tarjeta de crédito?',max_length=2, choices=INTERES_SERVICIOS_ANEXOS, default = NO)
  opinion_servicio = models.CharField('¿En este último tiempo, considera que el servicio brindado por la Empresa?',max_length=2, choices=MEJORA_SERVICIO, default = NS_NC)
  opinion_trabajo_muni = models.CharField('¿Cómo calificaría el trabajo que está realizando la Municipalidad para el control y mejoramiento del servicio?',max_length=2, choices=CALIFICA_CALIDAD, default = NS_NC)
  sugerencia = models.CharField('¿Tiene alguna sugerencia o comentario?',max_length=140, blank='true')
"""
