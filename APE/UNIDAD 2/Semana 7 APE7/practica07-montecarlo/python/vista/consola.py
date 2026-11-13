# Todo lo que se imprime en la terminal
import math

from modelo.error import desviacion_teorica, error_medio_teorico
from modelo.pruebas_chi import ALFA


def decision(rechaza):
    return "Se rechaza H0" if rechaza else "No se rechaza H0"


class Consola:

    def mostrar_inicio(self, tamanos, semilla, repeticiones):
        print("=== Estimación de pi con el método de Monte Carlo (Python) ===")
        print("Cuadrado de lado 2 con un círculo de radio 1 inscrito.  pi ≈ 4 · Nc / N")
        print(f"Tamaños de muestra: {', '.join(str(n) for n in tamanos)}")
        print(f"Semilla: {semilla}   Repeticiones por tamaño: {repeticiones}")
        print(f"Valor real de pi = {math.pi:.10f}")
        print()

    def mostrar_resultados(self, generador, tamanos, python, java):
        # Tabla de la ficha: N, pi estimado, error y tiempo de cada lenguaje
        print(f"--- Generador: {generador} ---")
        if java is None:
            print(f"{'N':>9}{'Nc':>9}{'pi Python':>12}{'Error Py':>12}{'t Python (ms)':>15}")
            for n in tamanos:
                r = python[(generador, n)]
                print(f"{n:>9}{r.dentro:>9}{r.pi:>12.6f}{r.error:>12.6f}{r.tiempo_ms:>15.2f}")
        else:
            print(f"{'N':>9}{'pi Python':>12}{'pi Java':>12}{'Error Py':>11}{'Error Java':>12}"
                  f"{'t Py (ms)':>11}{'t Java (ms)':>13}")
            for n in tamanos:
                r = python[(generador, n)]
                j = java[(generador, n)]
                print(f"{n:>9}{r.pi:>12.6f}{j.pi:>12.6f}{r.error:>11.6f}{j.error:>12.6f}"
                      f"{r.tiempo_ms:>11.2f}{j.tiempo_ms:>13.2f}")
        print()

    def mostrar_bondad(self, generador, tamanos, python):
        print(f"Chi-cuadrado de bondad de ajuste, Python, {generador} (gl = 1, alfa = {ALFA}, crítico = 3.8415)")
        print(f"{'N':>9}{'Nc obs':>9}{'Nc esp':>11}{'chi2':>10}{'p':>10}  Decisión")
        for n in tamanos:
            r = python[(generador, n)]
            print(f"{n:>9}{r.dentro:>9}{n * math.pi / 4:>11.1f}{r.chi2:>10.4f}{r.p:>10.4f}  "
                  f"{decision(r.p < ALFA)}")
        print()

    def mostrar_homogeneidad(self, generador, tamanos, pruebas):
        print(f"Chi-cuadrado de homogeneidad Python vs Java, {generador} (gl = 1)")
        print(f"{'N':>9}{'chi2':>10}{'p':>10}  Decisión")
        for n in tamanos:
            c = pruebas[(generador, n)]
            print(f"{n:>9}{c.chi2:>10.4f}{c.p:>10.4f}  {decision(c.rechaza)}")
        print()

    def mostrar_comparacion(self, comparacion, repeticiones_iguales):
        iguales = [clave for clave, v in comparacion.items() if all(v)]
        print("=== Comparación con Java ===")
        print(f"{'Generador':<12}{'N':>9}{'Mismo Nc':>10}{'Mismo pi':>10}{'Mismo chi2':>12}")
        for (generador, n), (a, b, c) in comparacion.items():
            print(f"{generador:<12}{n:>9}{'sí' if a else 'no':>10}{'sí' if b else 'no':>10}"
                  f"{'sí' if c else 'no':>12}")
        print(f"Repeticiones con el LCG propio idénticas en Java: {'sí' if repeticiones_iguales else 'no'}")
        print()

    def mostrar_repeticiones(self, resumenes):
        print("=== Error según el tamaño de muestra (varias repeticiones, LCG propio) ===")
        print(f"{'N':>9}{'Error medio':>13}{'Mínimo':>10}{'Máximo':>10}{'Desv. obs':>11}{'Desv. teórica':>15}{'Error teórico':>15}")
        for n, r in resumenes.items():
            print(f"{n:>9}{r.error_medio:>13.5f}{r.error_minimo:>10.5f}{r.error_maximo:>10.5f}"
                  f"{r.desviacion:>11.5f}{desviacion_teorica(n):>15.5f}{error_medio_teorico(n):>15.5f}")
        print()

    def mostrar_sin_java(self):
        print("No se encontraron los archivos de Java en 'resultados/'.")
        print("Ejecuta primero el programa Java para poder compararlo (se muestran solo los de Python).")
        print()

    def mostrar_mensaje(self, texto):
        print(texto)
