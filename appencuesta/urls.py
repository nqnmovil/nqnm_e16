 # -- coding: utf-8 --
from django.conf.urls import url
from .campania_view import CampaniaCrear, CampaniaDetalle
from .viewencuesta import EncuestaCrear, EncuestaBorrar, EncuestaDetalle, EncuestaConfirmaAlta, EncuestaListar, EncuestaModificar
from .viewlogin import user_login, user_logout
from .views import index
from django.contrib.auth.decorators import login_required

app_name="appencuesta" #namespace

urlpatterns = [
    url(r'^$', login_required(index), name='index'),
    #url(r'^clientes/$', login_required(ClienteListar.as_view()), name='cliente_listar'),
    url(r'^campania/crear/$', CampaniaCrear.as_view(), name='campania_crear'),
    url(r'^campania/(?P<pk>\d+)/$', CampaniaDetalle.as_view(), name='campania_detalle'),
    #url(r'^clientes/(?P<pk>\d+)/modificar/$', login_required(ClienteModificar.as_view()), name='cliente_modificar'),
    #url(r'^clientes/(?P<pk>\d+)/borrar/$', login_required(ClienteBorrar.as_view()), name='cliente_borrar'),

    #Login y logout
    url(r'^login/$', user_login, name='login'),
    url(r'^logout/$', user_logout, name='logout'),

    #para texto: (?P<post_id>[\w-]+)
    #para números: (?P<pk>\d+)

    url(r'^encuesta/$', EncuestaListar.as_view(), name='encuesta_listar'),
    url(r'^encuesta/crear/$', EncuestaCrear.as_view(), name='encuesta_crear'),
    url(r'^encuesta/(?P<pk>\d+)/$', EncuestaDetalle.as_view(), name='encuesta_detalle'),
	url(r'^encuesta/(?P<pk>\d+)/confirmaalta$', EncuestaConfirmaAlta.as_view(), name='encuesta_confirma_alta'),
    url(r'^encuesta/(?P<pk>\d+)/modificar/$', EncuestaModificar.as_view(), name='encuesta_modificar'),
    url(r'^encuesta/(?P<pk>\d+)/borrar/$', EncuestaBorrar.as_view(), name='encuesta_borrar'),

]
