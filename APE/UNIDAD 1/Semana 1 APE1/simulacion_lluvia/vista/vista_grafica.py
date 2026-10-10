# Vista: gráficas con matplotlib.
import os
import matplotlib.pyplot as plt

CARPETA = "graficas"

def _guardar(nombre_archivo):
    os.makedirs(CARPETA, exist_ok=True)
    plt.savefig(os.path.join(CARPETA, nombre_archivo), dpi=120)

def grafica_indice(modelo, resultados, archivo):
    horas = [r["hora"] for r in resultados]
    indices = [r["indice"] for r in resultados]

    plt.figure(figsize=(10, 5))
    plt.plot(horas, indices, marker="o", label="Índice I")
    plt.axhline(y=modelo.umbrales[0], linestyle="--", color="green", label="Baja posibilidad")
    plt.axhline(y=modelo.umbrales[1], linestyle="--", color="orange", label="Lluvia probable")
    plt.axhline(y=modelo.umbrales[2], linestyle="--", color="red", label="Lluvia")
    plt.xlabel("Hora")
    plt.ylabel("Índice de lluvia")
    plt.title(f"Índice de lluvia en 24 h - {modelo.nombre}")
    plt.grid(True)
    plt.legend()
    _guardar(archivo)
    plt.show()

def grafica_comparacion(res_original, res_ajustado, archivo):
    horas = [r["hora"] for r in res_original]

    plt.figure(figsize=(10, 5))
    plt.plot(horas, [r["indice"] for r in res_original], marker="o", label="Modelo original")
    plt.plot(horas, [r["indice"] for r in res_ajustado], marker="s", label="Modelo ajustado")
    plt.xlabel("Hora")
    plt.ylabel("Índice de lluvia")
    plt.title("Comparación: modelo original vs ajustado")
    plt.grid(True)
    plt.legend()
    _guardar(archivo)
    plt.show()
