from django import forms
from django.forms import ModelForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML,Div,Field,Layout, Fieldset, ButtonHolder, Submit
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions,StrictButton
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.db.models.deletion import ProtectedError
from django.forms import ValidationError

from django.core.urlresolvers import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView
import json
from django.contrib.auth.mixins import LoginRequiredMixin

encuesta_procedimiento_fields = (
'encuestador','parada_encuesta','cargaonline',
'dia_realizada','momento',
)
encuesta_procedimiento_fieldSet = ('Procedimiento de encuesta','encuestador','parada_encuesta','cargaonline',
'dia_realizada','momento') #('Procedimiento de encuesta',) + encuesta_procedimiento_fields

from .models import Encuesta
from .models import Encuestador
class DateInput(forms.DateInput):
  input_type = 'date'

class EncuestaProcedimientoForm(ModelForm):

  def __init__(self,user,*args, **kwargs):
    self.helper = FormHelper()
    self.helper.form_class = 'form-horizontal'
    self.helper.form_method = 'post'
    self.helper.layout = Layout(
      Div(
        HTML('<legend>Procedimiento de encuesta</legend>')
        ),
        Field('encuestador',css_class = 'col-lg-6 col-md-5 col-sm-3 col-xs-2'),
        Field('parada_encuesta'),
        HTML("""
          <a href="#" onclick="showModal();" >Buscar parada</a>
        """),
        Field('cargaonline'),
        #'dia_realizada' #para cuando se deba editar
        Field('dia_realizada', id='id_dia_realizada',readonly='readonly',template='appencuesta/util/datepicker_fecha.html'),
        Field('momento'),

        FormActions(
          StrictButton('Volver sin guardar',
          onclick="location.href='"+reverse('appencuesta:encuesta_listar',)+"'",
          name="volver",value='volver a listado' , css_class="extra"),
          Submit('save', 'Guardar y seguir', css_class='btn btn-primary '),
        ),
        HTML("""
        </script>
        <script type="text/javascript">
          function showModal()
          {
            var dialogWin = window.open('{% url "appencuesta:parada_prompt"  %}', "dialogwidth: 450px; dialogheight: 300px; resizable: yes"); // Showing the Modal Dialog
          }
        </script>
      """)

    )
    super(EncuestaProcedimientoForm, self).__init__(*args, **kwargs)
    #busco el encuestador asociado al current user
    encuestador = Encuestador.objects.get(usuario__id = user.id)
    self.fields['encuestador'].queryset= Encuestador.objects.filter(id=encuestador.id)
    self.fields['encuestador'].initial = encuestador
  class Meta:
    model = Encuesta
    fields = encuesta_procedimiento_fields

class EncuestaCrear(LoginRequiredMixin, CreateView):
    model = Encuesta
    form_class = EncuestaProcedimientoForm
    #fields = encuesta_procedimiento_fields

    def get_success_url(self):
        return reverse('appencuesta:encuesta_perfil', kwargs={'pk': self.object.pk,}) #va a paso2
    def get_form_kwargs(self):
      current_user = self.request.user
      print (current_user.id)
      kwargs = super(EncuestaCrear, self).get_form_kwargs()
      kwargs.update({'user': self.request.user})
      return kwargs

class EncuestaProcedimiento(LoginRequiredMixin, UpdateView):
    model = Encuesta
    form_class = EncuestaProcedimientoForm

    def get_success_url(self):
        return reverse('appencuesta:encuesta_perfil', kwargs={'pk': self.object.pk}) #va a paso2

    def get_success_url(self):
        return reverse('appencuesta:encuesta_perfil', kwargs={'pk': self.object.pk,}) #va a paso2
    def get_form_kwargs(self):
      usuarioAlta = self.object.encuestador.usuario
      #current_user = usuarioAlta #self.request.user
      print (usuarioAlta)
      kwargs = super(EncuestaProcedimiento, self).get_form_kwargs()
      kwargs.update({'user': usuarioAlta,'selfpk':self.object.pk})
      return kwargs



""" Perfil del usuario """
encuesta_perfil_fields = (
'sexo','rango_edad',
'origen_lugar','origen_motivo','origen_parada',
'destino_lugar','destino_motivo','destino_parada',
'veces_semana','veces_dia',
'otro_medio','linea'
)
encuesta_perfil_fieldSet = ('Perfil del usuario',) + encuesta_perfil_fields

class EncuestaPerfilForm(ModelForm):

  def __init__(self,user, selfpk, *args, **kwargs):
    self.helper = FormHelper()
    self.helper.form_class = 'form-horizontal'
    self.helper.form_method = 'post'
    self.helper.layout = Layout(
      Fieldset('Perfil del usuario',
        'sexo',
        'rango_edad',
      ),
      Fieldset('Origen del viaje',
      'origen_lugar',
      'origen_motivo',
      'origen_parada',
      ),
      Fieldset('Destino del viaje',
      'destino_lugar',
      'destino_motivo',
      'destino_parada',
      ),
      Fieldset('Detalles del viaje',
      'veces_semana',
      'veces_dia',
      'otro_medio',
      'linea'
      ),
      FormActions(
        StrictButton('Volver sin guardar',
          onclick="location.href='"+reverse('appencuesta:encuesta_procedimiento', kwargs={'pk': selfpk})+"'",
          name="volver",value='volver a procedimiento' , css_class="extra"),
        Submit('save', 'Guardar y seguir', css_class='btn btn-primary '),
      ),
    )
    super(EncuestaPerfilForm, self).__init__(*args, **kwargs)

  class Meta:
    model = Encuesta
    fields = encuesta_perfil_fields
    widgets = {
    }

class EncuestaPerfil(UpdateView):
    model = Encuesta
    form_class = EncuestaPerfilForm
    def get_success_url(self):
        return reverse('appencuesta:encuesta_calidad', kwargs={'pk': self.object.pk}) #va a paso3
    def get_form_kwargs(self):
      usuarioAlta = self.object.encuestador.usuario
      #current_user = usuarioAlta #self.request.user
      print (usuarioAlta)
      kwargs = super(EncuestaPerfil, self).get_form_kwargs()
      kwargs.update({'user': usuarioAlta,'selfpk':self.object.pk})
      return kwargs



""" Calidad del servicio """
encuesta_calidad_fields = (
'estado_unidad', 'comodidad', 'higiene_unidad',
'trato_choferes', 'conduccion_choferes', 'info_choferes',
'usa_medio_informacion',
'usa_trasbordo', 'usa_recarga_sube',
'opinion_servicio', 'opinion_trabajo_muni',
'sugerencia',
)
encuesta_calidad_fieldSet = ('Calidad del servicio',) + encuesta_calidad_fields

class EncuestaCalidadForm(ModelForm):

  def __init__(self, user, selfpk, *args, **kwargs):
    self.helper = FormHelper()
    self.helper.form_class = 'form-horizontal'
    self.helper.form_method = 'post'
    self.helper.layout = Layout(
      Fieldset('Estado de la unidad',
        'estado_unidad',
        'comodidad',
        'higiene_unidad',
      ),
      Fieldset('Choferes',
        'trato_choferes',
        'conduccion_choferes',
        'info_choferes',
      ),
      Fieldset('Servicios anexos',
        'usa_medio_informacion',
        'usa_trasbordo',
        'usa_recarga_sube',
      ),
      Fieldset(
        'opinion_servicio',
        'opinion_trabajo_muni',
        'sugerencia',
      ),
      FormActions(
        StrictButton('Volver sin guardar',
        onclick="location.href='"+reverse('appencuesta:encuesta_perfil', kwargs={'pk': selfpk})+"'",
        name="volver",value='volver al perfil' , css_class="extra"),
        Submit('save', 'Guardar y finalizar', css_class='btn btn-primary '),
      )
    )
    super(EncuestaCalidadForm, self).__init__(*args, **kwargs)

  class Meta:
    model = Encuesta
    fields = encuesta_calidad_fields
    widgets = {
    }

class EncuestaCalidad(UpdateView):
    model = Encuesta
    form_class = EncuestaCalidadForm
    def get_success_url(self):
        return reverse('appencuesta:encuesta_detalle', kwargs={'pk': self.object.pk}) #va a resumen de la encuesta
    def get_form_kwargs(self):
      usuarioAlta = self.object.encuestador.usuario
      #current_user = usuarioAlta #self.request.user
      print (usuarioAlta)
      kwargs = super(EncuestaCalidad, self).get_form_kwargs()
      kwargs.update({'user': usuarioAlta,'selfpk':self.object.pk})
      return kwargs
