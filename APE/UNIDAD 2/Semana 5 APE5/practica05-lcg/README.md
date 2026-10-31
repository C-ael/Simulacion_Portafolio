# Práctica 05: Generador Congruencial Lineal (LCG) en Python y Java

El mismo generador de números pseudoaleatorios programado en dos lenguajes, para comprobar que con los mismos parámetros producen exactamente la misma secuencia y para estudiar sus propiedades.

| | |
|---|---|
| Asignatura | Simulación, ciclo 5 (Carrera de Computación, UNL) |
| Docente | José O. Guamán Q. |
| Práctica | 05: Implementación y análisis del Generador Congruencial Lineal en Python y Java |

**Contenido:** [1. Descripción](#1-descripción) · [2. Tecnologías](#2-tecnologías) · [3. Instalación y ejecución](#3-instalación-y-ejecución) · [4. Uso](#4-uso) · [5. Configuración](#5-configuración) · [6. Estructura](#6-estructura-del-proyecto) · [7. Información adicional](#7-información-adicional)

---

## 1. Descripción

Un generador congruencial lineal (LCG) produce números "al azar" con una fórmula recursiva. A partir de un valor inicial llamado semilla, cada número se calcula con el anterior:

```text
X(n+1) = (a · X(n) + c) mod m
U(n)   = X(n) / m
```

`X(n)` es un entero entre 0 y m − 1 y `U(n)` es ese mismo valor llevado al intervalo [0, 1).

El proyecto sigue los pasos de la guía:

1. Generar 10 000 valores en Python con a = 1664525, c = 1013904223, m = 2³² y semilla 12345.
2. Hacer lo mismo en Java.
3. Comparar las primeras 20 observaciones (y, de paso, los 10 000 valores).
4. Graficar la secuencia.
5. Analizar el período.
6. Cambiar la semilla y comparar de nuevo.

Cada lenguaje guarda su secuencia en un CSV. El programa de Python lee los CSV de Java, los compara con los suyos y muestra la tabla de coincidencias.

## 2. Tecnologías

| Herramienta | Versión | Para qué se usa |
|---|---|---|
| Python | 3.8 o posterior | Generador, comparación con Java, análisis y gráficas. |
| Matplotlib | ver `requirements.txt` | Gráficas de la secuencia. |
| Java (JDK) | 11 o posterior | Generador, CSV y análisis del período. Solo biblioteca estándar. |
| MVC | | Organización del código en modelo, vista y controlador, en los dos lenguajes. |

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

**Paso a paso.** Python necesita los CSV que genera Java, así que Java va primero:

```bash
javac -encoding UTF-8 -d java/build $(find java/src -name "*.java")
java -cp java/build Main
python3 python/main.py
```

Java se ejecuta desde la raíz del proyecto, porque guarda los archivos en `resultados/`. Cada vez que se ejecuta, los CSV se reemplazan.

**Medir el período completo.** Con m = 2³² son más de 4 mil millones de pasos. Java tarda alrededor de medio minuto, así que solo se hace si se pide:

```bash
./ejecutar.sh periodo
# o, a mano:
java -cp java/build Main periodo
```

## 4. Uso

Al ejecutar `./ejecutar.sh` pasa esto:

1. **Java** genera 10 000 valores con la semilla 12345 y otros 10 000 con la semilla 54321. Muestra las primeras 20 observaciones, la media y la varianza de cada secuencia y el análisis del período. Guarda dos CSV en `resultados/`.
2. **Python** hace lo mismo con su propio generador y guarda sus dos CSV.
3. Python lee los CSV de Java y muestra una tabla con las primeras 20 observaciones de los dos lenguajes, indicando si coinciden. Después indica en cuántos de los 10 000 valores coinciden, con cada semilla.
4. Python muestra las tres gráficas, una por una: cierra cada ventana para ver la siguiente. También quedan guardadas en `graficas/`.

Si ejecutas Python sin haber ejecutado Java, muestra las primeras 20 observaciones de Python y avisa que falta comparar.

## 5. Configuración

Los valores de la guía están al inicio de cada controlador:

| Parámetro | Valor | Dónde cambiarlo |
|---|---:|---|
| a (multiplicador) | 1664525 | `A` |
| c (incremento) | 1013904223 | `C` |
| m (módulo) | 2³² = 4294967296 | `M` |
| Semilla de la guía | 12345 | `SEMILLA` |
| Segunda semilla (paso "cambiar la semilla") | 54321 | `SEMILLA_2` |
| Cantidad de valores | 10000 | `CANTIDAD` |

- Python: `python/controlador/controlador.py`
- Java: `java/src/controlador/Controlador.java`

Si cambias un valor, cámbialo en los dos archivos; si no, los lenguajes generan secuencias distintas y la comparación dará diferencias. En Java hay que volver a compilar.

La semilla es X(0), por eso el primer valor generado es X(1). Las 20 observaciones de la comparación son X(1) a X(20).

## 6. Estructura del proyecto

```text
practica05-lcg/
├── README.md
├── .gitignore
├── requirements.txt
├── ejecutar.sh
├── python/
│   ├── main.py
│   ├── modelo/
│   │   ├── generador_lcg.py
│   │   ├── analisis.py
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
│       │   ├── GeneradorLCG.java
│       │   ├── Valor.java
│       │   └── Analisis.java
│       ├── vista/
│       │   ├── Consola.java
│       │   └── ArchivoCsv.java
│       └── controlador/
│           └── Controlador.java
├── resultados/
│   ├── lcg_python_12345.csv
│   ├── lcg_python_54321.csv
│   ├── lcg_java_12345.csv
│   └── lcg_java_54321.csv
├── graficas/
│   ├── secuencia.png
│   ├── histograma.png
│   └── dispersion.png
└── docs/
```

| Parte | Python | Java |
|---|---|---|
| Fórmula del LCG | `modelo/generador_lcg.py` | `modelo/GeneradorLCG.java` |
| Un valor generado (n, X, U) | tupla `(n, x, u)` | `modelo/Valor.java` |
| Media, varianza, repetidos, período | `modelo/analisis.py` | `modelo/Analisis.java` |
| Leer CSV de Java y comparar | `modelo/comparador.py` | no tiene |
| Salida por consola | `vista/consola.py` | `vista/Consola.java` |
| Guardar el CSV | `vista/archivo_csv.py` | `vista/ArchivoCsv.java` |
| Gráficas | `vista/graficas.py` | no tiene |
| Orden de los pasos | `controlador/controlador.py` | `controlador/Controlador.java` |

El flujo en los dos lenguajes es `Main → controlador → modelo → vista`. La carpeta `docs/` es para el informe. `java/build/` y `venv/` son locales y no se suben.

## 7. Información adicional

### Resultados

Primeras observaciones con la semilla 12345 (las mismas en Python y en Java):

| n | X(n) | U(n) |
|---:|---:|---:|
| 1 | 87628868 | 0.0204026857 |
| 2 | 71072467 | 0.0165478482 |
| 3 | 2332836374 | 0.5431557945 |
| 4 | 2726892157 | 0.6349040561 |
| 5 | 3908547000 | 0.9100295138 |

Con los 10 000 valores de cada semilla:

| Semilla | Media (esperada 0.5) | Varianza (esperada 0.0833) | X repetidos |
|---:|---:|---:|---:|
| 12345 | 0.498770 | 0.083012 | 0 |
| 54321 | 0.498870 | 0.083588 | 0 |

Python y Java coinciden en los 10 000 valores con las dos semillas. Los dos lenguajes dan lo mismo porque X se calcula solo con aritmética de enteros, sin redondeos (en Java el producto a · X cabe en un `long`). Solo U usa decimales, y ahí también coinciden.

### Período

El período es cuántos valores pasan antes de que la secuencia empiece a repetirse. Con el módulo m el máximo posible es m.

Con los parámetros de la guía el período es completo: **m = 4 294 967 296**. El programa Java lo comprueba contando los pasos hasta volver a la semilla (`./ejecutar.sh periodo`).

Para ver cómo afectan los parámetros, los programas también cuentan el período con m = 16:

| a | c | m | Semilla | Período |
|---:|---:|---:|---:|---:|
| 5 | 3 | 16 | 1 | 16 |
| 5 | 0 | 16 | 1 | 4 |
| 1 | 0 | 16 | 3 | 1 |

Con parámetros inadecuados el período se acorta, y en el peor caso el generador se queda repitiendo el mismo valor.

### Gráficas

| Archivo | Qué muestra |
|---|---|
| `secuencia.png` | Los primeros 100 valores de U con las dos semillas. Se ve que cambiar la semilla cambia toda la secuencia. |
| `histograma.png` | Cuántos valores caen en cada décimo de [0, 1). Si el generador es uniforme, todas las barras quedan cerca de la línea roja (1000). |
| `dispersion.png` | Cada punto es (U(n), U(n+1)). Si no hay relación entre un valor y el siguiente, los puntos llenan el cuadrado sin un patrón. |

### Limitaciones

- La secuencia depende por completo de la semilla: la misma semilla siempre da los mismos números. Por eso es pseudoaleatoria y por eso se puede comparar entre lenguajes.
- Con m = 2³², los bits más bajos de X se repiten con períodos mucho más cortos que los bits altos; para simulación sirve, pero no para criptografía.
- Python no cuenta el período completo con m = 2³² porque tardaría horas; eso lo hace Java.
