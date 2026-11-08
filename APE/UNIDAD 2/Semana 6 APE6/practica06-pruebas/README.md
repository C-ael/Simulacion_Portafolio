# Práctica 06: Validación estadística de números pseudoaleatorios (Chi-cuadrado y Kolmogorov-Smirnov)

Se generan números con un generador congruencial lineal (LCG) y se comprueba, con dos pruebas de bondad de ajuste, si se comportan como una distribución uniforme en [0, 1]. Todo está programado en Python y en Java, y los resultados de los dos lenguajes se comparan.

| | |
|---|---|
| Asignatura | Simulación, ciclo 5 (Carrera de Computación, UNL) |
| Docente | José O. Guamán Q. |
| Estudiante | Cael Alejandro Soto Castillo. |
| Práctica | 06: Validación estadística de números pseudoaleatorios mediante Chi-cuadrado y Kolmogorov-Smirnov |

**Contenido:** [1. Descripción](#1-descripción) · [2. Tecnologías](#2-tecnologías) · [3. Instalación y ejecución](#3-instalación-y-ejecución) · [4. Uso](#4-uso) · [5. Configuración](#5-configuración) · [6. Estructura](#6-estructura-del-proyecto) · [7. Información adicional](#7-información-adicional)

---

## 1. Descripción

La guía plantea una hipótesis y un nivel de significancia:

```text
H0: X ~ U(0,1)      (los números siguen una distribución uniforme)
H1: X no sigue U(0,1)
α = 0.05
```

El programa sigue los tres algoritmos de la guía:

1. **Generación (LCG).** `X(n+1) = (a · X(n) + c) mod m` y `U(n) = X(n) / m`, con 10 000 números por configuración.
2. **Chi-cuadrado.** Divide [0, 1] en 10 intervalos, cuenta cuántos números caen en cada uno y compara con la frecuencia esperada (1000). Los grados de libertad son 10 − 1 = 9.
3. **Kolmogorov-Smirnov.** Ordena los números, calcula las diferencias positiva (D+) y negativa (D−) entre la distribución acumulada empírica y la teórica, y toma la mayor como estadístico D.

En las dos pruebas, si el valor p es mayor o igual a 0.05 no se rechaza H0; si es menor, se rechaza. Para cumplir el objetivo de comparar configuraciones del generador, se prueban cuatro:

| Configuración | a | c | m | Semilla |
|---|---:|---:|---:|---:|
| Guia semilla 12345 (la de la guía) | 1664525 | 1013904223 | 2³² | 12345 |
| Guia semilla 54321 | 1664525 | 1013904223 | 2³² | 54321 |
| RANDU | 65539 | 0 | 2³¹ | 1 |
| Parametros malos m=16 | 5 | 3 | 16 | 1 |

Cada lenguaje guarda sus secuencias y sus resultados en CSV, y Python compara los suyos con los de Java.

## 2. Tecnologías

| Herramienta | Versión | Para qué se usa |
|---|---|---|
| Python | 3.8 o posterior | Generador, pruebas, comparación con Java y gráficas. |
| Matplotlib | ver `requirements.txt` | Gráficas. |
| Java (JDK) | 11 o posterior | Generador, pruebas y CSV. Solo biblioteca estándar. |
| MVC | | Organización del código en modelo, vista y controlador, en los dos lenguajes. |

Los valores p se calculan con fórmulas propias, sin SciPy ni otras librerías.

## 3. Instalación y ejecución

Pensado para Ubuntu. Instala el JDK y las dependencias de Python:

```bash
sudo apt install default-jdk python3-venv

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Opción rápida.** Desde la raíz del proyecto, un solo comando compila y ejecuta Java y después Python:

```bash
./ejecutar.sh
```

Si no te deja ejecutarlo, dale permiso con `chmod +x ejecutar.sh`.

**Paso a paso.** Python lee el CSV que genera Java, así que Java va primero:

```bash
javac -encoding UTF-8 -d java/build $(find java/src -name "*.java")
java -cp java/build Main
python3 python/main.py
```

Java se ejecuta desde la raíz del proyecto, porque guarda el archivo en `resultados/`. Cada ejecución reemplaza los archivos anteriores.

## 4. Uso

Al ejecutar `./ejecutar.sh` pasa esto:

1. **Java** genera los 10 000 números de cada configuración, aplica las dos pruebas y muestra, para cada una: los primeros 10 números, las frecuencias observadas y esperadas, chi², grados de libertad, el chi² crítico, D+, D−, D, el D crítico, los valores p y la decisión. Guarda cada secuencia (`secuencia_java_1.csv` a `_4.csv`) y, al final de un resumen, `resultados/pruebas_java.csv`.
2. **Python** hace lo mismo, guarda sus secuencias y `resultados/pruebas_python.csv`, y muestra una tabla con cuántos de los 10 000 números coinciden con los de Java y si coinciden chi², p de chi², D y p de KS.
3. Python guarda siete gráficas en `graficas/` y las muestra en pantalla (cierra cada ventana para ver la siguiente).

Si ejecutas Python sin haber ejecutado Java, hace todo lo demás y avisa que falta la comparación. Si no hay pantalla (por ejemplo, por SSH), solo guarda las gráficas.

## 5. Configuración

Todo está al inicio de cada controlador:

| Parámetro | Valor | Dónde cambiarlo |
|---|---:|---|
| Números por configuración | 10000 | `CANTIDAD` |
| Intervalos de Chi-cuadrado | 10 | `INTERVALOS` |
| Configuraciones (nombre, a, c, m, semilla) | 4 | `CONFIGURACIONES` |
| Nivel de significancia | 0.05 | `ALFA` (Python: `modelo/resultado.py`; Java: `modelo/Resultado.java`) |

- Python: `python/controlador/controlador.py`
- Java: `java/src/controlador/Controlador.java`

Para probar otro generador, agrega una línea a `CONFIGURACIONES` en los dos controladores con el mismo nombre. En Java hay que volver a compilar. Las gráficas dibujan las primeras cuatro configuraciones de la lista.

## 6. Estructura del proyecto

```text
practica06-pruebas/
├── README.md
├── .gitignore
├── requirements.txt
├── ejecutar.sh
├── python/
│   ├── main.py
│   ├── modelo/
│   │   ├── configuracion.py
│   │   ├── generador_lcg.py
│   │   ├── prueba_chi.py
│   │   ├── prueba_ks.py
│   │   ├── distribuciones.py
│   │   ├── resultado.py
│   │   └── comparador.py
│   ├── vista/
│   │   ├── consola.py
│   │   ├── archivo_csv.py
│   │   └── graficas.py
│   └── controlador/
│       └── controlador.py
├── java/
│   └── src/
│       ├── Main.java
│       ├── modelo/
│       │   ├── Configuracion.java
│       │   ├── GeneradorLCG.java
│       │   ├── PruebaChi.java
│       │   ├── PruebaKS.java
│       │   ├── Distribuciones.java
│       │   ├── Resultado.java
│       │   ├── ResultadoChi.java
│       │   └── ResultadoKS.java
│       ├── vista/
│       │   ├── Consola.java
│       │   └── ArchivoCsv.java
│       └── controlador/
│           └── Controlador.java
├── resultados/
│   ├── secuencia_java_1.csv ... secuencia_java_4.csv
│   ├── secuencia_python_1.csv ... secuencia_python_4.csv
│   ├── pruebas_java.csv
│   └── pruebas_python.csv
├── graficas/
│   ├── secuencia.png
│   ├── dispersion.png
│   ├── chi_cuadrado.png
│   ├── chi_campana.png
│   ├── ks_acumulada.png
│   ├── ks_diferencias.png
│   └── valores_p.png
└── docs/
```

| Parte | Python | Java |
|---|---|---|
| Fórmula del LCG (Actividad 1) | `modelo/generador_lcg.py` | `modelo/GeneradorLCG.java` |
| Prueba Chi-cuadrado (Algoritmo 2) | `modelo/prueba_chi.py` | `modelo/PruebaChi.java` |
| Prueba KS (Algoritmo 3) | `modelo/prueba_ks.py` | `modelo/PruebaKS.java` |
| Valores p y valores críticos | `modelo/distribuciones.py` | `modelo/Distribuciones.java` |
| Parámetros de una configuración | `modelo/configuracion.py` | `modelo/Configuracion.java` |
| Resultados de las pruebas | `modelo/resultado.py` | `Resultado`, `ResultadoChi`, `ResultadoKS` |
| Comparar con Java | `modelo/comparador.py` | no tiene |
| Salida por consola | `vista/consola.py` | `vista/Consola.java` |
| Guardar el CSV | `vista/archivo_csv.py` | `vista/ArchivoCsv.java` |
| Gráficas | `vista/graficas.py` | no tiene |
| Orden de los pasos | `controlador/controlador.py` | `controlador/Controlador.java` |

El flujo en los dos lenguajes es `Main → controlador → modelo → vista`. La carpeta `docs/` es para el informe. `java/build/` y `venv/` son locales y no se suben.

## 7. Información adicional

### Resultados

Con 10 000 números por configuración, α = 0.05 y 9 grados de libertad (Python y Java dan lo mismo):

| Configuración | χ² | p (χ²) | D (KS) | p (KS) | Decisión |
|---|---:|---:|---:|---:|---|
| Guia semilla 12345 | 14.160 | 0.1167 | 0.00596 | 0.8686 | No se rechaza H0 |
| Guia semilla 54321 | 7.234 | 0.6128 | 0.00748 | 0.6288 | No se rechaza H0 |
| RANDU | 8.812 | 0.4548 | 0.00636 | 0.8127 | No se rechaza H0 |
| Parametros malos m=16 | 937.500 | ≈ 0 | 0.06250 | ≈ 0 | Se rechaza H0 |

- Con los parámetros de la guía, las dos semillas son compatibles con una uniforme en las dos pruebas.
- RANDU también pasa estas dos pruebas: miran cómo se reparten los valores, no la relación entre valores consecutivos.
- Con m = 16 solo existen 16 valores distintos, y las dos pruebas lo detectan: las frecuencias quedan desiguales (chi² muy alto) y la acumulada se ve como una escalera (D grande).

### Gráficas

Todas tienen un cuadro por configuración (menos `valores_p.png`):

| Archivo | Qué muestra | Para qué sirve al explicar |
|---|---|---|
| `secuencia.png` | Los primeros 100 números generados. | Cómo se ve la secuencia del LCG. |
| `dispersion.png` | Cada punto es (U(n), U(n+1)). | Si hay estructura entre un número y el siguiente: la guía llena el cuadrado; con m = 16 solo hay 16 puntos. |
| `chi_cuadrado.png` | Frecuencia observada de cada intervalo contra la esperada (línea roja). | De dónde sale el estadístico χ². |
| `chi_campana.png` | Curva de campana de la Chi-cuadrado con 9 grados de libertad, con la zona de rechazo (α = 0.05), el valor crítico y el χ² observado. | Si la línea azul cae fuera de la zona roja no se rechaza H0; el área a la derecha de la línea azul es el valor p. |
| `ks_acumulada.png` | Distribución acumulada empírica contra la teórica U(0,1). | Qué compara la prueba KS. |
| `ks_diferencias.png` | Distancia entre las dos acumuladas en cada punto, con el D observado y el D crítico. | El máximo de esta curva es el estadístico D. |
| `valores_p.png` | Los valores p de las dos pruebas contra α. | Resumen de la decisión de cada configuración. |

### Limitaciones

- Pasar las pruebas no demuestra que el generador sea aleatorio; solo que no se rechazó H0 con esta muestra. Con otra semilla o cantidad el resultado puede cambiar.
- El valor p de KS usa la aproximación para muestras grandes; con SciPy (cálculo exacto) difiere en el tercer decimal. El de Chi-cuadrado coincide con SciPy.
- La tabla de "Resultados esperados" de la guía (N, π estimado, error, tiempos) corresponde a otra práctica y no se usa aquí.
- Las pruebas evalúan uniformidad, no independencia entre valores consecutivos.
- Con m = 16 hay solo 16 valores posibles, así que esa configuración se incluye únicamente como ejemplo de un generador mal configurado.
