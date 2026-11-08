# Compara los resultados de Python con los que guardó Java
import csv
import math
import os


def leer_pruebas(ruta):
    # Devuelve {nombre: fila} o None si el archivo no existe o no se puede leer
    try:
        with open(ruta, encoding="utf-8") as archivo:
            return {fila["configuracion"]: fila for fila in csv.DictReader(archivo)}
    except (OSError, KeyError, csv.Error):
        return None


def son_iguales(valor_python, texto_java):
    try:
        return math.isclose(valor_python, float(texto_java), rel_tol=1e-6, abs_tol=1e-9)
    except ValueError:
        return False


def leer_secuencia(ruta):
    # Lista de U guardada por Java, o None si no se puede leer
    try:
        with open(ruta, encoding="utf-8") as archivo:
            return [float(fila["u"]) for fila in csv.DictReader(archivo)]
    except (OSError, KeyError, ValueError, csv.Error):
        return None


def contar_iguales(numeros_python, numeros_java):
    if numeros_java is None or len(numeros_java) != len(numeros_python):
        return 0
    return sum(1 for a, b in zip(numeros_python, numeros_java) if abs(a - b) < 1e-9)


def comparar(resultados, filas_java, carpeta):
    # Devuelve una lista de (nombre, iguales, total, chi2_igual, p_chi_igual, d_igual, p_ks_igual)
    comparacion = []
    for numero, r in enumerate(resultados, start=1):
        nombre = r.configuracion.nombre
        total = len(r.numeros)
        java = leer_secuencia(os.path.join(carpeta, f"secuencia_java_{numero}.csv"))
        iguales = contar_iguales(r.numeros, java)
        fila = filas_java.get(nombre)
        if fila is None:
            comparacion.append((nombre, iguales, total, False, False, False, False))
            continue
        comparacion.append((nombre, iguales, total,
                            son_iguales(r.chi.chi2, fila["chi2"]),
                            son_iguales(r.chi.p, fila["p_chi"]),
                            son_iguales(r.ks.d, fila["d_ks"]),
                            son_iguales(r.ks.p, fila["p_ks"])))
    return comparacion
