 # -- coding: utf-8 --
from django import forms
from django.forms import ModelForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse, reverse_lazy
#from django.db.models import Q #para OR en consultas
#from django.db.models.deletion import ProtectedError
#from django.forms import ValidationError

#from django.core.urlresolvers import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView
#import jsons
from .models import Campania
campania_fields = ('descripcion', 'fecha_inicio', 'fecha_fin')

class DateInput(forms.DateInput):
  input_type = 'date'

class CampaniaForm(ModelForm):

  def __init__(self, *args, **kwargs):
    self.helper = FormHelper()
    self.helper.form_class = 'form-horizontal'
    self.helper.form_method = 'post'
    self.helper.layout = Layout(
      Fieldset('Add a new dataset', 'descripcion', 'fecha_inicio', 'fecha_fin', ),
      #ButtonHolder(
      #  Submit('save', 'Submit', css_class='btn btn-primary '),
        #Reset('reset', 'Cancel', css_class='btn')
      #  )
    )
    self.helper.add_input(Submit('submit', 'Submit'))
    super(CampaniaForm, self).__init__(*args, **kwargs)
  class Meta:
    model = Campania
    fields = campania_fields
    widgets = {
      'fecha_inicio': DateInput(),
      'fecha_fin': DateInput(),
    }

class CampaniaCrear(CreateView):
    model = Campania
    form_class = CampaniaForm
    #template_name = 'appencuesta/campania_form.html'
    def get_success_url(self):
        return reverse('campania_detalle', kwargs={
            'pk': self.object.pk,
        })

class CampaniaDetalle(DetailView):
    model = Campania
    fields = campania_fields

class CampaniaModificar(UpdateView):
    model = Campania
    fields = campania_fields

    def get_success_url(self):
        return reverse('appencuesta:campania_detalle', kwargs={
            'pk': self.object.pk,
        })
