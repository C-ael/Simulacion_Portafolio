"""gráficas con matplotlib."""

import os
import matplotlib.pyplot as plt

CARPETA = "graficas"

# Para distinguir las líneas (el determinístico y el continuo casi se superponen)
ESTILOS = {
    "Determinístico": {"linestyle": "-"},
    "Discreto": {"marker": "o", "linestyle": "--"},
    "Estocástico": {"marker": "s", "linestyle": "-"},
    "Continuo (Euler)": {"linestyle": ":", "linewidth": 3},
}


def _guardar(archivo):
    os.makedirs(CARPETA, exist_ok=True)
    plt.savefig(os.path.join(CARPETA, archivo), dpi=120)


def grafica_comparacion(resultados, p):
    plt.figure(figsize=(10, 5))
    for nombre, (t, poblacion) in resultados.items():
        plt.plot(t, poblacion, label=nombre, **ESTILOS.get(nombre, {}))
    plt.scatter(range(len(p.datos)), p.datos, color="black", zorder=5,
                label="Datos de entrada")
    plt.xlabel("Tiempo")
    plt.ylabel("Población")
    plt.title("Comparación de los cuatro modelos de crecimiento poblacional")
    plt.grid(True)
    plt.legend()
    _guardar("comparacion_modelos.png")
    plt.show()


def grafica_influencia_r(curvas):
    """curvas: lista de (r, t, población) del modelo determinístico."""
    plt.figure(figsize=(10, 5))
    for r, t, poblacion in curvas:
        plt.plot(t, poblacion, label=f"r = {r:.2f}")
    plt.xlabel("Tiempo")
    plt.ylabel("Población")
    plt.title("Influencia de la tasa r (crecimiento y decrecimiento)")
    plt.grid(True)
    plt.legend()
    _guardar("influencia_r.png")
    plt.show()


def grafica_efecto_sigma(curvas):
    """curvas: lista de (sigma, t, población) del modelo estocástico."""
    plt.figure(figsize=(10, 5))
    for sigma, t, poblacion in curvas:
        plt.plot(t, poblacion, marker="o", label=f"sigma = {sigma}")
    plt.xlabel("Tiempo")
    plt.ylabel("Población")
    plt.title("Efecto de la aleatoriedad (modelo estocástico)")
    plt.grid(True)
    plt.legend()
    _guardar("efecto_sigma.png")
    plt.show()
