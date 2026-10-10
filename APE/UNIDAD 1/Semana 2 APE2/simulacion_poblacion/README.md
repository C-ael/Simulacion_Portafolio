# Práctica 02 - Comparación de modelos determinísticos, estocásticos, discretos y continuos

**Asignatura:** Simulación
**Ciclo:** Ciclo 5
**Carrera:** Carrera de Computación - UNL
**Docente:** José O. Guamán Q.
**Estudiante:** Cael Alejandro Soto Castillo.

## 1. Descripción del proyecto

Simula el **crecimiento poblacional** con cuatro modelos y los compara sobre los mismos datos
de entrada (`[1000, 1100, 1250, 1400, 1600, 1850, 2100]`).

**Propósito:** diferenciar los paradigmas de simulación. El proyecto responde a tres preguntas:

- ¿En qué se diferencia un modelo determinístico de uno estocástico?
- ¿En qué se diferencia un modelo discreto de uno continuo?
- ¿Cómo afectan la tasa `r` y la aleatoriedad `sigma` a los resultados?

| Modelo | Ecuación | Característica |
|---|---|---|
| Determinístico | `P(t) = P0·e^(r·t)` | Sin aleatoriedad |
| Discreto | `P(t+1) = P(t) + r·P(t)` | Cambia por períodos |
| Estocástico | `P(t+1) = P(t) + r·P(t) + ε`, `ε ~ N(0, σ²)` | Incluye ruido aleatorio |
| Continuo (Euler) | `P(t+dt) = P(t) + dt·r·P(t)` | Aproxima `dP/dt = r·P` con pasos pequeños |

Los parámetros salen del arreglo de entrada: `P0` es el primer dato, `tiempo` es el número de
períodos (6) y `r` es el promedio de la tasa de crecimiento entre períodos consecutivos (≈ 0.1318).

## 2. Tecnologías utilizadas

- Python 3
- NumPy (cálculo y números aleatorios)
- Matplotlib (gráficas)
- Arquitectura Modelo-Vista-Controlador y patrón Strategy (los cuatro modelos comparten el
  método `simular`)

## 3. Instalación

En Ubuntu:

```bash
sudo apt update
sudo apt install python3 python3-venv python3-pip    # solo la primera vez
cd simulacion_poblacion
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 4. Uso

```bash
python3 main.py
```

Se imprimen en la terminal los parámetros y la población final de cada modelo, y luego se
abren tres gráficas (cerrar cada ventana para ver la siguiente). También se guardan en
`graficas/`.

## 5. Configuración

Los parámetros se cambian en dos lugares:

- `modelo/parametros.py`: `DATOS` (arreglo de entrada) y los valores por defecto de `sigma`
  (ruido), `dt` (paso de Euler) y `semilla` (para repetir los mismos números aleatorios).
- `controlador/controlador.py`: `VALORES_R` y `VALORES_SIGMA`, que son los valores que se
  prueban en las gráficas de influencia.

Si se cambia `DATOS`, `P0`, `tiempo` y `r` se recalculan solos.

## 6. Estructura del proyecto

```
simulacion_poblacion/
├── main.py                    # punto de entrada
├── requirements.txt           # librerías necesarias
├── .gitignore
├── modelo/
│   ├── parametros.py          # datos de entrada y cálculo de P0, r, tiempo
│   └── modelos.py             # los cuatro modelos
├── vista/
│   ├── vista_consola.py       # parámetros y tabla de resultados por consola
│   └── vista_grafica.py       # las tres gráficas
├── controlador/
│   └── controlador.py         # ejecuta los modelos y llama a las vistas
└── graficas/                  # imágenes generadas al ejecutar
```

## 7. Información adicional

### Funcionalidades

- Los cuatro modelos con los mismos parámetros y una gráfica comparativa.
- Gráfica de la influencia de `r` (incluye una tasa negativa para ver el decrecimiento).
- Gráfica del efecto de `sigma` en el modelo estocástico.

### Resultados

Población final (período 6) con `r ≈ 0.1318`, `sigma = 50`, `dt = 0.1`. El dato real es 2100.

| Modelo | P final | Diferencia con el dato real |
|---|---:|---:|
| Determinístico | 2204.7 | +104.7 |
| Discreto | 2101.6 | +1.6 |
| Estocástico | 1983.7 | -116.3 |
| Continuo (Euler) | 2193.4 | +93.4 |

![Comparación](graficas/comparacion_modelos.png)
![Influencia de r](graficas/influencia_r.png)
![Efecto de sigma](graficas/efecto_sigma.png)


### Bibliografía

Diapositivas semana 2.

### Uso de IA

**Prompt que usamos:**

> Estoy haciendo la siguiente práctica (adjunto la guía y una imagen con la estructura
> de un README). Necesito resolverla solo en Python, con arquitectura Modelo-Vista-Controlador
> y un patrón de diseño simple, siguiendo el pseudocódigo de la guía y sin complicar el
> código. Elabora el README según la imagen, el .gitignore y el requirements.txt, y explícame
> el proyecto para poder defenderlo y realizarlo por mi cuenta.

**Dónde se usó IA:**

- Pautas para entender la práctica y los cuatro modelos.
- Estructura de carpetas (modelo, vista, controlador) y elección del patrón Strategy.
- Código de `vista_grafica.py` y correcciones de código generales a partir del pseudocódigo de la guía.
- Redacción del README (formato y estructura), `.gitignore` y `requirements.txt`.
