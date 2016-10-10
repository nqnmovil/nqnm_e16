 # -- coding: utf-8 --
from django import forms
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.db.models import Q #para OR en consultas
from django.db.models.deletion import ProtectedError
from django.forms import ValidationError

from django.core.urlresolvers import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView
import json
from django.contrib.auth.mixins import LoginRequiredMixin

encuesta_fields = (
'encuestador',
'parada_encuesta',
'cargaonline',
'dia_realizada',
'hora_inicio',
'momento',
)
#perfil del usuario
from .models import Encuesta

class EncuestaListar(LoginRequiredMixin, ListView):
    model = Encuesta
    paginate_by = 10

    #búsqueda

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query is None:
            return Encuesta.objects.all().order_by('dia_realizada')
        else:
            return Encuesta.objects.filter( Q(encuestador__usuario__username__icontains=query)).order_by('nombre')

    #almacenar contexto de la búsqueda
    def get_context_data(self, **kwargs):
        context = super(EncuestaListar, self).get_context_data(**kwargs)
        q = self.request.GET.get('q')
        if q: #si existe el valor, lo agrego/actualizo en el contexto
            q = q.replace(" ","+")
            context['query'] = q
        return context

class EncuestaCrear(LoginRequiredMixin, CreateView):
    model = Encuesta
    fields = encuesta_fields

    def get_success_url(self):
        return reverse('encuesta_confirma_alta', kwargs={
            'pk': self.object.pk,
        })

class EncuestaDetalle(LoginRequiredMixin, DetailView):
    model = Encuesta
    fields = encuesta_fields

class EncuestaConfirmaAlta(LoginRequiredMixin, DetailView):
    template_name = 'apppresupuestos/encuesta_confirm_create.html'
    model = Encuesta
    fields = encuesta_fields

class EncuestaModificar(UpdateView):
    model = Encuesta
    fields = encuesta_fields
    def get_success_url(self):
        return reverse('encuesta_detalle', kwargs={
            'pk': self.object.pk,
        })

class EncuestaBorrar(DeleteView):
    model = Encuesta
    success_url = reverse_lazy('encuesta_listar')
    fields = encuesta_fields

    def delete(self, request, *args, **kwargs):
        encuesta = self.get_object()

        try:
            encuesta.delete()
            estado = 'Encuesta eliminada correctamente'
        except ValidationError as e:
            estado = 'Objeto protegido.' + str(e)
        respuesta = estado

        return render(request, 'appencuesta/confirmar_borrado.html',{"respuesta":respuesta })
        #return HttpResponse(respuesta   )
