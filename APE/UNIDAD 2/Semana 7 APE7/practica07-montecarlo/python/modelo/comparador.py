# Lee los archivos que guardó Java y los compara con los de Python
import csv
import math
import os

from modelo.resultado import ResultadoPi


def leer_resultados(ruta):
    # Devuelve {(generador, n): ResultadoPi} o None si no se puede leer el archivo
    try:
        resultados = {}
        with open(ruta, encoding="utf-8") as archivo:
            for fila in csv.DictReader(archivo):
                r = ResultadoPi(int(fila["n"]), int(fila["dentro"]), float(fila["tiempo_ms"]))
                r.chi2 = float(fila["chi2"])
                r.p = float(fila["p_chi"])
                resultados[(fila["generador"], r.n)] = r
        return resultados or None
    except (OSError, KeyError, ValueError, csv.Error):
        return None


def leer_repeticiones(ruta):
    # Devuelve {n: [estimaciones de pi]} o None si no se puede leer el archivo
    try:
        repeticiones = {}
        with open(ruta, encoding="utf-8") as archivo:
            for fila in csv.DictReader(archivo):
                repeticiones.setdefault(int(fila["n"]), []).append(float(fila["pi"]))
        return repeticiones or None
    except (OSError, KeyError, ValueError, csv.Error):
        return None


def son_iguales(a, b):
    return math.isclose(a, b, rel_tol=1e-6, abs_tol=1e-9)


def comparar_resultados(python, java):
    # Devuelve {(generador, n): (mismos puntos dentro, mismo pi, mismo chi2)}
    comparacion = {}
    for clave, r in python.items():
        j = java.get(clave)
        if j is None:
            comparacion[clave] = (False, False, False)
        else:
            comparacion[clave] = (r.dentro == j.dentro, son_iguales(r.pi, j.pi), son_iguales(r.chi2, j.chi2))
    return comparacion


def repeticiones_iguales(python, java):
    # True si Java obtuvo las mismas estimaciones en todas las repeticiones
    if set(python) != set(java):
        return False
    return all(len(python[n]) == len(java[n]) and all(son_iguales(a, b) for a, b in zip(python[n], java[n]))
               for n in python)
