 # -- coding: utf-8 --
from django.conf.urls import url
from .campania_view import CampaniaCrear, CampaniaDetalle
from .viewencuesta import  EncuestaBorrar, EncuestaDetalle, EncuestaConfirmaAlta, EncuestaListar
from .viewencuestapasos import EncuestaCrear,EncuestaProcedimiento, EncuestaPerfil, EncuestaCalidad
from .viewparada_prompt import ParadaPrompt

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

    url(r'^encuesta/(?P<pk>\d+)/borrar/$', EncuestaBorrar.as_view(), name='encuesta_borrar'),

    #para texto: (?P<post_id>[\w-]+)
    #para números: (?P<pk>\d+)

    url(r'^encuesta/$', EncuestaListar.as_view(), name='encuesta_listar'),
    url(r'^encuesta/(?P<pk>\d+)/$', EncuestaDetalle.as_view(), name='encuesta_detalle'),
	url(r'^encuesta/(?P<pk>\d+)/confirmaalta$', EncuestaConfirmaAlta.as_view(), name='encuesta_confirma_alta'),
    #paso1. datos sobre el procedimiento de encuesta
    url(r'^encuesta/crear/$', EncuestaCrear.as_view(), name='encuesta_crear'),
    #datos similares al alta
    url(r'^encuesta/(?P<pk>\d+)/procedimiento/$', EncuestaProcedimiento.as_view(), name='encuesta_procedimiento'),
    #paso2. perfil del usuario
    url(r'^encuesta/(?P<pk>\d+)/perfil/$', EncuestaPerfil.as_view(), name='encuesta_perfil'),
    #paso3. Calidad del servicio
    url(r'^encuesta/(?P<pk>\d+)/calidad/$', EncuestaCalidad.as_view(), name='encuesta_calidad'),
    #seleccion de paradas
    url(r'^paradaprompt/$', ParadaPrompt.as_view(), name='parada_prompt'),
]
