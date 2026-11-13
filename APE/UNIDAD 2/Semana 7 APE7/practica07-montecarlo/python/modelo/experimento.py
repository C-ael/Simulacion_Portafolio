# Experimento Monte Carlo: estimar pi con puntos en un cuadrado y un círculo inscrito
#
# Cuadrado de lado 2 (de -1 a 1) y círculo de radio 1 en el centro.
# Área del círculo / área del cuadrado = pi / 4, así que pi ≈ 4 · Nc / N
import time

from modelo.resultado import ResultadoPi


def contar_dentro(generador, n):
    # Lanza n puntos y cuenta cuántos caen dentro del círculo (x² + y² <= 1)
    dentro = 0
    for _ in range(n):
        x = 2 * generador.siguiente() - 1       # número entre -1 y 1
        y = 2 * generador.siguiente() - 1
        if x * x + y * y <= 1:
            dentro += 1
    return dentro


def estimar_pi(generador, n):
    inicio = time.perf_counter()
    dentro = contar_dentro(generador, n)
    tiempo_ms = (time.perf_counter() - inicio) * 1000
    return ResultadoPi(n, dentro, tiempo_ms)


def generar_puntos(generador, cantidad):
    # Devuelve las listas x, y y si cada punto está dentro (para dibujarlos)
    xs, ys, dentro = [], [], []
    for _ in range(cantidad):
        x = 2 * generador.siguiente() - 1
        y = 2 * generador.siguiente() - 1
        xs.append(x)
        ys.append(y)
        dentro.append(x * x + y * y <= 1)
    return xs, ys, dentro


def curva_convergencia(generador, n, cada):
    # Estimación de pi cada 'cada' puntos, para ver cómo se acerca al valor real
    puntos, estimaciones = [], []
    dentro = 0
    for i in range(1, n + 1):
        x = 2 * generador.siguiente() - 1
        y = 2 * generador.siguiente() - 1
        if x * x + y * y <= 1:
            dentro += 1
        if i % cada == 0:
            puntos.append(i)
            estimaciones.append(4 * dentro / i)
    return puntos, estimaciones
