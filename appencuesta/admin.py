from django.contrib import admin

from .models import Campania
from .models import Encuestador
from .models import Parada
from .models import Linea
from .models import Lugar
from .models import Motivo
from .models import Encuesta

admin.site.register(Campania, Encuestador, Parada, Linea, Lugar, Motivo, Encuesta)
