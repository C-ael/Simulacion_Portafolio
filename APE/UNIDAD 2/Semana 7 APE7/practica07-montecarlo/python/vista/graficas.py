# Gráficas de la práctica. Se guardan en la carpeta graficas/ y se muestran en pantalla.
import math
import os

import matplotlib
if os.name == "posix" and not os.environ.get("DISPLAY") and not os.environ.get("WAYLAND_DISPLAY"):
    matplotlib.use("Agg")       # sin pantalla: solo se guardan los archivos
import matplotlib.pyplot as plt

from modelo.error import desviacion_teorica, error_medio_teorico
from modelo.pruebas_chi import ALFA

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CARPETA = os.path.join(RAIZ, "graficas")
CRITICO_CHI = 3.8415            # chi2 crítico con 1 grado de libertad y alfa = 0.05


def guardar(figura, nombre):
    figura.tight_layout()
    os.makedirs(CARPETA, exist_ok=True)
    figura.savefig(os.path.join(CARPETA, nombre), dpi=150)


def grafica_puntos(datos):
    # Los puntos lanzados al cuadrado: azul = dentro del círculo, naranja = fuera
    figura, ejes = plt.subplots(2, 2, figsize=(10, 10))
    angulos = [2 * math.pi * i / 200 for i in range(201)]
    for eje, (n, xs, ys, dentro, pi) in zip(ejes.flat, datos):
        azul = [(x, y) for x, y, d in zip(xs, ys, dentro) if d]
        naranja = [(x, y) for x, y, d in zip(xs, ys, dentro) if not d]
        eje.scatter([p[0] for p in azul], [p[1] for p in azul], s=2, color="tab:blue", label="Dentro")
        eje.scatter([p[0] for p in naranja], [p[1] for p in naranja], s=2, color="tab:orange", label="Fuera")
        eje.plot([math.cos(a) for a in angulos], [math.sin(a) for a in angulos], color="black", linewidth=1)
        eje.set_aspect("equal")
        eje.set_title(f"N = {n:,}  →  pi ≈ {pi:.4f}".replace(",", " ")
                      + ("" if len(xs) == n else f"\n(se dibujan los primeros {len(xs):,})".replace(",", " ")),
                      fontsize=10)
        eje.legend(loc="upper right", fontsize=7, markerscale=4)
    figura.suptitle("Puntos lanzados en el cuadrado y círculo inscrito")
    guardar(figura, "puntos.png")


def grafica_estimacion(tamanos, python, java):
    # Estimación de pi para cada tamaño de muestra
    figura, eje = plt.subplots(figsize=(9, 5))
    estilos = [("LCG propio", "Python", "o-", "tab:blue"), ("LCG propio", "Java", "x--", "tab:cyan"),
               ("Nativo", "Python", "s-", "tab:red"), ("Nativo", "Java", "^--", "tab:orange")]
    for generador, lenguaje, estilo, color in estilos:
        fuente = python if lenguaje == "Python" else java
        if fuente is None:
            continue
        eje.plot(tamanos, [fuente[(generador, n)].pi for n in tamanos], estilo, color=color,
                 label=f"{generador} ({lenguaje})", markersize=7)
    eje.axhline(math.pi, color="black", linestyle=":", label="pi real")
    eje.set_xscale("log")
    eje.set_xlabel("N (cantidad de puntos)")
    eje.set_ylabel("Estimación de pi")
    eje.set_title("Estimación de pi según el tamaño de muestra")
    eje.grid(True)
    eje.legend()
    guardar(figura, "estimacion_pi.png")


def grafica_error(tamanos, resumenes, python):
    # Error absoluto contra N, en escala logarítmica: baja aproximadamente como 1/raíz(N)
    figura, eje = plt.subplots(figsize=(9, 5.5))
    for i, n in enumerate(tamanos):
        errores = resumenes[n].errores
        eje.scatter([n] * len(errores), errores, s=18, color="tab:gray", alpha=0.6,
                    label="Cada repetición" if i == 0 else None)
    eje.plot(tamanos, [resumenes[n].error_medio for n in tamanos], "o-", color="tab:blue", label="Error medio observado")
    eje.plot(tamanos, [error_medio_teorico(n) for n in tamanos], "--", color="red", label="Error medio teórico")
    eje.plot(tamanos, [python[("LCG propio", n)].error for n in tamanos], "s", color="green", markersize=8,
             label="Ejecución principal (tabla de la ficha)")
    eje.set_xscale("log")
    eje.set_yscale("log")
    eje.set_xlabel("N (cantidad de puntos)")
    eje.set_ylabel("Error absoluto |pi estimado - pi|")
    eje.set_title("Error absoluto según el tamaño de muestra")
    eje.grid(True, which="both", alpha=0.4)
    eje.legend()
    guardar(figura, "error_vs_n.png")


def grafica_convergencia(puntos, estimaciones):
    # Una sola ejecución larga: la estimación fluctúa y se va acercando a pi
    figura, eje = plt.subplots(figsize=(9, 5))
    eje.plot(puntos, estimaciones, color="tab:blue", linewidth=1, label="Estimación de pi")
    eje.axhline(math.pi, color="black", linestyle=":", label="pi real")
    eje.fill_between(puntos, [math.pi - 1.96 * desviacion_teorica(n) for n in puntos],
                     [math.pi + 1.96 * desviacion_teorica(n) for n in puntos],
                     color="red", alpha=0.15, label="Zona esperada (95 %)")
    eje.set_xscale("log")
    eje.set_xlabel("Puntos lanzados")
    eje.set_ylabel("Estimación de pi")
    eje.set_ylim(2.9, 3.4)
    eje.set_title("Convergencia de la estimación en una ejecución")
    eje.grid(True)
    eje.legend()
    guardar(figura, "convergencia.png")


def grafica_tiempos(tamanos, python, java):
    # Tiempo de ejecución de cada lenguaje, en escala logarítmica
    figura, ejes = plt.subplots(1, 2, figsize=(11, 5))
    posiciones = range(len(tamanos))
    for eje, generador in zip(ejes, ["LCG propio", "Nativo"]):
        ancho = 0.4 if java is not None else 0.6
        desplazamiento = 0.2 if java is not None else 0
        eje.bar([i - desplazamiento for i in posiciones], [python[(generador, n)].tiempo_ms for n in tamanos],
                ancho, label="Python", color="tab:blue")
        if java is not None:
            eje.bar([i + 0.2 for i in posiciones], [java[(generador, n)].tiempo_ms for n in tamanos],
                    0.4, label="Java", color="tab:orange")
        eje.set_yscale("log")
        eje.set_xticks(list(posiciones))
        eje.set_xticklabels([f"{n:,}".replace(",", " ") for n in tamanos])
        eje.set_xlabel("N (cantidad de puntos)")
        eje.set_ylabel("Tiempo (ms, escala logarítmica)")
        eje.set_title(f"Generador: {generador}")
        eje.grid(True, axis="y", alpha=0.4)
        eje.legend()
    figura.suptitle("Tiempo de ejecución según el tamaño de muestra")
    guardar(figura, "tiempos.png")


def grafica_chi(tamanos, python, java, homogeneidad):
    # Estadísticos Chi-cuadrado contra el valor crítico (por encima de la línea se rechaza H0)
    figura, ejes = plt.subplots(1, 2, figsize=(11, 5))
    posiciones = list(range(len(tamanos)))
    series = [("LCG propio (Python)", [python[("LCG propio", n)].chi2 for n in tamanos])]
    series.append(("Nativo (Python)", [python[("Nativo", n)].chi2 for n in tamanos]))
    if java is not None:
        series.append(("Nativo (Java)", [java[("Nativo", n)].chi2 for n in tamanos]))
    ancho = 0.8 / len(series)
    for k, (nombre, valores) in enumerate(series):
        ejes[0].bar([i + k * ancho - 0.4 + ancho / 2 for i in posiciones], valores, ancho, label=nombre)
    ejes[0].set_title("Bondad de ajuste: Nc observado contra el esperado")
    if homogeneidad:
        for k, generador in enumerate(["LCG propio", "Nativo"]):
            ejes[1].bar([i + k * 0.4 - 0.2 for i in posiciones],
                        [homogeneidad[(generador, n)].chi2 for n in tamanos], 0.4, label=generador)
        ejes[1].set_title("Homogeneidad: Python contra Java\n(LCG propio = 0: resultados idénticos)")
    else:
        ejes[1].text(0.5, 0.5, "Falta ejecutar Java", ha="center", transform=ejes[1].transAxes)
    for eje in ejes:
        eje.axhline(CRITICO_CHI, color="red", linestyle="--", label=f"Crítico = {CRITICO_CHI} (alfa = {ALFA})")
        eje.set_xticks(posiciones)
        eje.set_xticklabels([f"{n:,}".replace(",", " ") for n in tamanos])
        eje.set_xlabel("N (cantidad de puntos)")
        eje.set_ylabel("chi2 (1 grado de libertad)")
        eje.set_ylim(0, 5.2)
        eje.legend(fontsize=8, loc="upper center", ncol=2)
    figura.suptitle("Pruebas Chi-cuadrado")
    guardar(figura, "chi_cuadrado.png")


def mostrar():
    try:
        plt.show()
    except Exception:
        pass
