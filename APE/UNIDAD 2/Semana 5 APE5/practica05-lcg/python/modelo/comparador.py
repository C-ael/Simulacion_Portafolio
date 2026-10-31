# Lee lo que generó Java y lo compara con lo que generó Python
import csv
import os


def leer_csv(ruta):
    # Devuelve una lista de (n, X, U), o None si el archivo no existe
    if not os.path.exists(ruta):
        return None

    valores = []
    with open(ruta, newline="", encoding="utf-8") as archivo:
        lector = csv.reader(archivo)
        next(lector)                    # se salta el encabezado
        for fila in lector:
            valores.append((int(fila[0]), int(fila[1]), float(fila[2])))
    return valores


def contar_iguales(valores_python, valores_java):
    # Cuenta en cuántas posiciones coinciden X (exacto) y U (casi exacto)
    iguales = 0
    for (n1, x1, u1), (n2, x2, u2) in zip(valores_python, valores_java):
        if x1 == x2 and abs(u1 - u2) < 1e-9:
            iguales += 1
    return iguales
