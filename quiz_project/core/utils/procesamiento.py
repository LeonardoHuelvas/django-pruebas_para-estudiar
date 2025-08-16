import pdfplumber
import subprocess
import textwrap


def extraer_texto_pdf(ruta_pdf):
    """
    Extrae el texto completo de un archivo PDF.
    """
    texto = ""
    with pdfplumber.open(ruta_pdf) as pdf:
        for pagina in pdf.pages:
            contenido = pagina.extract_text()
            if contenido:
                texto += contenido + "\n"
    return texto.strip()


def generar_preguntas_con_llama(texto):
    """
    Envía el texto a Ollama usando subprocess y obtiene preguntas tipo ICFES.
    """
    texto_limitado = texto[:4000]  # Limita para no saturar
    prompt = textwrap.dedent(f"""
    A partir del siguiente contenido, genera un resumen breve y luego 5 preguntas tipo ICFES con 4 opciones y su respuesta correcta. El formato debe ser así:

    Pregunta 1:
    ¿Cuál es el tema principal del texto?
    A. Opción A
    B. Opción B
    C. Opción C
    D. Opción D
    Respuesta correcta: B

    --- CONTENIDO ---
    {texto_limitado}
    """)

    try:
        proceso = subprocess.Popen(
            ["ollama", "run", "llama3"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        salida, error = proceso.communicate(prompt, timeout=120)

        if proceso.returncode != 0:
            return f"[ERROR] Ollama: {error.strip()}"

        return salida.strip()

    except subprocess.TimeoutExpired:
        return "[ERROR] Tiempo de espera agotado. Llama tardó demasiado en responder."

    except Exception as e:
        return f"[ERROR] Falló la generación con Ollama: {str(e)}"
