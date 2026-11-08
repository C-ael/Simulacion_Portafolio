# Algoritmo 2: prueba Chi-cuadrado de uniformidad
from modelo import distribuciones
from modelo.resultado import ResultadoChi

def aplicar(numeros, k=10):
    esperada = len(numeros) / k             # frecuencia esperada de cada intervalo
    observadas = [0] * k
    for u in numeros:
        intervalo = min(int(u * k), k - 1)  # a qué intervalo [i/k, (i+1)/k) pertenece
        observadas[intervalo] += 1

    chi2 = 0.0
    for o in observadas:
        chi2 += (o - esperada) ** 2 / esperada

    grados = k - 1
    p = distribuciones.p_valor_chi(chi2, grados)
    critico = distribuciones.valor_critico_chi(grados)
    return ResultadoChi(observadas, esperada, chi2, grados, p, critico)
