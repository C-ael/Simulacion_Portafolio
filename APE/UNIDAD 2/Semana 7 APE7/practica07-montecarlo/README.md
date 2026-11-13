# Práctica 07: Estimación de π mediante el método de Monte Carlo

Se estima el valor de π lanzando puntos al azar dentro de un cuadrado con un círculo inscrito. El mismo experimento se programa en Python y en Java, se analiza cómo cambia el error al aumentar la cantidad de puntos y se comparan los resultados de los dos lenguajes con pruebas Chi-cuadrado.

| | |
|---|---|
| Asignatura | Simulación, ciclo 5 (Carrera de Computación, UNL) |
| Docente | José O. Guamán Q. |
| Práctica | 07: Estimación de resultados mediante el método de Monte Carlo |

**Contenido:** [1. Descripción](#1-descripción) · [2. Tecnologías](#2-tecnologías) · [3. Instalación y ejecución](#3-instalación-y-ejecución) · [4. Uso](#4-uso) · [5. Configuración](#5-configuración) · [6. Estructura](#6-estructura-del-proyecto) · [7. Información adicional](#7-información-adicional)

---

## 1. Descripción

El método de Monte Carlo usa muestras aleatorias para aproximar un resultado. Aquí se aproxima π con la idea de "lanzar dardos":

- Se dibuja un cuadrado de lado 2 (de −1 a 1) y, dentro, un círculo de radio 1.
- Se lanzan N puntos al azar dentro del cuadrado y se cuentan los que caen dentro del círculo (Nc), es decir, los que cumplen x² + y² ≤ 1.
- El círculo ocupa π/4 del cuadrado, así que la proporción de puntos dentro es aproximadamente π/4:

```text
π ≈ 4 · Nc / N
```

El programa sigue lo que pide la guía:

1. Ejecutar el experimento con 1 000, 10 000, 100 000 y 1 000 000 de puntos.
2. Registrar la estimación de π, el error absoluto `|π estimado − π|` y el tiempo de ejecución en cada lenguaje.
3. Repetir todo en Java y comparar resultados y tiempos.

Para analizar bien el efecto del tamaño de muestra y responder las preguntas de la guía, el programa además:

- **Usa dos generadores de números aleatorios.** El **LCG propio** (el mismo de las prácticas anteriores, programado igual en los dos lenguajes, por lo que da exactamente los mismos números) y el **generador nativo** de cada lenguaje (`random` en Python y `java.util.Random` en Java, que dan números distintos aunque se use la misma semilla).
- **Repite el experimento 10 veces por tamaño** con semillas distintas, porque una sola ejecución puede tener suerte o mala suerte y no muestra la tendencia del error.
- **Compara con pruebas Chi-cuadrado** (ver más abajo).

Pruebas estadísticas (nivel de significancia α = 0.05, 1 grado de libertad, valor crítico 3.8415):

| Prueba | Qué compara | Hipótesis nula H0 |
|---|---|---|
| Bondad de ajuste | Los puntos dentro/fuera observados contra los esperados si π fuera el real (Nc esperado = N · π/4). | Los resultados son compatibles con el valor real de π. |
| Homogeneidad (tabla 2×2) | Los puntos dentro/fuera de Python contra los de Java. | Python y Java obtienen la misma proporción de puntos dentro. |

Si el valor p es mayor o igual a 0.05, no se rechaza H0.

## 2. Tecnologías

| Herramienta | Versión | Para qué se usa |
|---|---|---|
| Python | 3.8 o posterior | Experimento, pruebas, comparación con Java y gráficas. |
| Matplotlib | ver `requirements.txt` | Gráficas. |
| Java (JDK) | 11 o posterior | Experimento y pruebas. Solo biblioteca estándar. |
| MVC | | Organización del código en modelo, vista y controlador, en los dos lenguajes. |

El valor p de Chi-cuadrado se calcula con fórmulas propias, sin SciPy ni otras librerías.

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

**Paso a paso.** Python lee los archivos que genera Java, así que Java va primero:

```bash
javac -encoding UTF-8 -d java/build $(find java/src -name "*.java")
java -cp java/build Main
python3 python/main.py
```

Java se ejecuta desde la raíz del proyecto, porque guarda los archivos en `resultados/`. Cada ejecución reemplaza los archivos anteriores. Python tarda unos 10 segundos porque lanza varios millones de puntos.

## 4. Uso

Al ejecutar `./ejecutar.sh` pasa esto:

1. **Java** hace el experimento con los dos generadores y los cuatro tamaños, muestra la tabla de resultados (N, Nc, π estimado, error y tiempo) y la prueba de bondad de ajuste, hace las 10 repeticiones por tamaño y guarda `resultados/resultados_java.csv` y `resultados/repeticiones_java.csv`.
2. **Python** hace lo mismo con su propio código y guarda `resultados_python.csv` y `repeticiones_python.csv`.
3. Python lee los archivos de Java y muestra:
   - la tabla de la guía con los dos lenguajes lado a lado (π, error y tiempo);
   - la bondad de ajuste de cada generador;
   - la homogeneidad Python contra Java (tabla 2×2);
   - una tabla que indica si Java obtuvo exactamente los mismos resultados;
   - el error medio de las repeticiones frente al error teórico.
4. Python guarda seis gráficas en `graficas/` y las muestra en pantalla, una por una: cierra cada ventana para ver la siguiente. Si no hay pantalla (por ejemplo, por SSH), solo las guarda.

Si ejecutas Python sin haber ejecutado Java, muestra solo los resultados de Python y avisa que falta la comparación.

## 5. Configuración

Todo está al inicio de cada controlador:

| Parámetro | Valor | Dónde cambiarlo |
|---|---:|---|
| Tamaños de muestra | 1 000, 10 000, 100 000, 1 000 000 | `TAMANOS` |
| Semilla | 12345 | `SEMILLA` |
| Repeticiones por tamaño | 10 | `REPETICIONES` |
| Parámetros del LCG (a, c, m) | 1664525, 1013904223, 2³² | `A`, `C`, `M` |

- Python: `python/controlador/controlador.py`
- Java: `java/src/controlador/Controlador.java`

Si cambias un valor, cámbialo en los dos archivos; si no, los lenguajes harán experimentos distintos y la comparación dará diferencias. En Java hay que volver a compilar. Las gráficas de tamaños suponen que `TAMANOS` tiene cuatro valores.

El experimento principal usa siempre la misma semilla, así que cada ejecución da los mismos resultados (menos los tiempos). Las 10 repeticiones usan las semillas 12345, 12346, 12347…

## 6. Estructura del proyecto

```text
practica07-montecarlo/
├── README.md
├── .gitignore
├── requirements.txt
├── ejecutar.sh
├── python/
│   ├── main.py
│   ├── modelo/
│   │   ├── generador_lcg.py
│   │   ├── generador_nativo.py
│   │   ├── experimento.py
│   │   ├── resultado.py
│   │   ├── error.py
│   │   ├── pruebas_chi.py
│   │   ├── distribuciones.py
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
│       │   ├── Generador.java
│       │   ├── GeneradorLCG.java
│       │   ├── GeneradorNativo.java
│       │   ├── Experimento.java
│       │   ├── ResultadoPi.java
│       │   ├── PruebaChi.java
│       │   └── Distribuciones.java
│       ├── vista/
│       │   ├── Consola.java
│       │   └── ArchivoCsv.java
│       └── controlador/
│           └── Controlador.java
├── resultados/
│   ├── resultados_java.csv
│   ├── resultados_python.csv
│   ├── repeticiones_java.csv
│   └── repeticiones_python.csv
├── graficas/
│   ├── puntos.png
│   ├── estimacion_pi.png
│   ├── error_vs_n.png
│   ├── convergencia.png
│   ├── tiempos.png
│   └── chi_cuadrado.png
└── docs/
```

| Parte | Python | Java |
|---|---|---|
| Generador LCG propio | `modelo/generador_lcg.py` | `modelo/GeneradorLCG.java` |
| Generador nativo del lenguaje | `modelo/generador_nativo.py` | `modelo/GeneradorNativo.java` |
| Experimento Monte Carlo (π ≈ 4·Nc/N) | `modelo/experimento.py` | `modelo/Experimento.java` |
| Resultado de un experimento | `modelo/resultado.py` | `modelo/ResultadoPi.java` |
| Error teórico y resumen de repeticiones | `modelo/error.py` | no tiene |
| Chi-cuadrado (bondad de ajuste y homogeneidad) | `modelo/pruebas_chi.py` | `modelo/PruebaChi.java` (solo bondad de ajuste) |
| Valor p | `modelo/distribuciones.py` | `modelo/Distribuciones.java` |
| Leer y comparar con Java | `modelo/comparador.py` | no tiene |
| Salida por consola | `vista/consola.py` | `vista/Consola.java` |
| Guardar CSV | `vista/archivo_csv.py` | `vista/ArchivoCsv.java` |
| Gráficas | `vista/graficas.py` | no tiene |
| Orden de los pasos | `controlador/controlador.py` | `controlador/Controlador.java` |

El flujo en los dos lenguajes es `Main → controlador → modelo → vista`. En Java, `Generador.java` es una interfaz mínima para poder usar cualquiera de los dos generadores con el mismo código. La carpeta `docs/` es para el informe. `java/build/` y `venv/` son locales y no se suben.

## 7. Información adicional

### Resultados (semilla 12345)

Con el **LCG propio**, Python y Java dan exactamente los mismos resultados (mismo Nc en los cuatro tamaños y en las 10 repeticiones); solo cambia el tiempo:

| N | π estimado | Error absoluto | Chi-cuadrado | Valor p |
|---:|---:|---:|---:|---:|
| 1 000 | 3.188000 | 0.046407 | 0.7986 | 0.3715 |
| 10 000 | 3.151600 | 0.010007 | 0.3714 | 0.5423 |
| 100 000 | 3.133240 | 0.008353 | 2.5871 | 0.1077 |
| 1 000 000 | 3.141948 | 0.000355 | 0.0468 | 0.8287 |

Con el **generador nativo**, cada lenguaje da números distintos y, por eso, resultados distintos:

| N | π Python | π Java | Error Python | Error Java | p (Python) | p (Java) |
|---:|---:|---:|---:|---:|---:|---:|
| 1 000 | 3.140000 | 3.232000 | 0.001593 | 0.090407 | 0.9755 | 0.0817 |
| 10 000 | 3.133200 | 3.148000 | 0.008393 | 0.006407 | 0.6093 | 0.6964 |
| 100 000 | 3.137800 | 3.141360 | 0.003793 | 0.000233 | 0.4652 | 0.9643 |
| 1 000 000 | 3.143076 | 3.142416 | 0.001483 | 0.000823 | 0.3664 | 0.6161 |

La prueba de homogeneidad entre los nativos de Python y Java da valores p de 0.2014, 0.5241, 0.6281 y 0.7762 (de menor a mayor N): en ningún tamaño se rechaza H0, es decir, aunque los números son distintos, los dos lenguajes se comportan igual estadísticamente.

**Error según el tamaño de muestra** (promedio de 10 repeticiones con el LCG propio):

| N | Error medio observado | Error medio teórico |
|---:|---:|---:|
| 1 000 | 0.03928 | 0.04143 |
| 10 000 | 0.00692 | 0.01310 |
| 100 000 | 0.00370 | 0.00414 |
| 1 000 000 | 0.00120 | 0.00131 |

El error teórico baja como 1/√N: al multiplicar N por 100 el error se divide por 10. Con solo 10 repeticiones el promedio observado es un poco irregular (por ejemplo, en N = 10 000 salió menor al teórico).

**Tiempos.** Java resulta varias veces más rápido que Python (con el LCG propio, de unas 20 a 30 veces en N = 1 000 000). Los tiempos cambian en cada ejecución y dependen del computador, por eso no se fijan aquí; la tabla completa sale en consola y en `graficas/tiempos.png`.

### Gráficas

| Archivo | Qué muestra | Para qué sirve al explicar |
|---|---|---|
| `puntos.png` | Los puntos lanzados al cuadrado (azul = dentro del círculo, naranja = fuera) para cada tamaño. | La idea del método: la proporción de puntos dentro es π/4. |
| `estimacion_pi.png` | La estimación de π en cada tamaño, para los dos generadores y los dos lenguajes. | Cómo cambia la estimación al aumentar N; las dos líneas del LCG coinciden y las del nativo no. |
| `error_vs_n.png` | Error absoluto contra N en escala logarítmica: cada repetición, el promedio, el error teórico y la ejecución principal. | La relación entre tamaño de muestra y error. |
| `convergencia.png` | Una ejecución de 1 000 000 de puntos, con la estimación cada 1 000 puntos y la zona esperada al 95 %. | Que la estimación se acerca a π con fluctuaciones, y que más puntos no garantiza mejorar en cada paso. |
| `tiempos.png` | Tiempo de Python y de Java por tamaño (escala logarítmica). | Qué lenguaje es más rápido. |
| `chi_cuadrado.png` | Estadístico Chi-cuadrado de la bondad de ajuste y de la homogeneidad contra el valor crítico. | Por qué no se rechaza H0 en ningún caso. |

### Limitaciones

- La guía fija el modelo (estimar π con un círculo inscrito en un cuadrado); aquí no se cambia. Los dos generadores y las repeticiones se agregaron para poder analizar el error y comparar los lenguajes.
- Cada tamaño se ejecuta una vez en la tabla principal y el tiempo se mide con un solo intento. En Java se hace un calentamiento antes de medir, porque la primera ejecución de un bucle es más lenta. Los tiempos de los tamaños pequeños (1 000 puntos) son de décimas de milisegundo y varían mucho.
- Con el generador nativo, Python y Java no usan el mismo algoritmo, por lo que sus números (y estimaciones) son distintos; es el motivo por el que se incluye el LCG propio.
- Las 10 repeticiones son pocas para estimar bien el error promedio; se pueden aumentar en `REPETICIONES` (Python tarda más).
- Una prueba Chi-cuadrado que no se rechaza no demuestra que el resultado sea exacto: solo que es compatible con el azar esperado.
