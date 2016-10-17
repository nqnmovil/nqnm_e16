 # -- coding: utf-8 --
from django import forms
from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q #para OR en consultas

from django.core.urlresolvers import reverse, reverse_lazy
from django.views.generic import ListView
parada_fields = ('numero')

from .models import Parada

class ParadaPrompt(ListView):
    model = Parada

    template_name = 'appencuesta/parada_prompt.html'
    paginate_by = 10

    #búsqueda
    def get_queryset(self):
        query = self.request.GET.get('q')
        if query is None:
            return Parada.objects.all()
        else:
            return Parada.objects.filter( Q(numero__icontains=query) )
    #almacenar contexto de la búsqueda
    def get_context_data(self, **kwargs):
        context = super(ParadaPrompt, self).get_context_data(**kwargs)
        q = self.request.GET.get('q')
        if q: #si existe el valor, lo agrego/actualizo en el contexto
            q = q.replace(" ","+")
            context['query'] = q
        return context
