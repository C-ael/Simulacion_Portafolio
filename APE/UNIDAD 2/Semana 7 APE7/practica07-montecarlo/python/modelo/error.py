# Error esperado del método Monte Carlo y resumen de varias repeticiones
import math

P_CIRCULO = math.pi / 4         # probabilidad de que un punto caiga dentro del círculo


def desviacion_teorica(n):
    # Desviación estándar de la estimación de pi con n puntos: 4 · raíz(p(1-p) / n)
    return 4 * math.sqrt(P_CIRCULO * (1 - P_CIRCULO) / n)


def error_medio_teorico(n):
    # Error absoluto promedio esperado: desviación · raíz(2/pi)
    return desviacion_teorica(n) * math.sqrt(2 / math.pi)


class ResumenRepeticiones:
    def __init__(self, n, estimaciones):
        errores = [abs(e - math.pi) for e in estimaciones]
        self.n = n
        self.cantidad = len(estimaciones)
        self.media_pi = sum(estimaciones) / len(estimaciones)
        suma = sum((e - self.media_pi) ** 2 for e in estimaciones)
        self.desviacion = math.sqrt(suma / (len(estimaciones) - 1))
        self.error_medio = sum(errores) / len(errores)
        self.error_minimo = min(errores)
        self.error_maximo = max(errores)
        self.errores = errores
        self.estimaciones = estimaciones
