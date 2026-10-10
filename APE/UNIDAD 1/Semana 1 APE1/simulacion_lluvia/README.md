# Práctica 01 - Construcción y simulación computacional de un modelo matemático

**Asignatura:** Simulación - Ciclo 5 - Carrera de Computación, UNL

**Docente:** José O. Guamán Q.

**Estudiante:** Cael Alejandro Soto Castillo.

Simulación de la atmósfera durante 24 horas para determinar en qué horas el modelo
considera que hay posibilidad de lluvia, usando la formula:

```
I = 0.5*H + 0.3*N + 0.2*Tf
```

- `H`: humedad normalizada (humedad % / 100)
- `N`: nubosidad normalizada (nubosidad % / 100)
- `Tf`: factor de temperatura (1.00 si T <= 10 °C, baja 0.05 por cada °C, 0.10 si T >= 28 °C)

| Índice I            | Estado           |
|---------------------|------------------|
| I < 0.40            | Sin lluvia       |
| 0.40 <= I < 0.60    | Baja posibilidad |
| 0.60 <= I < 0.75    | Lluvia probable  |
| I >= 0.75           | Lluvia           |

## Estructura (Modelo - Vista - Controlador)

```
simulacion_lluvia/
├── main.py                      # punto de entrada
├── tablas/                      # imagenes de las tablas pedidas por la ficha (capturas colocadas manualmente, pues son de la terminal)
├── requirements.txt             # librerías necesarias
├── modelo/
│   ├── datos.py                 # datos de la tabla (hora, humedad, nubosidad, temp.)
│   └── modelo_lluvia.py         # fórmula, factor de temperatura y estados
├── vista/
│   ├── vista_tabla.py           # imprime la tabla en consola
│   └── vista_grafica.py         # gráficas con matplotlib
├── controlador/
│   └── controlador.py           # une modelo y vistas
└── graficas/                   # imágenes generadas al ejecutar
```

## Cómo ejecutar (Ubuntu / terminal)

1. Instalar Python y venv (solo la primera vez):

```bash
sudo apt update
sudo apt install python3 python3-venv python3-pip
```

2. Entrar a la carpeta, crear el entorno virtual e instalar las librerías:

```bash
cd simulacion_lluvia
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. Ejecutar desde la terminal:

```bash
python3 main.py
```

Se muestran dos tablas (modelo original y ajustado) y tres gráficas. Cada gráfica se
cierra para ver la siguiente y todas quedan guardadas en la carpeta `graficas/`.
Para salir del entorno virtual: `deactivate`.

> Se usa entorno virtual porque Ubuntu recientes no dejan instalar paquetes con `pip`
> directamente en el Python del sistema.

## Ajuste del modelo

Según lo indicado, el ajuste consiste en bajar cada coeficiente en 0.1, entonces quedaría:

```
Original: I = 0.5*H + 0.3*N + 0.2*Tf
Ajustado: I = 0.4*H + 0.2*N + 0.1*Tf
```

Los umbrales de los estados no se modifican. Los parámetros están en
`controlador/controlador.py`.

| Hora  | I original | Estado original | I ajustado | Estado ajustado |
|-------|-----------:|-----------------|-----------:|-----------------|
| 06:00 | 0.605 | Lluvia probable | 0.420 | Baja posibilidad |
| 08:00 | 0.640 | Lluvia probable | 0.450 | Baja posibilidad |
| 10:00 | 0.595 | Baja posibilidad | 0.422 | Baja posibilidad |
| 12:00 | 0.470 | Baja posibilidad | 0.340 | Sin lluvia |
| 14:00 | 0.685 | Lluvia probable | 0.490 | Baja posibilidad |
| 16:00 | 0.800 | Lluvia | 0.570 | Baja posibilidad |
| 18:00 | 0.885 | Lluvia | 0.628 | Lluvia probable |
| 20:00 | 0.840 | Lluvia | 0.597 | Baja posibilidad |
| 22:00 | 0.775 | Lluvia | 0.545 | Baja posibilidad |

## Interpretación matemática del comportamiento

- En el modelo original los pesos suman 1, así que I es un promedio ponderado y queda
  entre 0 y 1. En el ajustado suman 0.7, por lo que I nunca pasa de 0.7.
- Como los umbrales siguen iguales, en el modelo ajustado nunca se alcanza "Lluvia"
  (I >= 0.75): el modelo se vuelve más conservador y casi todas las horas bajan un
  estado. Esto muestra que los pesos y los umbrales deben calibrarse juntos.
- Cada variable aporta de forma lineal: si H sube 0.1, I sube 0.05 en el original y 0.04
  en el ajustado, con N sube 0.03 y 0.02, y con Tf sube 0.02 y 0.01.
- Tf es decreciente: mientras más baja la temperatura, mayor el factor y mayor el índice.
- A lo largo del día el índice baja al mediodía (12:00), sube hasta su máximo a las 18:00
  (humedad 92% y nubosidad 95%) y luego decrece hasta las 22:00. El ajuste conserva
  esa forma pero con valores más bajos.
- La humedad es la variable que más mueve el índice, mientras que la temperatura es la que menos.

## Conclusión

Los pesos y los umbrales dependen uno del otro, el cambiar uno sin ajustar el otro vuelve el modelo demasiado optimista o demasiado conservador.

## Prompt utilizado

> Prompt: En base a la siguiente ficha, dame las pautas, recursos e instrucciones
> a seguir para yo mismo hacer la actividad (entregables y que debería hacer o consultar), ademas de que se deben cumplir los siguientes puntos: Usar patron o patrones de diseño para la practica (una pequeña arquitectura).

## Dónde se usó IA

- Explicación de la actividad, pautas, conceptos y contextualización.
- Estructura de carpetas MVC: `modelo_lluvia.py`, `vista_tabla.py`, `vista_grafica.py` y `controlador.py`.
- Redacción inicial de este README (formato para que se vea mejor visualmente y cumpla lo especificado).
- Mejora de código y construcción de código en las clases .py de las vistas para las tablas.