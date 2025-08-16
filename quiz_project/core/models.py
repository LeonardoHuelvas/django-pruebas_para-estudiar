from django.db import models
from django.contrib.auth.models import User

class PerfilUsuario(models.Model):
    ROLES = [
        ('admin', 'Administrador'),
        ('estudiante', 'Estudiante'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    rol = models.CharField(max_length=20, choices=ROLES, default='estudiante')
    foto = models.ImageField(upload_to='usuarios/fotos/', null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} ({self.get_rol_display()})"

    def es_admin(self):
        return self.rol == 'admin'

    def es_estudiante(self):
        return self.rol == 'estudiante'


# Este es el modelo para los Quices
class Quiz(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre
    
    # este es el modelo para los Ejes Temáticos
class EjeTematico(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="ejes")

    def __str__(self):
        return f"{self.nombre} ({self.quiz.nombre})"

class Pregunta(models.Model):
    TIPO_PREGUNTA = [
        ('VF', 'Verdadero/Falso'),
        ('UNICA', 'Opción Única'),
    ]
    texto = models.TextField()
    tipo = models.CharField(max_length=10, choices=TIPO_PREGUNTA)
    eje = models.ForeignKey(EjeTematico, on_delete=models.CASCADE, related_name="preguntas")

    def __str__(self):
        return self.texto

class Opcion(models.Model):
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE, related_name="opciones")
    texto = models.CharField(max_length=255)
    es_correcta = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.texto} - {'Correcta' if self.es_correcta else 'Incorrecta'}"

from django.db import models
from core.models import Quiz, EjeTematico

from django.contrib.auth.models import User

class Resultado(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, null=True, blank=True)
    eje = models.ForeignKey(EjeTematico, on_delete=models.CASCADE, null=True, blank=True)
    puntaje = models.FloatField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.eje:
            return f"{self.usuario.username} - {self.eje.nombre} - {self.puntaje}"
        return f"{self.usuario.username} - {self.quiz.nombre} - {self.puntaje}"



class RespuestaUsuario(models.Model):
    resultado = models.ForeignKey(Resultado, related_name="respuestas", on_delete=models.CASCADE)
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE)
    opcion_seleccionada = models.ForeignKey(Opcion, on_delete=models.SET_NULL, null=True, blank=True)