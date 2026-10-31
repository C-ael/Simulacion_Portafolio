# Controlador: sigue los pasos de la guía y le pasa los resultados a la vista
import os

from modelo.generador_lcg import GeneradorLCG
from modelo import analisis, comparador
from vista.consola import Consola
from vista import archivo_csv, graficas

# Parámetros de la guía
A = 1664525
C = 1013904223
M = 2 ** 32
SEMILLA = 12345
SEMILLA_2 = 54321       # segunda semilla para el paso "cambiar la semilla"
CANTIDAD = 10000

# Carpeta resultados/ (en la raíz del proyecto, junto a python/ y java/)
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CARPETA_RESULTADOS = os.path.join(RAIZ, "resultados")


class Controlador:
    def ejecutar(self):
        consola = Consola()
        consola.mostrar_parametros(A, C, M, SEMILLA, CANTIDAD)

        # Pasos 1 y 2: generar 10 000 valores con la semilla de la guía
        valores1 = GeneradorLCG(A, C, M, SEMILLA).generar(CANTIDAD)
        # Paso 7: cambiar la semilla
        valores2 = GeneradorLCG(A, C, M, SEMILLA_2).generar(CANTIDAD)

        archivo_csv.guardar(self.ruta("python", SEMILLA), valores1)
        archivo_csv.guardar(self.ruta("python", SEMILLA_2), valores2)

        for semilla, valores in [(SEMILLA, valores1), (SEMILLA_2, valores2)]:
            media, varianza = analisis.estadisticas(valores)
            consola.mostrar_estadisticas(semilla, media, varianza, analisis.valores_repetidos(valores))

        # Pasos 3, 4 y 8: comparar con lo que generó Java
        self.comparar_con_java(consola, valores1, valores2)

        # Paso 6: período
        consola.mostrar_periodo(self.ejemplos_periodo())

        # Paso 5: gráficas
        graficas.grafica_secuencia(valores1, SEMILLA, valores2, SEMILLA_2)
        graficas.grafica_histograma(valores1, SEMILLA)
        graficas.grafica_dispersion(valores1, SEMILLA)

    def ruta(self, lenguaje, semilla):
        return os.path.join(CARPETA_RESULTADOS, f"lcg_{lenguaje}_{semilla}.csv")

    def comparar_con_java(self, consola, valores1, valores2):
        java1 = comparador.leer_csv(self.ruta("java", SEMILLA))
        java2 = comparador.leer_csv(self.ruta("java", SEMILLA_2))

        if java1 is None or java2 is None:
            consola.mostrar_primeras_20(valores1)
            consola.mostrar_sin_java()
            return

        consola.mostrar_comparacion_20(valores1, java1)
        consola.mostrar_resultado_comparacion(SEMILLA, comparador.contar_iguales(valores1, java1), CANTIDAD)
        consola.mostrar_resultado_comparacion(SEMILLA_2, comparador.contar_iguales(valores2, java2), CANTIDAD)

    def ejemplos_periodo(self):
        # Con m = 16 el período se puede contar completo. Cada fila es (a, c, m, semilla)
        casos = [
            (5, 3, 16, 1),      # parámetros buenos: período completo
            (5, 0, 16, 1),      # c = 0: el período se acorta
            (1, 0, 16, 3),      # a = 1 y c = 0: el valor nunca cambia
        ]
        return [(a, c, m, semilla, analisis.periodo(a, c, m, semilla)) for a, c, m, semilla in casos]
