# -- coding: utf-8 --
import uuid
from django.contrib.auth.models import User
from django.db import models
from datetime import date, time, datetime
from django.utils.encoding import python_2_unicode_compatible
from django.db.models.query import QuerySet

""" constantes """
#momento de la encuesta
ANTES_ASCENDER = 'AA'
LUEGO_DESCENDER = 'LD'

PARADA = 'P' #tipos de Lugares.parada

class ActivosQuerySet(QuerySet):
    def delete(self):
        self.update(activo=False)

class AdministrarActivos(models.Manager):
    def activo(self):
        return self.model.objects.filter(activo=True)

    def get_queryset(self):
        return ActivosQuerySet(self.model, using=self._db)

@python_2_unicode_compatible
class Numerador (models.Model):
	nombre = models.CharField(max_length=30, blank='true',unique=True)
	ultimo_valor = models.IntegerField(default=0)
	def __str__(self):
		return self.nombre

#from nqnmovilutiles import sigNumero,completarConCeros #Como usa Numerador, lo importo después de que existe en model
""" signumero y completar con ceros deben moverse a un archirvo nqnmovilutiles"""
def sigNumero(nombreNumerador):
	try:
		n = Numerador.objects.get(nombre=nombreNumerador)
	except Numerador.DoesNotExist:
		#Si no existe en la BD, lo creo
		n = Numerador(nombre=nombreNumerador, ultimo_valor = 1)
		n.save()
		return n.ultimo_valor
	else:
		#si existe, incremento el valor, lo guardo y lo retorno
		n.ultimo_valor += 1
		n.save()
		return n.ultimo_valor

def completarConCeros( numero, longitud):
	numerotxt = str(numero)
	return numerotxt.zfill(longitud)


@python_2_unicode_compatible
class Campania (models.Model):
  descripcion = models.CharField('Descripción',max_length=100)
  fecha_inicio = models.DateField('Fecha de inicio', default=date.today)
  fecha_fin = models.DateField('Fecha de fin')
  def __str__(self):
    return self.descripcion
  class Meta:
    verbose_name = "Campaña"
    verbose_name_plural = "Campañas"

#@python_2_unicode_compatible
class Encuestador (models.Model):
  usuario = models.ForeignKey(User)
  activo = models.BooleanField('Encuestador activo',default=True)
  def __str__(self):
    return self.usuario.get_full_name()#self.usuario.first_name
  class Meta:
    verbose_name = "Encuestador"
    verbose_name_plural = "Encuestadores"
  def delete(self):
    self.activo = False
    self.save()

@python_2_unicode_compatible
class Parada (models.Model):
  numero = models.CharField('Número',max_length=10)
  def __str__(self):
    return self.numero
  class Meta:
    verbose_name = "Parada"
    verbose_name_plural = "Paradas"

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
  class Meta:
    verbose_name = "Lugar"
    verbose_name_plural = "Lugares"
@python_2_unicode_compatible
class Motivo (models.Model):
  nombre = models.CharField('nombre del motivo',max_length=100)
  def __str__(self):
    return self.nombre

@python_2_unicode_compatible
class Encuesta (models.Model):
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
  ADULTO_MAYOR = 'AM'
  RANGO_EDAD = (
    (JOVEN,'Jóven (18-25 años)'),
    (ADULTO,'Adulto (25-60 años)'),
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

  #datos sobre el procedimiento de encuesta
  #nousar esto: id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  referencia = models.CharField('Número de encuesta',max_length=10,blank='true') #autoincremental
  encuestador = models.ForeignKey('Encuestador',Encuestador, null='true')
  parada_encuesta = models.ForeignKey(Parada,verbose_name='Parada', null='true', on_delete= models.PROTECT)
  cargaonline = models.BooleanField('Encuesta cargada en línea',default=True)
  dia_realizada = models.DateField('fecha de realización', default=date.today)
  hora_realizada = models.TimeField('hora de realización', default= time(16, 00))
  hora_inicio = models.DateTimeField(blank = 'true', null = 'true')
  hora_fin = models.DateTimeField(blank = 'true', null = 'true')
  momento = models.CharField('Momento de la encuesta',max_length=2, choices=MOMENTO, default= ANTES_ASCENDER)
  #perfil del usuario
  sexo = models.CharField('1.a. Sexo',max_length=1, choices=SEXO)
  rango_edad = models.CharField('1.b. Rango de edad',max_length=2, choices=RANGO_EDAD)
  #origen del viaje
  #parahacer:ocultar lugar y parada tanto de origen como destino o dejar que lo carguen en blanco
  origen_lugar = models.ForeignKey(Lugar, related_name='encuesta_origen_lugar', null='true', blank='true', on_delete= models.PROTECT)

  origen_motivo = models.ForeignKey(Motivo,verbose_name='2.a. Motivo del viaje. Desde',related_name='encuesta_origen_motivo', null='true', on_delete= models.PROTECT)
  origen_parada =  models.CharField('Parada de origen (opcional)',max_length=10, blank='true') #solo se carga si el tipo de lugar es parada
  #destino del viaje
  destino_lugar = models.ForeignKey(Lugar,related_name='encuesta_destino_lugar', null='true', blank='true', on_delete= models.PROTECT)
  destino_motivo = models.ForeignKey(Motivo,verbose_name='2.b. Motivo del viaje. Hacia',related_name='encuesta_destino_motivo', null='true', on_delete= models.PROTECT)
  destino_parada =  models.CharField('Parada de destino (opcional)',max_length=10, blank='true') #solo se carga si el tipo de lugar es parada
  #detalles del viaje
  #veces por semana
  TODOS_LOS_DIAS = 'TODOS'
  TRES_O_MAS = '3OMAS'
  MENOS_DE_TRES = 'MENOS3'
  VECES_SEMANA = (
    (TODOS_LOS_DIAS, 'Todos los días'),
    (TRES_O_MAS, 'Tres o más'),
    (MENOS_DE_TRES, 'Menos de tres'),
  )
  veces_semana = models.CharField('3.a. Veces por semana en que realiza este viaje',max_length=6, choices=VECES_SEMANA)
  #veces por día
  DOS_O_MAS  = '2OMAS'
  MENOS_DE_DOS = 'MENOS2'
  VECES_DIA = (
    (DOS_O_MAS, 'Dos o más'),
    (MENOS_DE_DOS, 'Menos de dos'),
  )
  veces_dia = models.CharField('3.b. Veces por día en que realiza este viaje',max_length=6, choices=VECES_DIA)
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
  otro_medio = models.CharField('4. Para completar el viaje ¿Usa otro medio de transporte?',max_length=6, choices=OTRO_MEDIO)
  linea = models.ForeignKey(Linea,verbose_name='5. ¿En qué línea de transporte suele viajar?', null='true', on_delete= models.PROTECT)
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
  estado_unidad =  models.CharField('6.a. Estado general de las unidades',max_length=2, choices=CALIFICA_CALIDAD, default = NS_NC)
  comodidad =  models.CharField('6.b. Comodidad con la que viaja',max_length=2, choices=CALIFICA_CALIDAD, default = NS_NC)
  higiene_unidad =  models.CharField('6.c. Higiene de las unidadades',max_length=2, choices=CALIFICA_CALIDAD, default = NS_NC)
  trato_choferes =  models.CharField('7.a. Nivel de trato y atención recibida por los choferes',max_length=2, choices=CALIFICA_CALIDAD, default = NS_NC)
  conduccion_choferes =  models.CharField('7.b. Desempeño de los choferes en la conducción',max_length=2, choices=CALIFICA_CALIDAD, default = NS_NC)
  info_choferes =  models.CharField('7.c. Nivel de información del sistema de transporte de los choferes?',max_length=2, choices=CALIFICA_CALIDAD, default = NS_NC)
  #Interes en servicios anexos
  SI = 'SI'
  NO = 'NO'
  NO_ME_INTERESA = 'NI'
  NO_LO_CONOZCO = 'NC'

  INTERES_SERVICIOS_ANEXOS = (
    (SI,'Si'),
    (NO,'No'),
    (NO_LO_CONOZCO,'No. No lo conozco'),
  )

  #medios de información de transporte
  WEB_CUANDOPASA = 'WC'
  WEB_MUNICIPAL = 'WM'
  CONSULTAS_TELEFONICAS = 'CT'
  MENSAJE_TEXTO = 'MT'
  CARTELES_INTELIGENTES ='CI'
  APP_CEL_CUANDO_PASA = 'CP'

  USA_MEDIOS_INFORMACION = (
    (SI,'Si'),
    (NO,'No'),
    (NO_ME_INTERESA,'No. No estoy interesado/a'),
    (NO_LO_CONOZCO,'No. No lo conozco'),
    (WEB_CUANDOPASA,'Si. Página web de cuandopasa.com'),
    (WEB_MUNICIPAL,'Si. Página web de la Municipalidad'),
    (CONSULTAS_TELEFONICAS,'Si. Consultas telefónicas'),
    (MENSAJE_TEXTO,'Si. Mensaje de texto'),
    (CARTELES_INTELIGENTES,'Si. Carteles de información LED'),
 )
  usa_medio_informacion = models.CharField('8. ¿Utiliza algún medio de información de transporte?',max_length=2, choices=USA_MEDIOS_INFORMACION, default = NO_LO_CONOZCO)
  usa_trasbordo = models.CharField('9. ¿Utiliza el servicio de trasbordo?',max_length=2, choices=INTERES_SERVICIOS_ANEXOS, default = NO)

  #paraHacer:tarjeta sube
  #beneficios tarjeta sube
  BENEF_SUBE_NO = 'BS_NO'
  BENEF_SUBE_SI_ANSES = 'BS_AN'
  BENEF_SUBE_SI_ESCOLAR = 'BS_ES'
  BENEF_SUBE_SI_UNIVERSITARIO = 'BS_UN'
  BENEF_SUBE_SI_JUCAID = 'BS_JU'
  SUBE_BENEFICIOS = {
    (BENEF_SUBE_NO,'No'),
    (SI,'Si'),
    (BENEF_SUBE_SI_ANSES,'Si. ANSES'),
    (BENEF_SUBE_SI_ESCOLAR,'Si. Escolar'),
    (BENEF_SUBE_SI_UNIVERSITARIO,'Si. Universitario'),
    (BENEF_SUBE_SI_JUCAID,'Si. JUCAID'),
  }
  sube_beneficios = models.CharField('9.1 ¿Su tarjeta SUBE tiene algún beneficio?',max_length=5, choices=SUBE_BENEFICIOS, default = BENEF_SUBE_NO)

  #opinión mejora en servicio
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
  opinion_servicio = models.CharField('9.2. ¿En este último tiempo, considera que el servicio brindado por la Empresa?',max_length=2, choices=MEJORA_SERVICIO, default = NS_NC)
  opinion_trabajo_muni = models.CharField('9.3. ¿Cómo calificaría el trabajo que está realizando la Municipalidad para el control y mejoramiento del servicio?',max_length=2, choices=CALIFICA_CALIDAD, default = NS_NC)
  sugerencia = models.CharField('10. ¿Tiene alguna sugerencia o comentario?',max_length=140, blank='true')
  activo = models.BooleanField('Encuesta activa',default=True)

  ESTADO_COMPLETA = 'COM'
  ESTADO_INCOMPLETA = 'INC'
  ESTADOS = (
    (ESTADO_COMPLETA, 'Si. Encuesta completa'),
    (ESTADO_INCOMPLETA, 'No. Terminaré de cargarla más adelante'),
  )
  estado = models.CharField('¿Da por finalizada la carga de la encuesta?',max_length=3, choices=ESTADOS, default = ESTADO_INCOMPLETA)

  def __str__(self):
    return self.referencia
  #sólo permito borrado lógico, también proveo lista de encuestas activas
  objects = AdministrarActivos()
  def delete(self):
    self.activo = False
    self.save()

  def save(self, *args, **kwargs):
    #si es insert (id= 0), asignar referencia autoincremental
    if self.id is None:
      self.referencia = completarConCeros( sigNumero('encuesta_campania_0001'), 5)

      unaparada = Lugar.objects.get(tipo = PARADA) #debe haber un solo Lugar de tipo PARADA
      #Valores por defecto de paradas de origen y destino. Se inhabilita por carga manual
      #self.origen_parada = self.parada_encuesta.numero if self.momento == ANTES_ASCENDER else '' #Si se releva al subir, uso la parada de la encuesta como origen
      #self.origen_lugar = unaparada if self.momento == ANTES_ASCENDER else None
      #self.destino_parada = self.parada_encuesta.numero if self.momento == LUEGO_DESCENDER else '' #Si se releva al bajar, uso la parada de la encuesta como destino
      #self.destino_lugar = unaparada if self.momento == LUEGO_DESCENDER else None

    super(Encuesta, self).save(*args, **kwargs) # Call the "real" save() method.

  def origenfijo(self): #el lugar y parada de origen no se pueden modificar
    return True if self.momento == ANTES_ASCENDER else False
