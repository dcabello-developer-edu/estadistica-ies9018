"""Lógica pura de estadística (sin Django), fácil de testear."""
import re
import statistics as st


class EntradaInvalida(ValueError):
    pass


def parsear(texto: str) -> list[float]:
    """Convierte '1, 2 3;4\n5.5' en [1.0, 2.0, 3.0, 4.0, 5.5]. Decimales con punto."""
    partes = [p for p in re.split(r"[\s,;]+", texto.strip()) if p]
    if not partes:
        raise EntradaInvalida("Ingresá al menos un número.")
    try:
        numeros = [float(p) for p in partes]
    except ValueError as e:
        raise EntradaInvalida(f"Valor no válido: {str(e).split(': ')[-1]}") from e
    if any(n != n or n in (float("inf"), float("-inf")) for n in numeros):
        raise EntradaInvalida("No se permiten valores infinitos o NaN.")
    if len(numeros) > 10_000:
        raise EntradaInvalida("Máximo 10.000 valores.")
    return numeros


def calcular(datos: list[float]) -> dict:
    n = len(datos)
    modas = st.multimode(datos)
    resultado = {
        "cantidad": n,
        "suma": sum(datos),
        "promedio": st.fmean(datos),
        "mediana": st.median(datos),
        # Si todos los valores son distintos no hay moda
        "moda": None if len(modas) == n and n > 1 else modas,
        "minimo": min(datos),
        "maximo": max(datos),
        "rango": max(datos) - min(datos),
        "varianza_poblacional": st.pvariance(datos),
        "desvio_poblacional": st.pstdev(datos),
        "varianza_muestral": st.variance(datos) if n > 1 else None,
        "desvio_muestral": st.stdev(datos) if n > 1 else None,
    }
    return resultado
