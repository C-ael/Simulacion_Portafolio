# Controlador: sigue los pasos de la guía y le pasa los resultados a la vista
import os

from modelo.configuracion import Configuracion
from modelo.generador_lcg import GeneradorLCG
from modelo.resultado import Resultado, ALFA
from modelo import prueba_chi, prueba_ks, comparador
from vista.consola import Consola
from vista import archivo_csv, graficas

CANTIDAD = 10000        # números por configuración
INTERVALOS = 10         # k para Chi-cuadrado (gl = 9)

# Configuraciones a comparar: la primera es la de la guía
CONFIGURACIONES = [
    Configuracion("Guia semilla 12345", 1664525, 1013904223, 2 ** 32, 12345),
    Configuracion("Guia semilla 54321", 1664525, 1013904223, 2 ** 32, 54321),
    Configuracion("RANDU", 65539, 0, 2 ** 31, 1),
    Configuracion("Parametros malos m=16", 5, 3, 16, 1),
]

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CARPETA_RESULTADOS = os.path.join(RAIZ, "resultados")


class Controlador:
    def ejecutar(self):
        consola = Consola()
        consola.mostrar_inicio(CANTIDAD, INTERVALOS, ALFA)

        resultados = []
        for numero, configuracion in enumerate(CONFIGURACIONES, start=1):
            # Actividad 1: generar los números con el LCG
            generador = GeneradorLCG(configuracion.a, configuracion.c, configuracion.m, configuracion.semilla)
            numeros = generador.generar(CANTIDAD)
            # Algoritmos 2 y 3: las dos pruebas
            chi = prueba_chi.aplicar(numeros, INTERVALOS)
            ks = prueba_ks.aplicar(numeros)
            resultado = Resultado(configuracion, numeros, chi, ks)
            resultados.append(resultado)
            consola.mostrar_configuracion(resultado)
            # Paso 12 del Algoritmo 1: guardar la secuencia para las pruebas
            archivo_csv.guardar_secuencia(os.path.join(CARPETA_RESULTADOS, f"secuencia_python_{numero}.csv"), numeros)

        consola.mostrar_resumen(resultados)
        archivo_csv.guardar_pruebas(os.path.join(CARPETA_RESULTADOS, "pruebas_python.csv"), resultados)

        self.comparar_con_java(consola, resultados)
        self.hacer_graficas(consola, resultados)

    def comparar_con_java(self, consola, resultados):
        filas_java = comparador.leer_pruebas(os.path.join(CARPETA_RESULTADOS, "pruebas_java.csv"))
        if filas_java is None:
            consola.mostrar_sin_java()
        else:
            consola.mostrar_comparacion(comparador.comparar(resultados, filas_java, CARPETA_RESULTADOS))

    def hacer_graficas(self, consola, resultados):
        # Si algo falla al graficar, el resto del programa ya terminó bien
        try:
            graficas.grafica_secuencia(resultados)
            graficas.grafica_dispersion(resultados)
            graficas.grafica_chi(resultados)
            graficas.grafica_campana_chi(resultados)
            graficas.grafica_ks(resultados)
            graficas.grafica_diferencias_ks(resultados)
            graficas.grafica_valores_p(resultados)
            consola.mostrar_mensaje("Gráficas guardadas en la carpeta graficas/.")
            graficas.mostrar()
        except Exception as error:
            consola.mostrar_mensaje(f"No se pudieron dibujar las gráficas: {error}")
