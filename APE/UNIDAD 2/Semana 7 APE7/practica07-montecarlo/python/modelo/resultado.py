# Resultado de un experimento Monte Carlo con N puntos
import math


class ResultadoPi:
    def __init__(self, n, dentro, tiempo_ms):
        self.n = n
        self.dentro = dentro                    # Nc: puntos dentro del círculo
        self.pi = 4 * dentro / n                # pi ≈ 4 · Nc / N
        self.error = abs(self.pi - math.pi)     # error absoluto
        self.tiempo_ms = tiempo_ms
        self.chi2 = 0.0                         # se llenan al aplicar la prueba Chi-cuadrado
        self.p = 1.0
