# Gráficas de la práctica. Se guardan en la carpeta graficas/ y se muestran en pantalla.
import math
import os

import matplotlib
if os.name == "posix" and not os.environ.get("DISPLAY") and not os.environ.get("WAYLAND_DISPLAY"):
    matplotlib.use("Agg")       # sin pantalla: solo se guardan los archivos
import matplotlib.pyplot as plt

from modelo import distribuciones
from modelo.resultado import ALFA

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CARPETA = os.path.join(RAIZ, "graficas")


def crear_cuadricula(resultados):
    # Una gráfica por configuración, en dos columnas
    filas = math.ceil(len(resultados) / 2)
    figura, ejes = plt.subplots(filas, 2, figsize=(11, 4 * filas), squeeze=False)
    lista = list(ejes.flat)
    for sobrante in lista[len(resultados):]:
        sobrante.axis("off")
    return figura, lista


def guardar(figura, nombre):
    figura.tight_layout()
    os.makedirs(CARPETA, exist_ok=True)
    figura.savefig(os.path.join(CARPETA, nombre), dpi=150)


def grafica_secuencia(resultados, cantidad=100):
    # Primeros valores de cada configuración (cómo se ve la secuencia generada)
    figura, ejes = crear_cuadricula(resultados)
    for eje, r in zip(ejes, resultados):
        eje.plot(range(1, cantidad + 1), r.numeros[:cantidad], "o-", markersize=3)
        eje.set_title(r.configuracion.nombre, fontsize=10)
        eje.set_xlabel("n")
        eje.set_ylabel("U(n)")
        eje.set_ylim(0, 1)
        eje.grid(True)
    figura.suptitle(f"Primeros {cantidad} números generados")
    guardar(figura, "secuencia.png")


def grafica_dispersion(resultados):
    # Cada punto es (U(n), U(n+1)): si hay estructura, se nota
    figura, ejes = crear_cuadricula(resultados)
    for eje, r in zip(ejes, resultados):
        eje.scatter(r.numeros[:-1], r.numeros[1:], s=2)
        eje.set_title(r.configuracion.nombre, fontsize=10)
        eje.set_xlabel("U(n)")
        eje.set_ylabel("U(n+1)")
        eje.set_aspect("equal")
    figura.suptitle("Relación entre cada número y el siguiente")
    guardar(figura, "dispersion.png")


def grafica_chi(resultados):
    # Frecuencia observada de cada intervalo contra la esperada
    figura, ejes = crear_cuadricula(resultados)
    for eje, r in zip(ejes, resultados):
        k = len(r.chi.observadas)
        eje.bar(range(k), r.chi.observadas, edgecolor="black", label="Observada")
        eje.axhline(r.chi.esperada, color="red", linestyle="--", label="Esperada")
        eje.set_xticks(range(k))
        eje.set_xticklabels([f"{i / k:.1f}" for i in range(k)], fontsize=8)
        eje.set_title(f"{r.configuracion.nombre}\nchi2 = {r.chi.chi2:.2f}, p = {r.chi.p:.4f}", fontsize=10)
        eje.set_xlabel("Inicio del intervalo")
        eje.set_ylabel("Cantidad de valores")
        eje.legend(fontsize=8)
    figura.suptitle("Chi-cuadrado: frecuencias observadas y esperadas")
    guardar(figura, "chi_cuadrado.png")


def grafica_campana_chi(resultados):
    # Curva de campana de la Chi-cuadrado: el área a la derecha del estadístico es el valor p
    grados = resultados[0].chi.grados
    critico = resultados[0].chi.critico
    limite = 30.0
    xs = [i * limite / 400 for i in range(1, 401)]
    ys = [distribuciones.densidad_chi(x, grados) for x in xs]
    figura, ejes = crear_cuadricula(resultados)
    for eje, r in zip(ejes, resultados):
        eje.plot(xs, ys, color="black")
        zona = [x for x in xs if x >= critico]
        eje.fill_between(zona, [distribuciones.densidad_chi(x, grados) for x in zona],
                         color="red", alpha=0.3, label=f"Zona de rechazo (alfa = {ALFA})")
        eje.axvline(critico, color="red", linestyle="--", label=f"Crítico = {critico:.2f}")
        if r.chi.chi2 <= limite:
            eje.axvline(r.chi.chi2, color="blue", linewidth=2, label=f"Observado = {r.chi.chi2:.2f}")
        else:
            eje.annotate(f"Observado = {r.chi.chi2:.1f}\n(fuera de la escala)", xy=(limite, 0), xytext=(limite - 11, 0.05),
                         arrowprops={"arrowstyle": "->", "color": "blue"}, color="blue")
        eje.set_title(f"{r.configuracion.nombre}\np = {r.chi.p:.4f}", fontsize=10)
        eje.set_xlabel("chi2")
        eje.set_ylabel("Densidad")
        eje.set_xlim(0, limite)
        eje.legend(fontsize=8)
    figura.suptitle(f"Distribución Chi-cuadrado con {grados} grados de libertad")
    guardar(figura, "chi_campana.png")


def grafica_ks(resultados):
    # Distribución acumulada empírica contra la uniforme teórica F(x) = x
    figura, ejes = crear_cuadricula(resultados)
    for eje, r in zip(ejes, resultados):
        ordenados = sorted(r.numeros)
        n = len(ordenados)
        eje.step(ordenados, [(i + 1) / n for i in range(n)], where="post", label="Empírica")
        eje.plot([0, 1], [0, 1], color="red", linestyle="--", label="Teórica U(0,1)")
        eje.set_title(f"{r.configuracion.nombre}\nD = {r.ks.d:.4f}, p = {r.ks.p:.4f}", fontsize=10)
        eje.set_xlabel("x")
        eje.set_ylabel("F(x)")
        eje.grid(True)
        eje.legend(fontsize=8)
    figura.suptitle("Kolmogorov-Smirnov: distribución acumulada")
    guardar(figura, "ks_acumulada.png")


def grafica_diferencias_ks(resultados):
    # Distancia entre la empírica y la teórica en cada punto; el máximo es el estadístico D
    figura, ejes = crear_cuadricula(resultados)
    for eje, r in zip(ejes, resultados):
        ordenados = sorted(r.numeros)
        n = len(ordenados)
        diferencias = [max(abs((i + 1) / n - u), abs(u - i / n)) for i, u in enumerate(ordenados)]
        eje.plot(ordenados, diferencias, linewidth=0.8, label="Diferencia")
        eje.axhline(r.ks.critico, color="red", linestyle="--", label=f"D crítico = {r.ks.critico:.4f}")
        eje.axhline(r.ks.d, color="green", linestyle=":", label=f"D observado = {r.ks.d:.4f}")
        eje.set_title(r.configuracion.nombre, fontsize=10)
        eje.set_xlabel("x")
        eje.set_ylabel("|Fn(x) - F(x)|")
        eje.grid(True)
        eje.legend(fontsize=8)
    figura.suptitle("Kolmogorov-Smirnov: diferencia entre la empírica y la teórica")
    guardar(figura, "ks_diferencias.png")


def texto_p(p):
    return "p < 0.0001" if p < 0.0001 else f"p = {p:.4f}"


def grafica_valores_p(resultados):
    # Resumen de la decisión: una barra por debajo de la línea roja rechaza H0
    nombres = [r.configuracion.nombre for r in resultados]
    posiciones = list(range(len(resultados)))
    figura, eje = plt.subplots(figsize=(10, 5))
    barras_chi = eje.bar([i - 0.2 for i in posiciones], [r.chi.p for r in resultados], 0.4, label="Chi-cuadrado")
    barras_ks = eje.bar([i + 0.2 for i in posiciones], [r.ks.p for r in resultados], 0.4, label="Kolmogorov-Smirnov")
    for barra, r in zip(barras_chi, resultados):
        eje.text(barra.get_x() + 0.2, r.chi.p + 0.02, texto_p(r.chi.p), ha="center", fontsize=8)
    for barra, r in zip(barras_ks, resultados):
        eje.text(barra.get_x() + 0.2, r.ks.p + 0.02, texto_p(r.ks.p), ha="center", fontsize=8)
    eje.axhline(ALFA, color="red", linestyle="--", label=f"alfa = {ALFA}")
    eje.set_ylim(0, 1.1)
    eje.set_xticks(posiciones)
    eje.set_xticklabels(nombres, fontsize=8)
    eje.set_ylabel("Valor p")
    eje.set_title("Valores p de cada configuración (por debajo de alfa se rechaza H0)")
    eje.legend()
    guardar(figura, "valores_p.png")


def mostrar():
    try:
        plt.show()
    except Exception:
        pass
