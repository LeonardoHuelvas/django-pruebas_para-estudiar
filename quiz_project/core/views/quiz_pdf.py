import re
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from core.models import Pregunta, EjeTematico
from core.utils.procesamiento import extraer_texto_pdf, generar_preguntas_con_llama


def quiz_desde_pdf(request):
    resultado = None
    ejes = EjeTematico.objects.all()
    eje_seleccionado = None

    if request.method == 'POST':
        archivo = request.FILES.get('archivo')
        eje_id = request.POST.get('eje_id')

        if not archivo or not eje_id:
            messages.error(request, "Debes subir un archivo PDF y seleccionar un eje temático.")
            return render(request, 'quiz/generar.html', {
                'ejes': ejes,
                'resultado': resultado,
                'eje_seleccionado': eje_id,
            })

        try:
            eje = EjeTematico.objects.get(pk=eje_id)
            eje_seleccionado = eje.id
        except EjeTematico.DoesNotExist:
            messages.error(request, "Eje temático no válido.")
            return render(request, 'quiz/generar.html', {
                'ejes': ejes,
                'resultado': resultado,
                'eje_seleccionado': eje_id,
            })

        # Guardar archivo y procesar preguntas
        fs = FileSystemStorage()
        nombre = fs.save(archivo.name, archivo)
        ruta = fs.path(nombre)

        texto = extraer_texto_pdf(ruta)
        preguntas_crudas = generar_preguntas_con_llama(texto)
        preguntas_procesadas = procesar_preguntas_generadas(preguntas_crudas)

        nuevas = []
        for preg in preguntas_procesadas:
            if not Pregunta.objects.filter(enunciado__iexact=preg['enunciado']).exists():
                pregunta = Pregunta.objects.create(
                    eje=eje,
                    enunciado=preg['enunciado'],
                    respuesta_correcta=preg['respuesta'],
                )
                nuevas.append(pregunta)

        messages.success(request, f"{len(nuevas)} preguntas nuevas añadidas.")
        resultado = preguntas_procesadas

    return render(request, 'quiz/generar.html', {
        'resultado': resultado,
        'ejes': ejes,
        'eje_seleccionado': eje_seleccionado
    })


def procesar_preguntas_generadas(texto):
    bloques = re.split(r'\n\d+\.', texto)
    preguntas = []
    for bloque in bloques:
        if not bloque.strip():
            continue
        partes = bloque.strip().split("\n")
        if len(partes) < 5:
            continue  # no tiene suficientes líneas

        enunciado = partes[0].strip()
        opciones = partes[1:5]
        correcta = ""
        for op in opciones:
            if op.strip().startswith("*"):
                correcta = op.replace("*", "").strip()
        preguntas.append({
            'enunciado': enunciado,
            'opciones': [op.replace("*", "").strip() for op in opciones],
            'respuesta': correcta
        })
    return preguntas
