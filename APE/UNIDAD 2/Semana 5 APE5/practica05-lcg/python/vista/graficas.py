# Gráficas de la secuencia. Se guardan en la carpeta graficas/ y se muestran.
import os
import matplotlib.pyplot as plt

CARPETA = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "graficas")


def guardar(nombre):
    os.makedirs(CARPETA, exist_ok=True)
    plt.savefig(os.path.join(CARPETA, nombre), dpi=150)


def grafica_secuencia(valores1, semilla1, valores2, semilla2, cantidad=100):
    # Primeros valores de U con las dos semillas, para ver que la semilla cambia la secuencia
    plt.figure(figsize=(10, 5))
    plt.plot([n for n, _, _ in valores1[:cantidad]], [u for _, _, u in valores1[:cantidad]],
             "o-", markersize=4, label=f"Semilla {semilla1}")
    plt.plot([n for n, _, _ in valores2[:cantidad]], [u for _, _, u in valores2[:cantidad]],
             "s-", markersize=4, label=f"Semilla {semilla2}")
    plt.title(f"Primeros {cantidad} valores generados")
    plt.xlabel("n")
    plt.ylabel("U(n)")
    plt.grid(True)
    plt.legend()
    guardar("secuencia.png")
    plt.show()


def grafica_histograma(valores, semilla):
    # Si el generador es uniforme, cada intervalo debería tener casi la misma cantidad
    plt.figure(figsize=(10, 5))
    plt.hist([u for _, _, u in valores], bins=10, range=(0, 1), edgecolor="black", label="Frecuencia observada")
    plt.axhline(len(valores) / 10, color="red", linestyle="--", label="Frecuencia esperada")
    plt.title(f"Histograma de {len(valores)} valores (semilla {semilla})")
    plt.xlabel("U")
    plt.ylabel("Cantidad de valores")
    plt.grid(True)
    plt.legend()
    guardar("histograma.png")
    plt.show()


def grafica_dispersion(valores, semilla):
    # Cada punto es (U(n), U(n+1)). Si no hay relación, se llena todo el cuadrado
    us = [u for _, _, u in valores]
    plt.figure(figsize=(7, 7))
    plt.scatter(us[:-1], us[1:], s=2)
    plt.title(f"U(n) contra U(n+1) (semilla {semilla})")
    plt.xlabel("U(n)")
    plt.ylabel("U(n+1)")
    plt.grid(True)
    guardar("dispersion.png")
    plt.show()
