 # -- coding: utf-8 --
from django.conf.urls import url
from .campania_view import CampaniaCrear, CampaniaDetalle
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    #url(r'^clientes/$', login_required(ClienteListar.as_view()), name='cliente_listar'),
    url(r'^campania/crear/$', CampaniaCrear.as_view(), name='campania_crear'),
    url(r'^campania/(?P<pk>\d+)/$', CampaniaDetalle.as_view(), name='campania_detalle'),
    #url(r'^clientes/(?P<pk>\d+)/modificar/$', login_required(ClienteModificar.as_view()), name='cliente_modificar'),
    #url(r'^clientes/(?P<pk>\d+)/borrar/$', login_required(ClienteBorrar.as_view()), name='cliente_borrar'),

]
