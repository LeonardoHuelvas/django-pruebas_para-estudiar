from django.contrib import admin
from .models import Quiz, EjeTematico, Pregunta, Opcion, Resultado

admin.site.register(Quiz)
admin.site.register(EjeTematico)
admin.site.register(Pregunta)
admin.site.register(Opcion)
admin.site.register(Resultado)
