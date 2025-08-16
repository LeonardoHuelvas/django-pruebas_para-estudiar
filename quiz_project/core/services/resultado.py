from django.db.models import Count
from core.models import Resultado

def registrar_resultado(usuario: str, quiz_id: int, puntaje: float) -> Resultado:
    return Resultado.objects.create(usuario=usuario, quiz_id=quiz_id, puntaje=puntaje)

def top_n_por_quiz(quiz_id: int, n: int = 10):
    return (Resultado.objects.filter(quiz_id=quiz_id)
            .order_by("-puntaje","-fecha")[:n])
