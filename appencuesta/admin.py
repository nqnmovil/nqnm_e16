from django.contrib import admin

from .models import Campania
from .models import Encuestador
from .models import Parada
from .models import Linea
from .models import Lugar
from .models import Motivo
from .models import Encuesta
from .models import Numerador

admin.site.register(Campania)
admin.site.register(Encuestador)
admin.site.register(Parada)
admin.site.register(Linea)
admin.site.register(Lugar)
admin.site.register(Motivo)
admin.site.register(Numerador)

#admin.site.register(Encuesta)
class EncuestaAdmin(admin.ModelAdmin):
  list_display = ('referencia','encuestador','parada_encuesta','dia_realizada','activo','hora_realizada','estado')

admin.site.register(Encuesta, EncuestaAdmin)
