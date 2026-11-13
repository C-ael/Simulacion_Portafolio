# Dos cuadros estadísticos con Chi-cuadrado (1 grado de libertad)
import math

from modelo import distribuciones

ALFA = 0.05

class ResultadoChi:
    def __init__(self, chi2, p):
        self.chi2 = chi2
        self.p = p
        self.rechaza = p < ALFA


def bondad_ajuste(dentro, n):
    # Compara dentro/fuera observados con los esperados si pi fuera el real
    esperado_dentro = n * math.pi / 4
    esperado_fuera = n - esperado_dentro
    chi2 = (dentro - esperado_dentro) ** 2 / esperado_dentro \
        + ((n - dentro) - esperado_fuera) ** 2 / esperado_fuera
    return ResultadoChi(chi2, distribuciones.p_valor_chi(chi2, 1))


def homogeneidad(dentro_1, dentro_2, n):
    # Tabla 2x2 (Python/Java x dentro/fuera): ¿las dos proporciones son iguales?
    tabla = [[dentro_1, n - dentro_1], [dentro_2, n - dentro_2]]
    total_columnas = [dentro_1 + dentro_2, 2 * n - dentro_1 - dentro_2]
    chi2 = 0.0
    for fila in tabla:
        for j in range(2):
            esperado = n * total_columnas[j] / (2 * n)      # total de fila = n
            if esperado > 0:
                chi2 += (fila[j] - esperado) ** 2 / esperado
    return ResultadoChi(chi2, distribuciones.p_valor_chi(chi2, 1))
