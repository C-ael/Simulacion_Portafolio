# Controlador: sigue los pasos de la guía y le pasa los resultados a la vista
import os

from modelo import experimento, comparador, pruebas_chi
from modelo.error import ResumenRepeticiones
from modelo.generador_lcg import GeneradorLCG
from modelo.generador_nativo import GeneradorNativo
from vista.consola import Consola
from vista import archivo_csv, graficas

TAMANOS = [1000, 10000, 100000, 1000000]    # tamaños de muestra de la guía
SEMILLA = 12345
REPETICIONES = 10                           # repeticiones por tamaño para ver el error promedio
A, C, M = 1664525, 1013904223, 2 ** 32      # parámetros del LCG propio
GENERADORES = ["LCG propio", "Nativo"]      # el LCG propio y el que trae cada lenguaje

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CARPETA_RESULTADOS = os.path.join(RAIZ, "resultados")


def crear_generador(nombre, semilla):
    if nombre == "LCG propio":
        return GeneradorLCG(A, C, M, semilla)
    return GeneradorNativo(semilla)


class Controlador:
    def ejecutar(self):
        consola = Consola()
        consola.mostrar_inicio(TAMANOS, SEMILLA, REPETICIONES)

        # Experimento principal: una ejecución por generador y tamaño (tabla de la ficha)
        python = {}
        for generador in GENERADORES:
            for n in TAMANOS:
                r = experimento.estimar_pi(crear_generador(generador, SEMILLA), n)
                prueba = pruebas_chi.bondad_ajuste(r.dentro, n)
                r.chi2, r.p = prueba.chi2, prueba.p
                python[(generador, n)] = r

        # Varias repeticiones con distintas semillas para ver cómo baja el error
        resumenes = {}
        for n in TAMANOS:
            estimaciones = [experimento.estimar_pi(crear_generador("LCG propio", SEMILLA + i), n).pi
                            for i in range(REPETICIONES)]
            resumenes[n] = ResumenRepeticiones(n, estimaciones)

        archivo_csv.guardar_resultados(os.path.join(CARPETA_RESULTADOS, "resultados_python.csv"), python)
        archivo_csv.guardar_repeticiones(os.path.join(CARPETA_RESULTADOS, "repeticiones_python.csv"), resumenes)

        java = comparador.leer_resultados(os.path.join(CARPETA_RESULTADOS, "resultados_java.csv"))
        java_repeticiones = comparador.leer_repeticiones(os.path.join(CARPETA_RESULTADOS, "repeticiones_java.csv"))
        if java is None or java_repeticiones is None:
            java = None
            consola.mostrar_sin_java()

        for generador in GENERADORES:
            consola.mostrar_resultados(generador, TAMANOS, python, java)
        for generador in GENERADORES:
            consola.mostrar_bondad(generador, TAMANOS, python)

        homogeneidad = {}
        if java is not None:
            for generador in GENERADORES:
                for n in TAMANOS:
                    homogeneidad[(generador, n)] = pruebas_chi.homogeneidad(
                        python[(generador, n)].dentro, java[(generador, n)].dentro, n)
                consola.mostrar_homogeneidad(generador, TAMANOS, homogeneidad)
            iguales = comparador.repeticiones_iguales(
                {n: r.estimaciones for n, r in resumenes.items()}, java_repeticiones)
            consola.mostrar_comparacion(comparador.comparar_resultados(python, java), iguales)

        consola.mostrar_repeticiones(resumenes)
        self.hacer_graficas(consola, python, java, resumenes, homogeneidad)

    def hacer_graficas(self, consola, python, java, resumenes, homogeneidad):
        # Si algo falla al graficar, el resto del programa ya terminó bien
        try:
            puntos = []
            for n in TAMANOS:
                dibujar = min(n, 20000)             # no se dibujan los 1 000 000 de puntos
                xs, ys, dentro = experimento.generar_puntos(crear_generador("LCG propio", SEMILLA), dibujar)
                puntos.append((n, xs, ys, dentro, python[("LCG propio", n)].pi))
            graficas.grafica_puntos(puntos)
            graficas.grafica_estimacion(TAMANOS, python, java)
            graficas.grafica_error(TAMANOS, resumenes, python)
            pasos, curva = experimento.curva_convergencia(crear_generador("LCG propio", SEMILLA), TAMANOS[-1], 1000)
            graficas.grafica_convergencia(pasos, curva)
            graficas.grafica_tiempos(TAMANOS, python, java)
            graficas.grafica_chi(TAMANOS, python, java, homogeneidad)
            consola.mostrar_mensaje("Gráficas guardadas en la carpeta graficas/.")
            graficas.mostrar()
        except Exception as error:
            consola.mostrar_mensaje(f"No se pudieron dibujar las gráficas: {error}")
