import json

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .stats import EntradaInvalida, calcular, parsear


def _fmt(x):
    if x is None:
        return "—"
    if isinstance(x, list):
        return ", ".join(_fmt(v) for v in x)
    if isinstance(x, float):
        return f"{x:.4f}".rstrip("0").rstrip(".") if abs(x) < 1e15 else f"{x:.6g}"
    return str(x)


ETIQUETAS = [
    ("promedio", "Promedio (media)", True),
    ("mediana", "Mediana", True),
    ("moda", "Moda", True),
    ("cantidad", "Cantidad (n)", False),
    ("suma", "Suma", False),
    ("minimo", "Mínimo", False),
    ("maximo", "Máximo", False),
    ("rango", "Rango", False),
    ("desvio_muestral", "Desvío estándar muestral", False),
    ("desvio_poblacional", "Desvío estándar poblacional", False),
    ("varianza_muestral", "Varianza muestral", False),
    ("varianza_poblacional", "Varianza poblacional", False),
]


def index(request):
    contexto = {"texto": ""}
    if request.method == "POST":
        texto = request.POST.get("numeros", "")
        contexto["texto"] = texto
        try:
            datos = parsear(texto)
            res = calcular(datos)
            contexto["resultados"] = [
                {"etiqueta": e, "valor": _fmt(res[k]), "destacado": d} for k, e, d in ETIQUETAS
            ]
        except EntradaInvalida as e:
            contexto["error"] = str(e)
    return render(request, "estadistica/index.html", contexto)


@csrf_exempt  # API pública sin sesión: no hay cookies que proteger
@require_POST
def api_calcular(request):
    """POST JSON {"numeros": [1,2,3]} o {"numeros": "1, 2, 3"} -> estadísticas."""
    try:
        cuerpo = json.loads(request.body or b"{}")
        numeros = cuerpo.get("numeros")
        if isinstance(numeros, str):
            datos = parsear(numeros)
        elif isinstance(numeros, list) and numeros:
            datos = parsear(" ".join(str(n) for n in numeros))
        else:
            raise EntradaInvalida("Enviá 'numeros' como lista o texto.")
        return JsonResponse(calcular(datos))
    except (json.JSONDecodeError, AttributeError):
        return JsonResponse({"error": "JSON inválido"}, status=400)
    except EntradaInvalida as e:
        return JsonResponse({"error": str(e)}, status=400)
