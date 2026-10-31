# Análisis de la secuencia: estadísticas, valores repetidos y período


def estadisticas(valores):
    # Media y varianza de los U generados.
    # Para una uniforme (0,1) se espera media 0.5 y varianza 1/12 = 0.0833
    us = [u for _, _, u in valores]
    media = sum(us) / len(us)
    varianza = sum((u - media) ** 2 for u in us) / len(us)
    return media, varianza


def valores_repetidos(valores):
    # Cuántos X se repiten dentro de la secuencia
    xs = [x for _, x, _ in valores]
    return len(xs) - len(set(xs))


def periodo(a, c, m, semilla):
    # Cuenta cuántos pasos pasan hasta volver a la semilla.
    # Solo se usa con m pequeño: con m = 2^32 en Python tardaría horas.
    x = semilla
    for paso in range(1, m + 1):
        x = (a * x + c) % m
        if x == semilla:
            return paso
    return None     # nunca vuelve a la semilla
