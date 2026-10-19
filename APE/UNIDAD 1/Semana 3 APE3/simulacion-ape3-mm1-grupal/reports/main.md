::: center
**Reporte Técnico de Actividades\
Práctico-Experimentales Nro. 003**
:::

# Datos de Identificación del Estudiante y la Práctica

::: tabularx
\|L0.43\|Y\| **Nombre del estudiante(s)** & Cael Alejandro Soto
Castillo\
**Asignatura** & Simulación\
**Ciclo** & 5 A\
**Unidad** & 1\
**Resultado de aprendizaje de la unidad** & R1. Aplica análisis
estadísticos de los datos de la Simulación para mejorar la calidad de
los resultados, bajo los principios de solidaridad, transparencia,
responsabilidad y honestidad.\
**Práctica Nro.** & 003\
**Título de la Práctica** & Simulación de un sistema de líneas de espera
M/M/1 mediante SimPy\
**Nombre del Docente** & José O. Guamán Q.\
**Fecha** & 15 de Octubre de 2026\
& 16 de Octubre 2026\
**Horario** & Jueves 10h30 a 11h30\
& Viernes 07h30 a 09h30\
**Lugar** & Aula\
**Tiempo planificado en el Sílabo** & 3 horas\
:::

# Objetivo(s) de la Práctica

Simular un sistema de líneas de espera M/M/1 utilizando Python y SimPy,
analizando el comportamiento de los clientes, la cola y el servidor.

1.  Implementar un modelo M/M/1 utilizando la biblioteca SimPy.

2.  Calcular las principales métricas teóricas del sistema de espera.

3.  Comparar los resultados teóricos con los obtenidos mediante la
    simulación.

# Materiales y reactivos

- Python 3.x (se ejecutó con Python 3.14.8).

- Biblioteca SimPy (se ejecutó con SimPy 4.1.2).

- NumPy (2.5.4).

- Matplotlib (3.11.2).

- Editor de código: Visual Studio Code, PyCharm o Jupyter Notebook.

# Equipos y herramientas

- Computador.

- Procesador de 2 núcleos o superior.

- Mínimo 4 GB de RAM.

- Sistema operativo Linux o macOS.

# Link Repositorio

<https://github.com/C-ael/Simulacion_Portafolio>

# Procedimiento / Metodología Ejecutada

## Fundamento teórico

El modelo **M/M/1** representa un sistema de líneas de espera con
llegadas de clientes siguiendo una distribución de Poisson, tiempos de
servicio con distribución exponencial, un único servidor y atención de
clientes bajo el principio FIFO (*primero en llegar, primero en ser
atendido*).

El modelo utiliza dos parámetros principales:

- $\lambda$: tasa promedio de llegada de clientes.

- $\mu$: tasa promedio de servicio del servidor.

La utilización del servidor se calcula mediante:
$$\rho = \frac{\lambda}{\mu}$$

**Observación sobre la guía.** La guía de la práctica imprime
$\rho = \mu/\lambda$, lo que contradice su propia condición de
estabilidad $\lambda < \mu$ enunciada unas líneas más abajo y también su
pseudocódigo, que usa $\rho = \lambda/\mu$. Con la fórmula impresa, los
tres escenarios de la guía darían $\rho = 1{,}50$, $1{,}20$ y $1{,}03$,
es decir un servidor saturado en los tres casos, y las medidas $L$,
$L_q$, $W$ y $W_q$ no existirían, porque solo están definidas para
$\rho < 1$. Este trabajo usa la definición correcta
$\rho = \lambda/\mu$, que es la que emplea el pseudocódigo de la propia
guía y la que aparece en la bibliografía de teoría de colas.

Para que el sistema sea estable debe cumplirse: $$\lambda < \mu$$

Las principales medidas teóricas del sistema son:

$$L = \frac{\lambda}{\mu-\lambda} \qquad
L_q = \frac{\lambda^2}{\mu(\mu-\lambda)}$$

$$W = \frac{1}{\mu-\lambda} \qquad
W_q = \frac{\lambda}{\mu(\mu-\lambda)}$$

  **[Símbolo]{style="color: white"}**   **[Significado]{style="color: white"}**
  ------------------------------------- -------------------------------------------
  $\lambda$                             Tasa de llegada de clientes
  $\mu$                                 Tasa de servicio
  $\rho$                                Utilización del servidor
  $L$                                   Número promedio de clientes en el sistema
  $L_q$                                 Número promedio de clientes en la cola
  $W$                                   Tiempo promedio en el sistema
  $W_q$                                 Tiempo promedio de espera en la cola

  : Notación empleada.

## Escenarios ejecutados

Se ejecutaron los tres escenarios indicados por la guía, todos con
$\mu = 3{,}0$:

   **[Escenario]{style="color: white"}**   **[$\lambda$]{style="color: white"}**   **[$\mu$]{style="color: white"}**  **[Condición]{style="color: white"}**
  --------------------------------------- --------------------------------------- ----------------------------------- ---------------------------------------
                     1                                      2,0                                   3,0                 Sistema estable
                     2                                      2,5                                   3,0                 Mayor utilización
                     3                                      2,9                                   3,0                 Cerca de saturación

  : Escenarios de la guía. La utilización teórica resulta
  $\rho = 0{,}667$, $0{,}833$ y $0{,}967$ respectivamente.

## Arquitectura e implementación

El programa se desarrolló en Python siguiendo el pseudocódigo de la guía
y se estructuró en tres capas (modelo, vista y controlador) para que
cada medida tuviera un único responsable en el código. Los componentes
son:

- **Escenarios** (): cada escenario es un objeto con su $\lambda$, su
  $\mu$ y su condición. Para cambiar un escenario se editan sus números
  y para agregar uno nuevo se añade a la lista `ESCENARIOS`.

- **Métricas teóricas** (): calcula $\rho$, $L$, $L_q$, $W$ y $W_q$ con
  las fórmulas del apartado anterior y expone `es_estable()` para
  verificar $\lambda < \mu$. Sus valores son los que se comparan con los
  de la simulación.

- **Motor de simulación** (): crea un entorno SimPy con un servidor de
  `capacity = 1` y genera los clientes con tiempos entre llegadas
  exponenciales de tasa $\lambda$ (`expovariate`). Cada cliente pide el
  servidor, espera su turno en orden FIFO y es atendido con un tiempo
  exponencial de tasa $\mu$. Por cada cliente se registra el tiempo de
  espera en cola, y aparte se guarda una traza del tamaño de la cola a
  lo largo del tiempo.

- **Tablas** (): imprime en la terminal la tabla de valores teóricos y
  la tabla de teoría contra simulación. No calcula nada.

- **Gráficas** (): genera las tres figuras del informe y las guarda en
  `graficas/`.

- **Controlador** (): recorre los escenarios, simula cada uno varias
  veces, promedia las réplicas y une el modelo con la vista. Si un
  escenario no cumple $\lambda < \mu$, avisa que el sistema no es
  estable, no lo simula y continúa con el siguiente.

- **Punto de entrada** (): un solo comando ejecuta todo el estudio:

<!-- -->

    python3 main.py

**Medición de las métricas simuladas.** Dos detalles de implementación
importan para que los números sean comparables con la teoría:

- La **espera promedio** se calcula como el promedio simple de los
  tiempos de espera de todos los clientes atendidos en la corrida.
  Mientras más clientes se atienden, más se acerca a $W_q$, aunque al
  empezar con el sistema vacío tiende a quedar un poco por debajo.

- El **tamaño promedio de la cola** no se calcula como el promedio
  simple de los tamaños registrados, porque cada tamaño dura un tiempo
  distinto y eso distorsionaría el resultado. Se calcula como el
  *promedio ponderado por tiempo*: cada tamaño de cola se multiplica por
  el tiempo que permaneció en ese valor y al final se divide entre el
  tiempo total simulado. Así se obtiene $L_q$ de forma comparable con la
  teoría.

**Sistemas no estables.** Si en algún escenario $\lambda \geq \mu$ el
programa no simula: informa que el sistema no es estable y sigue con los
demás. Esto respeta el pseudocódigo de la guía y evita reportar
promedios de una cola que crece sin límite.

## Parámetros de la corrida oficial y reproducibilidad

La corrida que alimenta este informe se ejecutó con la configuración
definida en el controlador, en el archivo :

  **[Variable]{style="color: white"}**    **[Valor]{style="color: white"}**  **[Qué controla]{style="color: white"}**
  -------------------------------------- ----------------------------------- -------------------------------------------------
  `TIEMPO_SIMULACION`                                   5000                 Duración de cada corrida, en unidades de tiempo
  `REPETICIONES`                                         10                  Réplicas independientes por escenario
  `SEMILLA`                                              42                  Semilla base; la réplica $i$ usa `SEMILLA + i`

  : Parámetros de la corrida oficial.

En total se ejecutaron **30 simulaciones**: 3 escenarios $\times$ 10
réplicas. La corrida es **reproducible**: como cada réplica recibe una
semilla derivada de forma determinista de la semilla base, repetir
`python3 main.py` produce exactamente los mismos números. En cada
corrida se atendieron del orden de $10\,000$ clientes en el escenario 1,
$12\,500$ en el escenario 2 y $14\,400$ en el escenario 3.

**Justificación del número de réplicas.** Una sola corrida no es
evidencia suficiente cuando el sistema está cerca de la saturación: con
$\rho = 0{,}967$ la cola tarda mucho en vaciarse después de una racha de
llegadas, así que las esperas de clientes seguidos están muy
relacionadas entre sí y una corrida aporta menos información de la que
parece. Por eso cada escenario se repite 10 veces con semillas distintas
y se reporta el promedio de las réplicas junto con su intervalo de
confianza, que es lo que permite afirmar si la teoría queda o no dentro
del rango de lo simulado.

# Resultados esperados

- Un sistema M/M/1 funcional mediante SimPy.

- Simulación de llegada de clientes y atención por un único servidor.

- Tiempo promedio de espera de los clientes.

- Tamaño promedio de la cola.

- Utilización teórica del servidor.

- Valores teóricos de $L$, $L_q$, $W$ y $W_q$.

- Gráficas del comportamiento de la cola y los tiempos de espera.

- Comparación entre resultados teóricos y simulados.

- Análisis del comportamiento del sistema para los tres escenarios
  propuestos.

La guía anticipa que *se espera observar que, cuando $\lambda$ se
aproxima a $\mu$, aumentan el tiempo de espera y el tamaño de la cola,
debido a que el servidor trabaja cerca de su capacidad máxima*. Los
resultados de la sección siguiente registran esas medidas; su
interpretación va en el análisis de resultados.

# Resultados

## Comparación entre resultados teóricos y simulados

La Tabla [1](#tab:comparacion){reference-type="ref"
reference="tab:comparacion"} presenta, para cada escenario, los valores
teóricos obtenidos con las fórmulas del modelo y los valores simulados
obtenidos como promedio de las 10 réplicas.

::: {#tab:comparacion}
  -------------------------------------- --------------------------------------- ------------------------------------ --------------------------------- ----------------------------------- --------------------------------- ----------------------------------- ------------ -------------
     **[Esc.]{style="color: white"}**     **[$\lambda$]{style="color: white"}**   **[$\rho$]{style="color: white"}**   **[$L$]{style="color: white"}**   **[$L_q$]{style="color: white"}**   **[$W$]{style="color: white"}**   **[$W_q$]{style="color: white"}**               
   **[simulada]{style="color: white"}**                                                                                                                                                                                                                                        
   **[simulada]{style="color: white"}**                                                                                                                                                                                                                                        
                    1                                      2,0                                  0,6667                             2,0000                             1,3333                             1,0000                             0,6667                 **0,6691**   **1,3350**
                    2                                      2,5                                  0,8333                             5,0000                             4,1667                             2,0000                             1,6667                 **1,8141**   **4,5500**
                    3                                      2,9                                  0,9667                             29,0000                            28,0333                            10,0000                            9,6667                 **8,5730**   **24,8003**
  -------------------------------------- --------------------------------------- ------------------------------------ --------------------------------- ----------------------------------- --------------------------------- ----------------------------------- ------------ -------------

  : Comparación de resultados teóricos y simulados por escenario. Las
  columnas $\rho$, $L$, $L_q$, $W$ y $W_q$ son teóricas; las dos últimas
  son los promedios simulados de 10 réplicas.
:::

Los mismos valores son los que imprime el programa en la terminal al
ejecutar `python3 main.py`:

`===``\ `{=latex}`Valores``\ `{=latex}`teóricos``\ `{=latex}`===`\
`Escenario``\ `{=latex}$\lambda$`\ `{=latex}$\mu$`\ `{=latex}$\rho$`\ `{=latex}`L``\ `{=latex}`Lq``\ `{=latex}`W``\ `{=latex}`Wq`\
`Escenario``\ `{=latex}`1``\ `{=latex}`2.0``\ `{=latex}`3.0``\ `{=latex}`0.667``\ `{=latex}`2.000``\ `{=latex}`1.333``\ `{=latex}`1.000``\ `{=latex}`0.667`\
`Escenario``\ `{=latex}`2``\ `{=latex}`2.5``\ `{=latex}`3.0``\ `{=latex}`0.833``\ `{=latex}`5.000``\ `{=latex}`4.167``\ `{=latex}`2.000``\ `{=latex}`1.667`\
`Escenario``\ `{=latex}`3``\ `{=latex}`2.9``\ `{=latex}`3.0``\ `{=latex}`0.967``\ `{=latex}`29.000``\ `{=latex}`28.033``\ `{=latex}`10.000``\ `{=latex}`9.667`

`===``\ `{=latex}`Teoría``\ `{=latex}`vs``\ `{=latex}`simulación``\ `{=latex}`===`\
`Escenario``\ `{=latex}`Wq``\ `{=latex}`teórico``\ `{=latex}`Wq``\ `{=latex}`simulado``\ `{=latex}`Dif`\
`Escenario``\ `{=latex}`1``\ `{=latex}`0.667``\ `{=latex}`0.669``\ `{=latex}`0.4``\ `{=latex}`1.333``\ `{=latex}`1.335``\ `{=latex}`0.1`\
`Escenario``\ `{=latex}`2``\ `{=latex}`1.667``\ `{=latex}`1.814``\ `{=latex}`8.8``\ `{=latex}`4.167``\ `{=latex}`4.550``\ `{=latex}`9.2`\
`Escenario``\ `{=latex}`3``\ `{=latex}`9.667``\ `{=latex}`8.573``\ `{=latex}`-11.3``\ `{=latex}`28.033``\ `{=latex}`24.800``\ `{=latex}`-11.5`

## Intervalo de confianza y error relativo

La Tabla [2](#tab:intervalos){reference-type="ref"
reference="tab:intervalos"} reporta, para las dos medidas que produce la
simulación ($W_q$ y $L_q$), la media de las 10 réplicas, su desviación
estándar, el intervalo de confianza al 95 % y el error relativo frente
al valor teórico. El intervalo se calculó con la distribución $t$ de
Student sobre las 10 medias por réplica, que es la cantidad que se
compara contra la teoría y no la dispersión de los clientes
individuales.

::: {#tab:intervalos}
  ----------------------------------------- ------------------------------------ --------- -------- --------------------------- --------- ---- --------------
      **[Esc.]{style="color: white"}**       **[Medida]{style="color: white"}**                                                                
    **[simulada]{style="color: white"}**                                                                                                       
      **[est.]{style="color: white"}**                                                                                                         
     **[teórico]{style="color: white"}**                                                                                                       
   **[al teórico?]{style="color: white"}**                                                                                                     
      **[rel.]{style="color: white"}**                                                                                                         
                      1                                    $W_q$                  0,6691    0,0576    $[0{,}6279;\ 0{,}7104]$    0,6667    Sí   $+0{,}37$ %
                      1                                    $L_q$                  1,3350    0,1243    $[1{,}2461;\ 1{,}4240]$    1,3333    Sí   $+0{,}13$ %
                      2                                    $W_q$                  1,8141    0,3807    $[1{,}5418;\ 2{,}0864]$    1,6667    Sí   $+8{,}85$ %
                      2                                    $L_q$                  4,5500    0,9876    $[3{,}8436;\ 5{,}2565]$    4,1667    Sí   $+9{,}20$ %
                      3                                    $W_q$                  8,5730    1,6844    $[7{,}3682;\ 9{,}7779]$    9,6667    Sí   $-11{,}31$ %
                      3                                    $L_q$                  24,8003   5,0023   $[21{,}2221;\ 28{,}3785]$   28,0333   Sí   $-11{,}53$ %
  ----------------------------------------- ------------------------------------ --------- -------- --------------------------- --------- ---- --------------

  : Media simulada de 10 réplicas, desviación estándar, intervalo de
  confianza al 95 % y error relativo de $W_q$ y $L_q$ frente a la
  teoría. Se marca en cada fila si el valor teórico cae dentro del
  intervalo simulado.
:::

## Gráficas

La Figura [1](#fig:cola){reference-type="ref" reference="fig:cola"}
muestra la evolución del número de clientes en la cola durante las
primeras 200 unidades de tiempo de la primera réplica de cada escenario,
junto con la línea del valor teórico $L_q$.

<figure id="fig:cola" data-latex-placement="H">
<span class="image placeholder"
data-original-image-src="figures/cola_en_el_tiempo.png"
data-original-image-title="" width="\textwidth" height="53%"></span>
<figcaption>Clientes en la cola a lo largo del tiempo, un panel por
escenario, con la línea roja del valor teórico <span
class="math inline"><em>L</em><sub><em>q</em></sub></span>. En el
escenario 1 la cola llega como máximo a 12 clientes, en el 2 a 24 y en
el 3 a 20; en el escenario 3 queda lejos del valor teórico porque solo
se muestran las primeras 200 unidades de tiempo.</figcaption>
</figure>

La Figura [2](#fig:esperas){reference-type="ref"
reference="fig:esperas"} muestra el tiempo que esperó cada uno de los
primeros 300 clientes, con la línea del valor teórico $W_q$.

<figure id="fig:esperas" data-latex-placement="H">
<span class="image placeholder"
data-original-image-src="figures/tiempos_de_espera.png"
data-original-image-title="" width="\textwidth" height="46%"></span>
<figcaption>Tiempo de espera de cada cliente (primeros 300), un panel
por escenario, con la línea roja del valor teórico <span
class="math inline"><em>W</em><sub><em>q</em></sub></span>. En el
escenario 1 las esperas son pequeñas; en el escenario 2 hay tramos
largos por encima del valor teórico; y en el escenario 3 la serie queda
por debajo porque corresponde al inicio de la simulación.</figcaption>
</figure>

La Figura [3](#fig:comparacion){reference-type="ref"
reference="fig:comparacion"} compara, con barras, el valor teórico y el
valor simulado de $W_q$ y de $L_q$ en los tres escenarios.

<figure id="fig:comparacion" data-latex-placement="H">
<span class="image placeholder"
data-original-image-src="figures/teoria_vs_simulacion.png"
data-original-image-title="" width="\textwidth" height="22%"></span>
<figcaption>Comparación teoría – simulación por escenario para <span
class="math inline"><em>W</em><sub><em>q</em></sub></span> (izquierda) y
<span class="math inline"><em>L</em><sub><em>q</em></sub></span>
(derecha). Las barras azules son los valores teóricos y las naranjas el
promedio de las 10 réplicas simuladas.</figcaption>
</figure>

# Análisis de Resultados

En los tres escenarios el servidor trabaja siempre a $\mu = 3{,}0$ y lo
único que cambia es cuántos clientes llegan: $\lambda$ sube de 2,0 a
2,9. En la Tabla [1](#tab:comparacion){reference-type="ref"
reference="tab:comparacion"} vemos que la espera en cola $W_q$ pasa de
0,67 a 1,67 y luego a 9,67, y que la cola $L_q$ pasa de 1,33 a 4,17 y
luego a 28,03. Es decir, con solo un 45 % más de llegadas, la espera se
multiplica por 14,5 y la cola por 21.

::: {#tab:comparacion1}
  -------------------------------------- --------------------------------------- ------------------------------------ --------------------------------- ----------------------------------- --------------------------------- ----------------------------------- ------------ -------------
     **[Esc.]{style="color: white"}**     **[$\lambda$]{style="color: white"}**   **[$\rho$]{style="color: white"}**   **[$L$]{style="color: white"}**   **[$L_q$]{style="color: white"}**   **[$W$]{style="color: white"}**   **[$W_q$]{style="color: white"}**               
   **[simulada]{style="color: white"}**                                                                                                                                                                                                                                        
   **[simulada]{style="color: white"}**                                                                                                                                                                                                                                        
                    1                                      2,0                                  0,6667                             2,0000                             1,3333                             1,0000                             0,6667                 **0,6691**   **1,3350**
                    2                                      2,5                                  0,8333                             5,0000                             4,1667                             2,0000                             1,6667                 **1,8141**   **4,5500**
                    3                                      2,9                                  0,9667                             29,0000                            28,0333                            10,0000                            9,6667                 **8,5730**   **24,8003**
  -------------------------------------- --------------------------------------- ------------------------------------ --------------------------------- ----------------------------------- --------------------------------- ----------------------------------- ------------ -------------
:::

[]{#tab:comparacion1 label="tab:comparacion1"}

La razón está en las fórmulas, donde la resta $\mu-\lambda$ aparece
dividiendo. Por ejemplo, con $W = \frac{1}{\mu-\lambda}$:

- Escenario 1: $\mu-\lambda = 1{,}0$, entonces $W = 1$.

- Escenario 2: $\mu-\lambda = 0{,}5$, entonces $W = 2$.

- Escenario 3: $\mu-\lambda = 0{,}1$, entonces $W = 10$.

Yo interpreto esa resta como el "margen libre" del servidor. Mientras es
grande, el servidor se recupera rápido de cualquier racha de llegadas
seguidas. Cuando es muy pequeña, casi no tiene descanso y cada
acumulación de clientes tarda mucho en desaparecer. Por eso el
crecimiento no es proporcional: el último tramo (de 2,5 a 2,9) pesa
mucho más que los anteriores, aunque el aumento de $\lambda$ sea
parecido.

## Lo que se ve en las gráficas

<figure id="fig:cola1" data-latex-placement="H">
<p><span class="image placeholder"
data-original-image-src="figures/cola_en_el_tiempo.png"
data-original-image-title="" width="\textwidth"
height="43%">image</span> <span id="fig:cola1"
data-label="fig:cola1"></span></p>
</figure>

**Cola en el tiempo (Figura [1](#fig:cola){reference-type="ref"
reference="fig:cola"}).** En el escenario 1 la línea vuelve a cero muy
seguido: en las 200 unidades mostradas, la cola está vacía un poco más
de la mitad del tiempo (54 %). Casi siempre hay entre 0 y 4 clientes, y
el único momento fuera de lo normal es un pico máximo de 12 cerca del
tiempo 137. En el escenario 2 el panorama cambia: la cola se vacía mucho
menos (solo el 12 % del tiempo) y sube y baja en oleadas largas que
llegan a cerca de 24 clientes. En el escenario 3 la cola llega a unos 20
clientes, pero en estas 200 unidades nunca alcanza la línea roja (28) y
en promedio es incluso más corta que en el escenario 2 (unos 4 clientes
contra unos 8). Eso va en contra de lo que dice la teoría; una
explicación posible es que la simulación recién está empezando (se
explica más abajo).

<figure id="fig:esperas1" data-latex-placement="H">
<p><span class="image placeholder"
data-original-image-src="figures/tiempos_de_espera.png"
data-original-image-title="" width="\textwidth"
height="40%">image</span> <span id="fig:esperas1"
data-label="fig:esperas1"></span></p>
</figure>

**Espera de cada cliente (Figura [2](#fig:esperas){reference-type="ref"
reference="fig:esperas"}).** En el escenario 1 la mayoría de los
clientes espera poco, casi siempre menos de 2 unidades. Hay un grupo de
clientes seguidos, cerca del número 280, pero después todo se normaliza.
En el escenario 2 las esperas son más altas y duran más, pues entre los
clientes 100 y 130 llegan a unas 8 unidades. Un detalle que me llamó la
atención es que las esperas bajan poco a poco, porque si un cliente
espera mucho, el siguiente también (ambos están en la misma fila) y la
fila solo se va vaciando de a poco. Las subidas pueden ser más rápidas,
por ejemplo cuando un cliente tarda mucho en ser atendido, como se ve
cerca del cliente 260. En el escenario 3, en cambio, casi todos los
primeros 300 clientes esperan menos de 5 unidades, muy por debajo de la
línea roja. Esto es coherente con que la corrida empieza vacía y la fila
todavía está creciendo hacia su tamaño normal.

<figure id="fig:comparacion1" data-latex-placement="H">
<p><span class="image placeholder"
data-original-image-src="figures/teoria_vs_simulacion.png"
data-original-image-title="" width="\textwidth"
height="22%">image</span> <span id="fig:comparacion1"
data-label="fig:comparacion1"></span></p>
</figure>

**Teoría vs simulación
(Figura [3](#fig:comparacion){reference-type="ref"
reference="fig:comparacion"}).** En el escenario 1 las barras azul
(teórica) y naranja (simulada) son casi idénticas. En el escenario 2 la
naranja queda un poco más alta y en el escenario 3 queda más baja que la
azul.

## ¿Por qué no coinciden exactamente?

::: {#tab:intervalos1}
  ----------------------------------------- ------------------------------------ --------- -------- --------------------------- --------- ---- --------------
      **[Esc.]{style="color: white"}**       **[Medida]{style="color: white"}**                                                                
    **[simulada]{style="color: white"}**                                                                                                       
      **[est.]{style="color: white"}**                                                                                                         
     **[teórico]{style="color: white"}**                                                                                                       
   **[al teórico?]{style="color: white"}**                                                                                                     
      **[rel.]{style="color: white"}**                                                                                                         
                      1                                    $W_q$                  0,6691    0,0576    $[0{,}6279;\ 0{,}7104]$    0,6667    Sí   $+0{,}37$ %
                      1                                    $L_q$                  1,3350    0,1243    $[1{,}2461;\ 1{,}4240]$    1,3333    Sí   $+0{,}13$ %
                      2                                    $W_q$                  1,8141    0,3807    $[1{,}5418;\ 2{,}0864]$    1,6667    Sí   $+8{,}85$ %
                      2                                    $L_q$                  4,5500    0,9876    $[3{,}8436;\ 5{,}2565]$    4,1667    Sí   $+9{,}20$ %
                      3                                    $W_q$                  8,5730    1,6844    $[7{,}3682;\ 9{,}7779]$    9,6667    Sí   $-11{,}31$ %
                      3                                    $L_q$                  24,8003   5,0023   $[21{,}2221;\ 28{,}3785]$   28,0333   Sí   $-11{,}53$ %
  ----------------------------------------- ------------------------------------ --------- -------- --------------------------- --------- ---- --------------
:::

[]{#tab:intervalos1 label="tab:intervalos1"}

En la Tabla [2](#tab:intervalos){reference-type="ref"
reference="tab:intervalos"} se ve que la diferencia en $W_q$ es mínima
en el escenario 1 ($+0{,}37$ %), de cerca de $+9$ % en el escenario 2 y
de cerca de $-11$ % en el escenario 3. Veo dos explicaciones posibles:

- **El azar:** Cada réplica usa números aleatorios distintos, así que
  ninguna da exactamente el valor teórico. Además, cuanto más cargado
  está el sistema, más cambian los resultados de una réplica a otra: la
  desviación estándar de $W_q$ sube de 0,058 a 0,381 y a 1,684 entre los
  escenarios 1, 2 y 3.

- **El inicio vacío:** La simulación arranca sin clientes, pero la
  teoría describe el sistema ya estabilizado. Al principio la cola es
  más corta de lo normal y eso baja los promedios, esto se nota sobre
  todo en el escenario 3, porque con $\rho = 0{,}967$ el sistema tarda
  mucho en llenarse. Por eso las gráficas de ese escenario quedan por
  debajo de la línea roja.

Como el escenario 2 queda por encima de la teoría y el 3 por debajo, el
azar parece tener un papel importante. Para separarlas habría que
descartar el tramo inicial de cada corrida o usar más réplicas.

## Los intervalos de confianza

En los seis casos de la Tabla [2](#tab:intervalos){reference-type="ref"
reference="tab:intervalos"}, el valor teórico cae dentro del intervalo
de confianza al 95 %. Dicho de forma simple: con lo que simulamos, **no
hay evidencia de que la simulación esté mal**, porque las diferencias
son compatibles con el azar (pero eso no significa que sea exacta). En
el escenario 3 los intervalos son anchos (por ejemplo, el de $W_q$ va de
7,37 a 9,78), así que parte de la razón por la que la teoría cabe es que
el intervalo deja mucho margen; con más réplicas se estrecharía y la
comparación sería más exigente.

## ¿Por qué hacer varias corridas?

Logré entender que el resultado cambia mucho de una corrida a otra. En
el escenario 3 la desviación de $W_q$ entre réplicas es 1,68, cerca del
20 % de la media simulada (8,57). Una sola corrida podría salir bastante
más alta o más baja que el valor real y llevarnos a una conclusión
equivocada. En el escenario 1 la desviación entre réplicas es solo
0,058, cerca del 9 % de la media, y una corrida sola ya sería bastante
confiable. Por eso hicimos 10 réplicas por escenario: el promedio de
varias corridas es mucho más seguro que una sola.

# Preguntas de Control

1.  **Qué representa el modelo M/M/1?**

    El modelo $M/M/1$ representa una fila de espera con un solo servidor
    que atiende a los clientes uno por uno [@smith2024]. Los tiempos
    entre llegadas y los tiempos de atención son aleatorios y siguen una
    distribución exponencial [@smith2024; @heather2026]. Los clientes
    forman una sola fila sin límite de espacio, se atienden en orden de
    llegada (FIFO) y salen del sistema al terminar [@smith2024].

2.  **Qué representan $\lambda$ y $\mu$?**

    $\lambda$ es la rapidez con la que llegan los clientes, osea cuántos
    llegan por unidad de tiempo [@smith2024]. $\mu$ es la rapidez con la
    que el servidor atiende, osea cuántos clientes puede atender por
    unidad de tiempo [@smith2024; @heather2026]. Juntos indican qué tan
    ocupado estará el sistema [@smith2024].

3.  **Por qué debe cumplirse $\lambda < \mu$ para que el sistema sea
    estable?**

    Porque el servidor debe atender clientes más rápido de lo que llegan
    [@smith2024]. Si es así, la fila no crece sin parar y el sistema se
    mantiene en equilibrio [@smith2024]. En ese caso la utilización es
    menor a uno ($\rho < 1$), es decir, el servidor tiene tiempo libre
    [@smith2024].

4.  **Qué significa la utilización $\rho$?**

    La utilización $\rho$ representa la proporción del tiempo en que el
    servidor está ocupado atendiendo entidades
    [@smith2024; @heather2026]. Para un servidor único se calcula como
    $\rho = \lambda/\mu$ [@smith2024]. Un valor alto de $\rho$ indica
    mayor carga sobre el recurso y mayor congestión del sistema
    [@smith2024].

5.  **Cuál es la diferencia entre $W$ y $W_q$?**

    $W_q$ es el tiempo promedio que una entidad pasa únicamente
    esperando en la cola antes de ser atendida
    [@smith2024; @heather2026]. $W$ es el tiempo promedio total en el
    sistema, que incluye la espera en cola y el tiempo de servicio
    [@smith2024; @heather2026].

6.  **Cuál es la diferencia entre $L$ y $L_q$?**

    $L_q$ es el número promedio, ponderado en el tiempo, de entidades
    que esperan en la cola [@smith2024; @heather2026]. $L$ es el número
    promedio total de entidades en el sistema, es decir, las que esperan
    más las que reciben servicio [@smith2024; @heather2026].

7.  **Por qué SimPy utiliza una distribución exponencial para generar
    los tiempos?**

    En los modelos de colas simulados con SimPy se usa la distribución
    exponencial por su propiedad de "falta de memoria" (*memoryless
    property*) [@baxter2024; @smith2024]. Esta propiedad simplifica la
    modelación de llegadas de Poisson y de tiempos de servicio
    independientes [@heather2026; @smith2024]. Además, permite verificar
    la simulación comparándola con las soluciones analíticas teóricas de
    colas $M/M/s$ [@heather2026; @smith2024].

8.  **Qué sucede con la cola cuando $\lambda$ se aproxima a $\mu$?**

    Cuando $\lambda$ se aproxima a $\mu$, la utilización $\rho$ tiende a
    $1$ [@smith2024]. Esto genera un crecimiento desproporcionado de la
    congestión y de la acumulación de entidades [@smith2024]. Como
    resultado, tanto la longitud promedio de la cola ($L_q$) como el
    tiempo medio de espera ($W_q$) aumentan drásticamente, tendiendo al
    infinito [@smith2024].

9.  **Por qué los resultados simulados pueden ser diferentes de los
    resultados teóricos?**

    Porque la simulación usa números aleatorios, y por eso cada corrida
    da resultados un poco distintos [@smith2024]. Además, la simulación
    empieza con el sistema vacío, y eso afecta los primeros resultados
    mientras el sistema se estabiliza (*warm-up*)
    [@smith2024; @heather2026]. La teoría da el valor exacto a muy largo
    plazo, mientras que la simulación solo lo estima con un número
    limitado de corridas [@smith2024; @heather2026].

10. **Qué ocurriría si $\lambda$ fuera mayor que $\mu$?**

    Si $\lambda > \mu$, llegan más clientes de los que el servidor puede
    atender, y el sistema se vuelve inestable ($\rho > 1$) [@smith2024].
    Como el servidor no alcanza a atenderlos a tiempo, la fila crece sin
    parar [@smith2024]. El sistema nunca llega a un equilibrio, y las
    fórmulas de $L$, $L_q$, $W$ y $W_q$ dejan de aplicarse [@smith2024].

# Conclusiones

- Se logró implementar el sistema M/M/1 con SimPy, con llegadas de
  clientes, una cola y un único servidor, y se pudo ejecutar los tres
  escenarios con el mismo programa cambiando solo $\lambda$.

- Las métricas teóricas ($\rho$, $L$, $L_q$, $W$ y $W_q$) mostraron que
  el sistema se vuelve muy sensible cuando $\lambda$ se acerca a $\mu$:
  al pasar de $\rho = 0{,}667$ a $\rho = 0{,}967$ la espera teórica sube
  de 0,67 a 9,67 unidades de tiempo, aunque la tasa de llegadas solo
  aumentó de 2,0 a 2,9.

- La simulación confirmó lo esperado: a mayor $\lambda$, más espera y
  colas más largas. Los valores simulados quedaron cerca de los
  teóricos, y en los tres escenarios la teoría cayó dentro del intervalo
  de confianza del 95 %.

- Las diferencias que aparecen se explican por el azar y porque la
  simulación arranca con el sistema vacío, algo que pesa más en el
  escenario 3. Por eso conviene repetir la simulación varias veces y no
  confiar en una sola corrida.

# Declaración de uso de Inteligencia Artificial

En este trabajo se usaron herramientas de inteligencia artificial como
apoyo, no como sustituto del trabajo propio. Primero se muestra un
prompt representativo de la forma en que se usó la herramienta y, a
continuación, la justificación de su uso.

## Prompt utilizado

El estudiante partió siempre de contenido ya elaborado (informe, código
y resultados propios) y pidió mejorarlo, no generarlo desde cero. El
siguiente prompt resume la instrucción general empleada (es
representativo, no una transcripción literal de todas las
interacciones):

> *Te comparto mi informe de la práctica 003 (simulación de un sistema
> M/M/1 con SimPy) escrito en LaTeX para Overleaf, junto con la guía del
> docente. Ya tengo redactados el fundamento teórico, las tablas de
> resultados y las gráficas, y ya ejecuté mi programa. Necesito que me
> ayudes a **mejorar** lo que ya tengo, no a hacerlo desde cero:*
>
> *1. Redacción: revisa mi análisis de resultados y propón una versión
> con lenguaje más claro y natural, sin cambiar mis números.*
>
> *2. Formato: corrige mi código LaTeX para que las figuras y las tablas
> no se superpongan con el texto y para que las citas salgan en estilo
> IEEE usando mi archivo `referencias.bib`.*
>
> *3. Fórmulas y modelo matemático: verifica que $\rho$, $L$, $L_q$, $W$
> y $W_q$ y la condición $\lambda < \mu$ estén bien según la guía, y
> avísame si encuentras errores.*
>
> *4. Estructura del código: dime si mi organización en modelo, vista y
> controlador es adecuada y qué mejorarías.*
>
> *Reglas: no inventes datos ni referencias. Las respuestas de las
> preguntas de control salen del cuaderno de NotebookLM compartido por
> el docente; solo ayúdame a simplificar su redacción. Si algo no puedes
> verificar, dímelo.*

## Justificación del uso

**Herramientas utilizadas.**

- **Claude Sonnet 5.5** (Anthropic), mediante la aplicación web
  claude.ai.

- **NotebookLM** (Google), con el cuaderno de documentos compartido por
  el docente.

**Apoyo recibido de Claude.**

- **Redacción:** mejora de la claridad de los textos, simplificación de
  las respuestas de las preguntas de control y borrador del análisis de
  resultados a partir de las tablas y gráficas obtenidas.

- **Formato:** escritura y corrección del código LaTeX en Overleaf,
  incluida la ubicación de figuras y tablas y el estilo de las citas.

- **Indagación de fórmulas y modelo matemático:** revisión de las
  fórmulas de $\rho$, $L$, $L_q$, $W$ y $W_q$ y de la condición de
  estabilidad $\lambda < \mu$, contrastadas con la guía de la práctica.

- **Estructura del código:** orientación sobre la organización del
  programa en modelo, vista y controlador.

**Lo que no se hizo con IA.**

- La información de las **preguntas de control** se obtuvo del cuaderno
  de NotebookLM compartido por el docente, a partir de sus documentos
  cargados. Claude solo ayudó a reformular esas respuestas con un
  lenguaje más sencillo y a pasarlas a LaTeX.

- El archivo de referencias (`referencias.bib`) se generó a partir de
  ese mismo cuaderno.

- Los resultados numéricos, las tablas y las gráficas provienen de la
  ejecución del programa por parte del estudiante.

**Alcance y verificación.** La inteligencia artificial **no se usó para
elaborar el informe completo**. El estudiante revisó los textos,
comprobó que los valores y comentarios coincidieran con sus propios
resultados y es responsable del contenido final. Dado que las
herramientas de IA pueden cometer errores, las respuestas y las
referencias se contrastaron con la guía de la práctica y con las fuentes
del cuaderno del docente.

# Bibliografía
