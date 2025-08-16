from django.urls import path
from django.conf.urls.static import static
from core.views.dashboard import DashboardView 
from django.contrib.auth.views import LoginView
from django.conf import settings
from core.views.quiz_pdf import quiz_desde_pdf

from core.views.quiz import *
from core.views.eje import *
from core.views.pregunta import *
from core.views.opcion import *
from core.views.resultado import *
from core.views.auth import cerrar_sesion
from core.views.usuario import crear_usuario, gestionar_perfil, gestionar_roles
 

app_name = "core"

urlpatterns = [
    
    # Home y autenticación
    path('', DashboardView.as_view(), name='dashboard'),
    path('accounts/login/', LoginView.as_view(template_name='login/login.html'), name='login'),
    path('cerrar-sesion/', cerrar_sesion, name='cerrar_sesion'),
    
    #  # PERFIL (editar mis datos)
    path("perfil/editar/", gestionar_perfil, name="gestionar_perfil"),

     # USUARIOS (solo admin)
    path("usuarios/roles/", gestionar_roles, name="gestionar_roles"),
    path("usuarios/nuevo/", crear_usuario, name="crear_usuario"),


    # Quiz
    path("quices/", QuizListView.as_view(), name="quiz_list"),
    path("quices/crear/", QuizCreateView.as_view(), name="quiz_create"),
    path("quices/<int:pk>/", QuizDetailView.as_view(), name="quiz_detail"),
    path("quices/<int:pk>/editar/", QuizUpdateView.as_view(), name="quiz_update"),
    path("quices/<int:pk>/eliminar/", QuizDeleteView.as_view(), name="quiz_delete"),
    path("quices/desde-pdf/", quiz_desde_pdf, name="quiz_desde_pdf"),
    path('quiz/<int:eje_id>/presentar/', presentar_quiz_view, name='presentar_quiz'),
    # path("quiz/seleccionar/", seleccionar_quiz_view, name="seleccionar_quiz"),
 

    # Eje
    path("ejes/", EjeListView.as_view(), name="eje_list"),
    path("ejes/crear/", EjeCreateView.as_view(), name="eje_create"),
    path("ejes/<int:pk>/", EjeDetailView.as_view(), name="eje_detail"),
    path("ejes/<int:pk>/editar/", EjeUpdateView.as_view(), name="eje_update"),
    path("ejes/<int:pk>/eliminar/", EjeDeleteView.as_view(), name="eje_delete"),

    # Pregunta
    path("preguntas/", PreguntaListView.as_view(), name="pregunta_list"),
    path("ejes/<int:eje_id>/preguntas/", PreguntaListView.as_view(), name="pregunta_list_by_eje"),
    path("preguntas/crear/", PreguntaCreateView.as_view(), name="pregunta_create"),
    path("preguntas/<int:pk>/", PreguntaDetailView.as_view(), name="pregunta_detail"),
    path("preguntas/<int:pk>/editar/", PreguntaUpdateView.as_view(), name="pregunta_update"),
    path("preguntas/<int:pk>/eliminar/", PreguntaDeleteView.as_view(), name="pregunta_delete"),
    path("preguntas/importar/", importar_preguntas_view, name="importar_preguntas"),
    





    # Opción
    path("opciones/crear/", OpcionCreateView.as_view(), name="opcion_create"),
    path("opciones/<int:pk>/editar/", OpcionUpdateView.as_view(), name="opcion_update"),
    path("opciones/<int:pk>/eliminar/", OpcionDeleteView.as_view(), name="opcion_delete"),

    # Resultados / ranking
    path("resultados/", ResultadoListView.as_view(), name="resultado_list"),
    path("resultados/<int:pk>/", ResultadoDetailView.as_view(), name="resultado_detail"),
    path("quices/<int:quiz_id>/ranking/", RankingPorQuizView.as_view(), name="ranking_quiz"),
    path("resultado/<int:resultado_id>/detalle/", detalle_resultado_view, name="detalle_resultado")

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)