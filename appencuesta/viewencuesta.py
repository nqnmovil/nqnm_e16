 # -- coding: utf-8 --
from django import forms
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.db.models import Q #para OR en consultas
from django.db.models.deletion import ProtectedError
from django.forms import ValidationError

from django.core.urlresolvers import reverse, reverse_lazy
from django.views.generic import DetailView, ListView, DeleteView
import json
from django.contrib.auth.mixins import LoginRequiredMixin

encuesta_fields = (
'encuestador',
'parada_encuesta',
'cargaonline',
'dia_realizada',
'momento',
'estado',
)

from .models import Encuesta

class EncuestaListar(LoginRequiredMixin, ListView):
    model = Encuesta
    paginate_by = 10

    #búsqueda
    def get_queryset(self):

        query_ape = self.request.GET.get('filtro_ape')
        query_nom = self.request.GET.get('filtro_nom')
        query_num = self.request.GET.get('filtro_num')
        qs = Encuesta.objects.activo().order_by('-id') #antes .all()
        #muestro sólo las encuestas del usuario logueado
        current_user = self.request.user
        print(current_user)
        qs = qs.filter(encuestador__usuario = current_user)
        if query_ape is None:
            """
            no aplico filtros
            """
        else:
            qs = qs.filter( Q(encuestador__usuario__last_name__icontains=query_ape)).order_by('-id')
        if not(query_nom is None):
            qs = qs.filter(encuestador__usuario__first_name__icontains=query_nom)
        if not(query_num is None or query_num == ''):
            qs = qs.filter(referencia__icontains=query_num)

        return qs
    #almacenar contexto de la búsqueda
    def get_context_data(self, **kwargs):
        context = super(EncuestaListar, self).get_context_data(**kwargs)
        filtro_ape = self.request.GET.get('filtro_ape')
        if filtro_ape: #si existe el valor, lo agrego/actualizo en el contexto
            filtro_ape = filtro_ape.replace(" ","+")
            context['filtro_ape'] = filtro_ape
        filtro_nom = self.request.GET.get('filtro_nom')
        if filtro_nom: #si existe el valor, lo agrego/actualizo en el contexto
            filtro_nom = filtro_nom.replace(" ","+")
            context['filtro_nom'] = filtro_nom
        filtro_num = self.request.GET.get('filtro_num')
        if filtro_num: #si existe el valor, lo agrego/actualizo en el contexto
            filtro_num = filtro_num.replace(" ","+")
            context['filtro_num'] = filtro_num

        return context

class EncuestaDetalle(LoginRequiredMixin, DetailView):
    model = Encuesta
    fields = encuesta_fields

class EncuestaConfirmaAlta(LoginRequiredMixin, DetailView):
    template_name = 'appencuesta/encuesta_confirm_create.html'
    model = Encuesta
    fields = encuesta_fields

class EncuestaBorrar(DeleteView):
    model = Encuesta
    success_url = reverse_lazy('appencuesta:encuesta_listar')
    fields = encuesta_fields
