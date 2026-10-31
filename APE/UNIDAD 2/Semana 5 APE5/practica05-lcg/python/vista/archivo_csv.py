# Guarda la secuencia en un CSV (el mismo formato que usa el programa Java)
import os


def guardar(ruta, valores):
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    with open(ruta, "w", encoding="utf-8") as archivo:
        archivo.write("n,x,u\n")
        for n, x, u in valores:
            archivo.write(f"{n},{x},{u:.10f}\n")
