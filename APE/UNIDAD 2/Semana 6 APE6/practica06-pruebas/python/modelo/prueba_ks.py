# Algoritmo 3: prueba Kolmogorov-Smirnov contra la uniforme (0,1)
from modelo import distribuciones
from modelo.resultado import ResultadoKS

def aplicar(numeros):
    ordenados = sorted(numeros)
    n = len(ordenados)
    d_positiva = 0.0
    d_negativa = 0.0
    for i, u in enumerate(ordenados, start=1):
        # F(u) = u para la uniforme (0,1); la empírica vale i/n
        d_positiva = max(d_positiva, i / n - u)
        d_negativa = max(d_negativa, u - (i - 1) / n)
    p = distribuciones.p_valor_ks(max(d_positiva, d_negativa), n)
    critico = distribuciones.valor_critico_ks(n)
    return ResultadoKS(d_positiva, d_negativa, p, critico)
