# Tarea 6 — Temporal-Difference Learning (Capítulo 6)

**Fuente:** Sutton & Barto, *Reinforcement Learning: An Introduction* (2da ed.), **Capítulo 6** (Temporal-Difference Learning).

> **Aclaración:** el capítulo 6 es, según los propios autores, *"the one idea central and novel to reinforcement learning"*. TD learning es una **combinación de ideas de Monte Carlo y de DP**: como MC, aprende directo de la experiencia cruda sin modelo del entorno; como DP, actualiza usando en parte *otras estimaciones propias* sin esperar el resultado final (es decir, hace **bootstrapping**). Es el método TD(0) y, a partir de él, los cuatro algoritmos de control más usados del campo. La numeración de ecuaciones reinicia en (6.1). Secciones: 6.1 *TD prediction*, 6.2 *advantages of TD prediction methods*, 6.3 *optimality of TD(0)*, 6.4 *Sarsa: on-policy TD control*, 6.5 *Q-learning: off-policy TD control*, 6.6 *Expected Sarsa*, 6.7 *maximization bias and double learning*, 6.8 *games, afterstates and other special cases* y 6.9 *summary*.

**Índice**

1. Encuadre: TD = muestreo de MC + bootstrap de DP
2. (6.1) TD Prediction
3. (6.2) Advantages of TD Prediction Methods
4. (6.3) Optimality of TD(0)
5. (6.4) Sarsa: On-policy TD Control
6. (6.5) Q-learning: Off-policy TD Control
7. (6.6) Expected Sarsa
8. (6.7) Maximization Bias and Double Learning
9. (6.8) Games, Afterstates, and Other Special Cases
10. (6.9) Summary
11. Tabla comparativa: los cuatro algoritmos de control TD
12. Cómo se conecta con los capítulos 4, 5, 7 y 12

---

## Encuadre: TD = muestreo de MC + bootstrap de DP

El capítulo 5 resolvió el problema **sin modelo** pero tuvo que pagar un precio: para aprender de una visita a un estado había que **esperar a que terminara el episodio entero**. El cap. 4 hacía lo contrario (no esperaba nada) pero **necesitaba el modelo completo** $p(s', r \mid s, a)$. TD se queda con lo mejor de los dos mundos:

| | ¿Necesita modelo? | ¿Espera al final del episodio? | ¿Usa sus propias estimaciones? |
|---|---|---|---|
| **DP** (cap. 4) | **Sí** | No | **Sí** (bootstrap) |
| **MC** (cap. 5) | No | **Sí** | No |
| **TD** (cap. 6) | No | **No (un paso)** | **Sí** (bootstrap) |

> Las dos propiedades — *¿necesita modelo?* y *¿usa bootstrap?* — son **separables** y se pueden combinar de muchas maneras. El cap. 7 (n-step) y el cap. 12 (TD(λ)) exploran las otras dos: *n*-step va del TD puro hacia MC, y TD(λ) los unifica sin costuras.

**El movimiento de TD, en una línea.** MC usa como target el retorno real $G_t$; DP usa como target el valor del estado siguiente, promediando sobre todos los sucesores posibles. TD agarra **el retorno real pero truncado a un paso**, y le pega la cola que ya se conoce:

$$
\underbrace{R_{t+1} + \gamma V(S_{t+1})}_{\text{target TD}} \quad\text{en vez de}\quad \underbrace{G_t}_{\text{target de MC}}
$$

**El esqueleto es el mismo de siempre:** GPI (cap. 4.6) — evaluar ⟶ mejorar ⟶ evaluar. Lo que cambia en el capítulo es **el método de evaluación**: se reemplaza la *expected update* de DP por una *sample update* de TD. Por eso el libro empieza, como siempre, por el problema de **predicción** (policy evaluation) y recién después pasa a **control**.

---

## (6.1) — TD Prediction

**Qué representa:** estimar $v_\pi$ a partir de la experiencia, como MC, pero actualizando **un paso después** de cada visita en lugar de al final del episodio.

**El contraste paso a paso.** La mejor forma de verlo es tomar el método *every-visit* MC con step-size constante, apto para entornos no estacionarios (o sea: la regla general (2.4) del cap. 2, con el retorno como target):

$$
V(S_t) \leftarrow V(S_t) + \alpha\,[\, G_t - V(S_t) \,] \tag{6.1}
$$

MC tiene que esperar hasta el final del episodio para saber cuánto vale $G_t$. TD alcanza con esperar **un paso**: en $t+1$ ya conoce la recompensa observada $R_{t+1}$ y la estimación $V(S_{t+1})$, así que puede hacer una actualización útil inmediatamente:

$$
V(S_t) \leftarrow V(S_t) + \alpha\,[\, R_{t+1} + \gamma V(S_{t+1}) - V(S_t) \,] \tag{6.2}
$$

Este es **TD(0)**, o *one-step TD*: caso particular de los métodos *n*-step (cap. 7) y TD($\lambda$) (cap. 12).

**Pseudocódigo (TD(0) tabular para estimar $v_\pi$):**
1. **Input:** la política $\pi$ a evaluar. **Parámetro:** step size $\alpha \in (0, 1]$.
2. Inicializar $V(s)$ para todo $s \in \mathcal{S}^+$, arbitrariamente, salvo $V(\text{terminal}) = 0$.
3. Por cada episodio: inicializar $S$. Por cada paso: elegir $A$ según $\pi$; ejecutar $A$ y observar $R, S'$; **$V(S) \leftarrow V(S) + \alpha[\,R + \gamma V(S') - V(S)\,]$**; $S \leftarrow S'$. Hasta que $S$ sea terminal.

### El TD error (6.5): la pieza que reaparece todo el capítulo

Lo que está entre corchetes en (6.2) es una especie de **error**: mide la diferencia entre el valor estimado de $S_t$ y el valor *mejor estimado* $R_{t+1} + \gamma V(S_{t+1})$. Tiene nombre propio:

$$
\delta_t \doteq R_{t+1} + \gamma V(S_{t+1}) - V(S_t) \tag{6.5}
$$

Dos precisiones que importan:
- $\delta_t$ es el error en la estimación **hecha en el tiempo $t$**. Como depende del estado siguiente y la recompensa siguiente, en realidad no está disponible hasta un paso después: es información del tiempo $t+1$.
- Si el array $V$ **no cambia** durante el episodio (que es lo que pasa en MC), el error Monte Carlo se puede escribir como una **suma de TD errors**:

$$
G_t - V(S_t) = \sum_{k=t}^{T-1} \gamma^{\,k-t} \, \delta_k \tag{6.6}
$$

> **Por qué esto importa:** es la **puente entre TD y MC**. Dice que la *"corrección"* que MC aplica de un saque es simplemente la suma de las correcciones chiquitas que TD aplicó paso a paso. Y aunque $V$ sí cambie durante el episodio (que es lo que pasa en TD(0)), si $\alpha$ es chico la igualdad sigue valiendo aproximadamente. **Ejercicio 6.1:** rehacer la derivación cuando $V$ cambia, denotando $V_t$ al array usado en el tiempo $t$, y ver qué término extra hay que sumar.

### Los tres targets, de un vistazo

El capítulo apoya todo en una comparación de tres ecuaciones. Escribimos $v_\pi(s)$ de dos maneras (ambas del cap. 3):

$$
v_\pi(s) \doteq \mathbb{E}[\, G_t \mid S_t = s \,] \tag{6.3}
$$

$$
v_\pi(s) \doteq \mathbb{E}[\, R_{t+1} + \gamma\, v_\pi(S_{t+1}) \mid S_t = s \,] \tag{6.4}
$$

- **El target de MC es (6.3)**, y es *una estimación* porque el valor esperado no se conoce: se usa un retorno muestreado en lugar del retorno esperado real.
- **El target de DP es (6.4)**, y es *una estimación* **no** por los valores esperados (el modelo los da completos y exactos), sino porque $v_\pi(S_{t+1})$ no se conoce y se reemplaza por la estimación actual $V(S_{t+1})$.
- **El target de TD es una estimación por las dos razones a la vez**: muestrea los valores esperados de (6.4) **y** usa $V$ en lugar del verdadero $v_\pi$.

> **Sample updates vs expected updates.** TD y MC hacen ***sample updates***: miran un único sucesor muestreado. DP hace ***expected updates***: promedian sobre la distribución completa de todos los sucesores posibles. En los *backup diagrams* la diferencia se ve directo: el de TD muestra **una sola flecha** desde el nodo raíz; el de DP muestra **una rama por cada sucesor posible**. Esa diferencia gráfica *es* la diferencia algorítmica de fondo.

### Ejemplo didáctico 1: volver a casa (Ejemplo 6.1)

Este es el ejemplo que mejor explica TD, así que lo vamos a hacer cuenta por cuenta. Cada día volvés del trabajo a casa y tratás de **predecir cuánto te va a tomar**. El estado es (dónde estás, qué hora es, el clima) y la **recompensa es el tiempo transcurrido en cada tramo**; no hay descuento ($\gamma = 1$), así que el retorno de un estado es el tiempo real que falta para llegar.

El día del libro: salís a las 6:00 del viernes y estimás 30 minutos. Al llegar al auto (6:05) llueve, así que reestimás 35 minutos más. Al salir de la autopista bajás la estimación, pero después quedás atascado detrás de un camión y por la calle angosta tenés que seguirlo. Entrás a tu calle a las 6:40 y llegás 3 minutos después:

| Estado | Tiempo transcurrido (min) | Tiempo estimado que falta | Tiempo total estimado |
|---|---|---|---|
| salís de la oficina, viernes 6:00 | 0 | 30 | 30 |
| llegás al auto, lloviendo | 5 | 35 | 40 |
| salís de la autopista | 20 | 15 | 35 |
| calle secundaria, detrás del camión | 30 | 10 | 40 |
| entrás a tu calle | 40 | 3 | 43 |
| **llegás a casa** | **43** | 0 | 43 |

**Las recompensas de cada tramo** son los tiempos transcurridos: $5, 15, 10, 10, 3$. Y los **retornos reales** (el tiempo que de verdad faltaba) son $43, 38, 23, 13, 3, 0$ — que es justamente la última columna menos lo transcurrido.

**(a) Qué haría MC (6.1).** MC espera a llegar a casa para poder aplicar las correcciones. Los errores $G_t - V(S_t)$ son:

| Estado | $V(S_t)$ estimado | $G_t$ real | error |
|---|---|---|---|
| salís de la oficina | 30 | 43 | **13** |
| llegás al auto | 35 | 38 | **3** |
| salís de la autopista | 15 | 23 | **8** |
| detrás del camión | 10 | 13 | **3** |
| entrás a tu calle | 3 | 3 | 0 |

Con $\alpha = \tfrac{1}{2}$, la estimación del estado "salís de la autopista" sube 8 × ½ = **4 minutos**. El libro comenta algo muy sano: ese probably es un cambio demasiado grande, porque el camión fue simplemente una mala racha. Y lo estructural: **todos estos cambios solo se pueden hacer una vez que llegaste a casa**.

**(b) Qué haría TD (6.2), y acá está la magia.** Con $\alpha = 1$ y $\gamma = 1$ la actualización se simplifica mucho: el nuevo valor del estado es *la recompensa de este tramo más lo que valía el estado siguiente*. O sea, **cada estimación se corre hacia la estimación que la sigue**:

| Estado | $V(S_t)$ | $R_{t+1}$ | $V(S_{t+1})$ | target $= R_{t+1} + V(S_{t+1})$ | $\delta_t$ | nuevo $V(S_t)$ |
|---|---|---|---|---|---|---|
| salís de la oficina | 30 | 5 | 35 | 40 | **+10** | **40** |
| llegás al auto | 35 | 15 | 15 | 30 | **−5** | **30** |
| salís de la autopista | 15 | 10 | 10 | 20 | **+5** | **20** |
| detrás del camión | 10 | 10 | 3 | 13 | **+3** | **13** |
| entrás a tu calle | 3 | 3 | 0 | 3 | 0 | 3 |

Tres cosas para mirar:

1. **Aprendés en el camino, no al llegar.** Cuando por fin entrás a tu calle, ya corregiste cuatro estimaciones. Con el atasco del día siguiente, TD te habría movido la estimación de salida de 30 hacia 50 **de inmediato**, en vez de tener que esperar el lunes siguiente.
2. **Los errores se cancelan entre sí** (fijate: +10, −5, +5, +3). Eso es exactamente (6.6) en acción: el error MC total desde el primer estado (13) es la **suma de los TD errors** del episodio:

$$
\underbrace{\delta_0 + \delta_1 + \delta_2 + \delta_3 + \delta_4}_{10 - 5 + 5 + 3 + 0} = 13 \;=\; G_0 - V(S_0) = 43 - 30 \quad\checkmark
$$

   Y el mismo chequeo desde el estado "salís de la autopista": $\delta_2 + \delta_3 + \delta_4 = 5 + 3 + 0 = 8 = 23 - 15$ — **precisamente los 8 minutos que menciona el libro**. TD no es un método distinto: es la descomposición del update de MC en pasos chiquitos encadenados.

> **Ejercicio 6.2 (la intuición que más se usa en la práctica):** imaginá que te mudás de edificio y empezás a aprender predicciones para el camino nuevo desde cero, **pero la autopista es la misma**. TD va a ser mucho mejor al principio, porque el tramo que ya conocés (el final del viaje) alimenta el target desde el primer día; MC no puede aprovechar nada hasta completar un episodio completo nuevo.

**Ejercicios:** **6.1** (la identidad (6.6) cuando $V$ cambia) y **6.2** (cuándo TD le gana a MC en promedio).

---

## (6.2) — Advantages of TD Prediction Methods

**Qué representa:** la pregunta obvia después de ver el capítulo. Si TD **aprende una estimación a partir de otra** (*bootstrapping*: aprender de una suposición), ¿eso es sensato o es inventar el valor de la nada? El capítulo adelanta la respuesta y promete el resto del libro.

**Las ventajas, en orden de obviedad:**

1. **Sobre DP:** TD **no requiere modelo** del entorno, ni de las distribuciones de recompensa ni de las probabilidades del próximo estado.
2. **Sobre MC:** TD se implementa de forma **online y totalmente incremental**. MC tiene que esperar al final del episodio; TD, un paso. Y esto "sorprendentemente a menudo" resulta una Consideración crítica, por tres razones concretas:
   - Algunas aplicaciones tienen **episodios larguísimos** → retrasar todo el aprendizaje hasta el final es demasiado lento.
   - Otras son **tareas continuas**, donde directamente **no hay episodios**.
   - Algunos métodos MC (off-policy con importance sampling, secc. 5.7) tienen que **ignorar o descontar los episodios** en los que se tomaron acciones experimentales, lo cual frena muchísimo el aprendizaje. TD es mucho menos susceptible: **aprende de cada transición** sin importar qué acciones se tomen después.

3. **¿Y es correcto?** **Sí, está probado.** Para cualquier política fija $\pi$, se ha demostrado que TD(0) converge a $v_\pi$: **en la media** con un step-size constante suficientemente chico, y **con probabilidad 1** si el step-size decrece siguiendo las condiciones usuales de aproximación estocástica (2.7). La mayoría de las pruebas son para el caso **tabular** de (6.2); algunas también cubren el caso de **aproximación lineal de funciones** (se generalizan en el cap. 9).

### Ejemplo didáctico 2: random walk (Ejemplo 6.2)

El banco de pruebas del capítulo es un **Markov reward process** (MRP): un MDP *sin acciones*. Sirve justamente porque, al no haber política, no hay que distinguir la dinámica que viene del entorno de la que viene del agente.

- Estados `A`–`E` en línea. Todos los episodios arrancan en el centro, `C`.
- En cada paso se mueve **una casilla a la izquierda o a la derecha, con igual probabilidad**.
- Los episodios terminan en los extremos. Terminar a la **derecha** da recompensa **+1**; todas las demás recompensas son **0**.
- Un episodio típico: `C`, 0, `B`, 0, `C`, 0, `D`, 0, `E`, 1.

**Los valores verdaderos, calculados.** Como la tarea no tiene descuento, el valor de cada estado es **la probabilidad de terminar a la derecha si arranco ahí**. O sea, un sistema de 5 ecuaciones:

$$
\begin{aligned}
v(A) &= 0 \\
v(B) &= 0{,}5\,v(A) + 0{,}5\,v(C) = 0{,}25 \\
v(C) &= 0{,}5\,v(B) + 0{,}5\,v(D) = 0{,}50 \\
v(D) &= 0{,}5\,v(C) + 0{,}5\,v(E) = 0{,}75 \\
v(E) &= 1
\end{aligned}
$$

Check: $v(C) = 0{,}5(0{,}25) + 0{,}5(0{,}75) = 0{,}5$ ✓ (justo el valor que el libro menciona explícitamente). Y como la dinámica es simétrica, $v(D) = 1 - v(B)$ ✓.

**El resultado experimental.** El gráfico de la izquierda muestra los valores aprendidos después de distintos números de episodios: después de 100 episodios ya están **tan cerca de los verdaderos como van a estar nunca** — con step-size constante ($\alpha = 0{,}1$) los valores fluctúan **indefinidamente** siguiendo los resultados de los episodios más recientes. El gráfico de la derecha muestra las curvas de aprendizaje de TD(0) y constant-$\alpha$ MC para varios $\alpha$: la medida es el **error RMS** entre la función de valor aprendida y la verdadera, promediado sobre los 5 estados y luego sobre 100 corridas. **TD le ganó a MC de forma consistente en esta tarea.**

> **Ejercicios:** **6.3** (en el primer episodio solo cambió $V$ de un estado: ¿qué pasó?, ¿por qué solo ese?, ¿cuánto cambió), **6.4** (¿cambia la conclusión con un rango más amplio de $\alpha$?), **6.5** (por qué el error RMS de TD *baja y después vuelve a subir* con $\alpha$ grandes), **6.6** (describir al menos dos formas distintas de calcular esos valores verdaderos).

---

## (6.3) — Optimality of TD(0)

**Qué representa:** hasta ahora hablamos de la actualización paso a paso, pero el argumento de convergencia necesita un caso limpio. Acá se mete **batch updating**, que permite obtener respuestas deterministas y comparar los dos métodos sin ruido.

**Qué es batch updating.** Cuando solo hay cantidad finita de experiencia (digamos 10 episodios o 100 pasos de tiempo), el enfoque con métodos incrementales es **repetir la experiencia una y otra vez** hasta que el método converja: se calculan los incrementos de (6.1) o (6.2) para cada paso de tiempo con estado no terminal, **pero el array $V$ se cambia una sola vez, por la suma de todos los incrementos**. Después se reprocesa toda la experiencia con el nuevo $V$, y así hasta que $V$ converge.

**El resultado clave.** Bajo batch updating, **TD(0) converge determinísticamente a una única respuesta, independiente del step-size $\alpha$**, siempre que $\alpha$ sea suficientemente chico. El constant-$\alpha$ MC también converge determinísticamente bajo las mismas condiciones... **pero a una respuesta distinta**.

**Ejemplo 6.3: random walk bajo batch.** Con el random walk del 6.2: después de cada episodio nuevo se trataron **todos los episodios vistos hasta ahí como un batch**, y se reprocesó ese batch repetidamente con $\alpha$ suficientemente chico. Resultado (fig. 6.2): **batch TD le ganó consistentemente a batch MC**, siempre midiendo el error RMS contra $v_\pi$.

> **La paradoja que hay que resolver.** MC converge a los **promedios muestrales de los retornos reales** observados después de cada visita. Eso, en el sentido de minimizar el error cuadrático medio *sobre el set de entrenamiento*, es **óptimo**. Entonces: **¿cómo carajo TD puede ganarle a un método óptimo?** Porque la optimalidad de MC es *limitada* (minimiza el error sobre los datos que ya viste), mientras que la de TD es *la que importa para predecir retornos*.

### Ejemplo didáctico 3: "You are the Predictor" (Ejemplo 6.4)

El experimento mental del libro para entender esa diferencia. Sos el predictor de retornos de un MRP desconocido y observaste estos **ocho episodios**:

- Episodio 1: arrancás en `A`, pasás a `B` con recompensa 0, y desde `B` terminás con recompensa 0.
- Episodios 2–8: arrancan en `B` y terminan de inmediato (6 de ellos con retorno **1**, y el restante con retorno **0**).

**Primero, $V(B)$: no hay discusión.** En 8 apariciones, 6 veces terminó con retorno 1 y 2 veces con 0. Todo el mundo diría lo mismo:

$$
V(B) = \frac{6}{8} = 0{,}75
$$

**Ahora, $V(A)$: hay dos respuestas razonables.**

- **Respuesta 1 (la de TD).** El 100% de las veces que el proceso estuvo en `A`, pasó inmediatamente a `B` con recompensa 0. Como ya fijamos $V(B) = 0{,}75$, entonces **`A` vale $0{,}75$ también**. Otra forma de verlo: modelás el proceso Markov como
  `A --0--> B --0--> [terminal]` y calculás la función de valor correcta de ese modelo. **Este es el valor que da batch TD(0).**
- **Respuesta 2 (la de MC).** Vimos `A` **una vez**, y el retorno que siguió fue 0; entonces estimamos **`V(A) = 0`**. **Este es el valor que da batch MC** — y además es el que da **error cero sobre los datos de entrenamiento**.

**Y sin embargo esperamos que la primera sea mejor.** Si el proceso es Markov, la respuesta 1 tiene menor error sobre **datos futuros**, aunque la respuesta 2 sea perfecta sobre los datos existentes.

**La generalización detrás del ejemplo:**

- **Batch MC** siempre encuentra las estimaciones que **minimizan el error cuadrático medio sobre el set de entrenamiento**.
- **Batch TD(0)** siempre encuentra las estimaciones que serían **exactamente correctas para el modelo de máxima verosimilitud** del proceso Markov. El *maximum-likelihood estimate* de un parámetro es el valor cuya probabilidad de generar los datos observados es mayor: acá, la probabilidad de transición estimada de $i$ a $j$ es la fracción de transiciones observadas desde $i$ que fueron a $j$, y la recompensa esperada asociada es el promedio de las observadas en esas transiciones. La función de valor que sería exactamente correcta si ese modelo fuera correcto se llama **certainty-equivalence estimate**, porque equivale a **asumir que la estimación del proceso se conoce con certeza** en lugar de estar aproximada.

> **Esto explica por qué TD converge más rápido que MC.** En forma batch, TD(0) es más rápido porque computa la verdadera estimación de *certainty equivalence*. También puede explicar en parte la ventaja de TD(0) no batch: aunque los métodos no batch no llegan ni a la estimación de *certainty equivalence* ni a la de mínimo error cuadrático, se los puede entender como **moviéndose aproximadamente en esas direcciones**. **TD(0) puede ser más rápido que constant-$\alpha$ MC porque se está moviendo hacia una mejor estimación, aunque no llegue del todo.** En el estado actual del campo no se puede decir nada más definitivo sobre la eficiencia relativa online.

**Y un remate que duele:** aunque la *certainty-equivalence estimate* es en algún sentido una solución óptima, **casi nunca es factible calcularla directamente**. Si $n = |\mathcal{S}|$ es el número de estados, solo **formar** la estimación de máxima verosimilitud del proceso puede requerir del orden de $n^2$ de memoria, y computar la función de valor correspondiente requiere del orden de $n^3$ pasos de cómputo si se hace de forma convencional. En esos términos es realmente llamativo que **TD pueda aproximar la misma solución usando memoria del orden de $n$ y cómputo repetido sobre el set de entrenamiento**. En tareas con espacios de estado grandes, **TD puede ser la única forma factible de aproximar la solución de certainty equivalence**.

**Ejercicio:** **6.7** — diseñar una versión *off-policy* del update TD(0) que sirva con una política target $\pi$ arbitraria y una behavior policy $b$ cubriente, usando en cada paso $t$ el importance sampling ratio $\rho_{t:T-1}$ de (5.3).

---

## (6.4) — Sarsa: On-policy TD Control

**Qué representa:** pasamos de **predicción** a **control**, manteniendo el patrón de GPI: TD se usa para el lado de la evaluación, y la mejora sigue siendo "volverse greedy respecto de $q_\pi$". Aparece el mismo dilema del cap. 5 — exploración contra explotación — y por eso los métodos se dividen en **on-policy** y **off-policy**. Éste es el on-policy.

**El primer paso: de $v$ a $q$.** Igual que en MC (secc. 5.2), para *actuar* no alcanza con $v_\pi$: necesitamos el valor de cada **par estado–acción**. Un episodio es una secuencia alternada de estados y pares estado–acción:

$$
\ldots, S_t, A_t, R_{t+1}, S_{t+1}, A_{t+1}, R_{t+2}, \ldots
$$

En 6.1 considerábamos transiciones de **estado a estado** y aprendíamos valores de estados. Ahora consideramos transiciones de **par estado–acción a par estado–acción**. Formalmente es el mismo caso: ambos son cadenas de Markov con proceso de recompensa, así que **los teoremas de convergencia de los valores de estado bajo TD(0) también aplican**:

$$
Q(S_t, A_t) \leftarrow Q(S_t, A_t) + \alpha\,[\, R_{t+1} + \gamma Q(S_{t+1}, A_{t+1}) - Q(S_t, A_t) \,] \tag{6.7}
$$

La actualización se hace **después de cada transición desde un estado no terminal** $S_t$. Si $S_{t+1}$ es terminal, se define $Q(S_{t+1}, A_{t+1}) = 0$. Esta regla usa **cada elemento de la quíntupla** $(S_t, A_t, R_{t+1}, S_{t+1}, A_{t+1})$ que forma una transición de un par estado–acción al siguiente, y de ahí sale el nombre **Sarsa** (*state–action–reward–state–action*).

**Pseudocódigo (Sarsa, on-policy TD control, para estimar $Q \approx q_*$):**
1. **Parámetros:** step size $\alpha \in (0, 1]$, $\varepsilon > 0$ chico.
2. Inicializar $Q(s, a)$ para todo $s \in \mathcal{S}^+$, $a \in \mathcal{A}(s)$, arbitrariamente, salvo $Q(\text{terminal}, \cdot) = 0$.
3. Por cada episodio: inicializar $S$; elegir $A$ desde $S$ con una política derivada de $Q$ (p. ej. $\varepsilon$-greedy).
4. Por cada paso: ejecutar $A$ y observar $R, S'$; **elegir $A'$ desde $S'$ con la política derivada de $Q$**; **$Q(S, A) \leftarrow Q(S, A) + \alpha[\,R + \gamma Q(S', A') - Q(S, A)\,]$**; $S \leftarrow S'$; $A \leftarrow A'$. Hasta que $S$ sea terminal.

**Convergencia.** Depende de cómo se derive la política de $Q$ (puede ser $\varepsilon$-greedy o $\varepsilon$-soft). **Sarsa converge con probabilidad 1 a una política y una función de valor de acción óptimas**, siempre que (i) todos los pares estado–acción se visiten infinitas veces y (ii) la política converja en el límite a la política greedy — lo cual se puede conseguir, por ejemplo, con $\varepsilon$-greedy usando $\varepsilon = 1/t$.

### Ejemplo 6.5: windy gridworld

Un gridworld estándar, con start y goal, pero con una diferencia: hay un **viento cruzado** que corre hacia arriba por el medio de la grilla. Las acciones son las cuatro usuales (arriba, abajo, derecha, izquierda), pero en la región central los próximos estados se desplazan hacia arriba por el viento, cuya **fuerza varía de columna en columna** y se escribe debajo de cada columna (en número de casillas de desplazamiento). Por ejemplo: si estás a una casilla a la derecha del goal, la acción *izquierda* te lleva a la casilla justo **arriba** del goal.

Es una tarea **episódica sin descuento**, con recompensas constantes de **−1** hasta llegar al goal.

**Resultado.** Con Sarsa $\varepsilon$-greedy, $\varepsilon = 0{,}1$, $\alpha = 0{,}5$ y valores iniciales $Q(s, a) = 0$: la pendiente creciente del gráfico muestra que **el goal se alcanzaba cada vez más rápido**. A los 8000 pasos de tiempo la política greedy **hacía rato que era óptima** (una trayectoria suya se muestra en la figura); la exploración $\varepsilon$-greedy siguió manteniendo la **longitud media de episodio en unos 17 pasos, dos más que el mínimo de 15**.

> **Y acá está el argumento por qué Sarsa es más apropiado que MC para esta tarea:** con MC **no se puede usar fácilmente**, porque **la terminación no está garantizada para todas las políticas**. Si alguna política hiciera que el agente se quedara en el mismo estado, el siguiente episodio no terminaría nunca. Los métodos paso a paso como Sarsa **no tienen ese problema**, porque aprenden *durante* el propio episodio que esas políticas son malas y cambian.

**Ejercicios:** **6.8** (demostrar la versión action-value de (6.6) para $\delta_t = R_{t+1} + \gamma Q(S_{t+1}, A_{t+1}) - Q(S_t, A_t)$, asumiendo que los valores no cambian entre pasos), **6.9** (resolver el windy gridworld con los **8 movimientos de rey**, ¿cuánto mejor se puede hacer? ¿Conviene agregar una novena acción que no cause movimiento más allá del viento?) y **6.10** (hacer el viento **estocástico**: un tercio de las veces el valor de la columna, un tercio una casilla más arriba, un tercio una casilla más abajo).

---

## (6.5) — Q-learning: Off-policy TD Control

**Qué representa:** uno de los primeros grandes avances del RL fue un algoritmo de control TD *off-policy*. La diferencia con Sarsa es mínima en la escritura y enorme en el comportamiento.

$$
Q(S_t, A_t) \leftarrow Q(S_t, A_t) + \alpha\,[\, R_{t+1} + \gamma \max_a Q(S_{t+1}, a) - Q(S_t, A_t) \,] \tag{6.8}
$$

**Lo decisivo:** la función de valor de acción aprendida, $Q$, aproxima directamente a **$q_*$, el valor de acción óptimo, con independencia de la política que se esté siguiendo**. Eso simplifica drásticamente el análisis del algoritmo y habilitó las primeras pruebas de convergencia muy temprano.

- La política **igual tiene efecto**: determina qué pares estado–acción se **visitan** y se actualizan.
- Pero lo único que hace falta para la convergencia correcta es que **todos los pares sigan actualizándose** (la misma condición mínima del cap. 5: cualquier método que encuentre comportamiento óptimo en el caso general tiene que exigirlo).
- Bajo esa condición y una variante de las condiciones usuales de aproximación estocástica sobre la secuencia de step-sizes, se ha demostrado que **$Q$ converge con probabilidad 1 a $q_*$.**

**Pseudocódigo (Q-learning, off-policy TD control, para estimar $\pi \approx \pi_*$):**
1. **Parámetros:** step size $\alpha \in (0, 1]$, $\varepsilon > 0$ chico.
2. Inicializar $Q(s, a)$ para todo $s \in \mathcal{S}^+$, $a \in \mathcal{A}(s)$, arbitrariamente, salvo $Q(\text{terminal}, \cdot) = 0$.
3. Por cada episodio: inicializar $S$.
4. Por cada paso: elegir $A$ desde $S$ con una política derivada de $Q$ (p. ej. $\varepsilon$-greedy); ejecutar $A$ y observar $R, S'$; **$Q(S, A) \leftarrow Q(S, A) + \alpha[\,R + \gamma \max_a Q(S', a) - Q(S, A)\,]$**; $S \leftarrow S'$. Hasta que $S$ sea terminal.

**El backup diagram de Q-learning** (fig. 6.4): como (6.8) actualiza un par estado–acción, el **nodo raíz es un<Action>filled action node**. Y la actualización viene *desde* nodos de acción, maximizando sobre todas las acciones posibles en el próximo estado — o sea, los **nodos de abajo son todos los nodos de acción de $S_{t+1}$**, con el **arco de maximización** cruzándolos (igual que en la fig. 3.4 derecha).

### Ejemplo didáctico 4: cliff walking (Ejemplo 6.6)

Este ejemplo compara Sarsa y Q-learning y resalta la diferencia on-policy vs off-policy de la forma más limpia posible.

- Es una tarea **episódica sin descuento**, con start y goal, y las cuatro acciones usuales.
- La recompensa es **−1 en todas las transiciones**, salvo las que entran en la región marcada *"The Cliff"*.
- Entrar en el precipicio da **−100** y manda al agente **instantáneamente de vuelta al start**.

**El resultado (fig. 6.7), con $\varepsilon$-greedy y $\varepsilon = 0{,}1$:**

- **Q-learning**, después de un transitorio inicial, aprende los valores de la **política óptima**: la que viaja a la derecha **por el borde del precipicio**. Es la más corta… y por lo mismo, con la selección $\varepsilon$-greedy, **cae ocasionalmente al precipicio**.
- **Sarsa**, en cambio, **sí tiene en cuenta la selección de acciones** en su actualización, y aprende el camino **más largo pero más seguro** por la parte de arriba de la grilla.

> **La moraleja (y es un resultado contraintuitivo):** aunque Q-learning aprende los valores de la política óptima, **su desempeño online es peor** que el de Sarsa, que aprendió la política roundabout. La razón es que Q-learning evalúa la política greedy *así como si no tuviera que seguir explorando con ella*: ignora el costo que la exploración le impone a sí mismo. Sarsa es *on-policy*: su target usa $A_{t+1}$, la acción que **realmente** se va a elegir. Si $\varepsilon$ se redujera gradualmente, **ambos convergerían asintóticamente a la política óptima**.

**Ejercicios:** **6.11** (¿por qué Q-learning se considera un método de control *off-policy*?) y **6.12** (si la selección de acciones fuera greedy, ¿sería Q-learning exactamente el mismo algoritmo que Sarsa? ¿Harían exactamente las mismas selecciones de acción y updates?).

---

## (6.6) — Expected Sarsa

**Qué representa:** un algoritmo que es **exactamente Q-learning salvo por un cambio**: en vez del máximo sobre los pares estado–acción siguientes, usa el **valor esperado**, teniendo en cuenta qué tan probable es cada acción bajo la política actual.

$$
Q(S_t, A_t) \leftarrow Q(S_t, A_t) + \alpha\,[\, R_{t+1} + \gamma \sum_a \pi(S_{t+1}, a)\, Q(S_{t+1}, a) - Q(S_t, A_t) \,] \tag{6.9}
$$

Por lo demás sigue el esquema de Q-learning. Dado el próximo estado $S_{t+1}$, este algoritmo se mueve **determinísticamente en la misma dirección que Sarsa se mueve *en expectativa***, y por eso se llama **Expected Sarsa**. Su backup diagram está en la fig. 6.4.

**El trade-off.** Es **más complejo computacionalmente** que Sarsa, pero a cambio **elimina la varianza** debida a la selección aleatoria de $A_{t+1}$. Con la misma cantidad de experiencia se esperaría un rendimiento ligeramente mejor que Sarsa, y en general lo es.

**Resultados en cliff walking (fig. 6.3, adaptada de van Seijen et al. 2009).** La figura muestra el desempeño *interim* (promedio sobre los primeros 100 episodios) y el *asintótico* (promedio sobre 100.000 episodios) de Sarsa, Q-learning y Expected Sarsa, en función de $\alpha$, todos con política $\varepsilon$-greedy y $\varepsilon = 0{,}1$:

- **Expected Sarsa conserva la ventaja significativa de Sarsa sobre Q-learning** en este problema (es decir, es mucho mejor en el comportamiento *interim*, donde la exploración es lo que domina).
- Además, **Expected Sarsa mejora significativamente a Sarsa** sobre un rango amplio de valores de $\alpha$.
- En cliff walking **todas las transiciones de estado son deterministas** y toda la aleatoriedad viene de la política. En esos casos, **Expected Sarsa puede poner $\alpha = 1$ sin sufrir degradación del desempeño asintótico**, mientras que **Sarsa solo puede rendir bien en el largo plazo con un $\alpha$ chico, en el cual su desempeño a corto plazo es malo**. (Los círculos sólidos de la figura marcan el mejor desempeño *interim* de cada método.)

**La generalización importante (y un cambio respecto de la 1da edición).** En estos resultados Expected Sarsa se usó *on-policy*, pero **en general podría usar una política diferente de la política target $\pi$ para generar comportamiento, en cuyo caso se vuelve *off-policy***. Por ejemplo: si $\pi$ es la política greedy pero el comportamiento es más exploratorio, **entonces Expected Sarsa es exactamente Q-learning**.

> En este sentido, **Expected Sarsa subsume y generaliza a Q-learning, mientras que mejora de forma confiable a Sarsa**. Salvo por el pequeño costo computacional adicional, **Expected Sarsa puede dominar por completo a los otros dos algoritmos TD de control más conocidos**.

---

## (6.7) — Maximization Bias and Double Learning

**Qué representa:** una advertencia sobre un sesgo sutil que affects **todos** los algoritmos de control del capítulo, y su remedio.

**El sesgo.** Todos los algoritmos discutidos hasta acá involucran **maximización** al construir el target. En Q-learning, la política target es la greedy, que se define con un $\max$. En Sarsa, la política suele ser $\varepsilon$-greedy, que también involucra una maximización. En todos estos casos, **se está usando un máximo sobre valores estimados como si fuera una estimación del máximo de los valores verdaderos — y eso puede producir un sesgo positivo significativo**.

**El mecanismo, en el caso más simple.** Considerá un estado $s$ con muchas acciones $a$ cuyos valores verdaderos $q(s, a)$ son **todos cero**, pero cuyas estimaciones $Q(s, a)$ son inciertas y por lo tanto están distribuidas unas por encima de cero y otras por debajo. El máximo de los valores verdaderos es cero, pero **el máximo de las estimaciones es positivo**. Eso es el ***maximization bias***.

Una forma de verlo: el problema es que **se usan las mismas muestras para determinar la acción maximizadora y para estimar su valor**. El valor maximizado es ruidoso, así que tenderá a estar inflado.

### Ejemplo 6.7: el MDP del sesgo de maximización

Un MDP mínimo de la figura 6.5:

- Dos estados no terminales, **`A`** y **`B`**. Los episodios **siempre arrancan en `A`**, con dos acciones: `left` y `right`.
- **`right`** lleva **inmediatamente** al estado terminal, con recompensa y retorno **0**.
- **`left`** lleva a `B`, también con recompensa 0. Desde `B` hay muchas acciones posibles, y **todas** terminan de inmediato con una recompensa sacada de una **distribución normal con media −0.1 y varianza 1.0**.

**El análisis correcto:** el retorno esperado de cualquier trayectoria que empiece con `left` es **−0.1**, así que **elegir `left` en `A` es siempre un error**. Y sin embargo, **los métodos de control pueden favorecer `left`**, porque el sesgo de maximización hace que **`B` parezca tener valor positivo** (es el máximo sobre muchas estimaciones ruidosas de un valor verdadero negativo).

**El resultado (fig. 6.5, $\varepsilon = 0{,}1$, $\alpha = 0{,}1$, $\gamma = 1$):** Q-learning con selección $\varepsilon$-greedy **aprende inicialmente a favorecer fuertemente la acción `left`**. Incluso asintóticamente, Q-learning toma `left` alrededor de un **5% más de lo óptimo** (recordá que $\varepsilon = 0{,}1$ ya impone un 5% mínimo de probabilidad de acción no-greedy). **Double Q-learning es esencialmente inmune al sesgo de maximización.**

**La idea del double learning.** Partamos de un caso bandit con estimaciones ruidosas del valor de muchas acciones, obtenidas como promedios muestrales. Usar el máximo de las estimaciones como estimación del máximo de los valores verdaderos tiene un sesgo positivo. **La causa: usar las mismas muestras (las partidas) tanto para determinar la acción maximizadora como para estimar su valor.**

El arreglo: **dividir las partidas en dos conjuntos** y aprender **dos estimaciones independientes**, $Q_1(a)$ y $Q_2(a)$, ambas estimaciones del verdadero $q(a)$ para todo $a \in \mathcal{A}$. Se usa **una** estimación para determinar la acción maximizadora, $A^* = \arg\max_a Q_1(a)$, y la **otra** para estimar el valor de esa acción:

$$
Q_2(A^*) \;=\; Q_2(\arg\max_a Q_1(a))
$$

Esta estimación es **insesgada** en el sentido de que $\mathbb{E}[\,Q_2(A^*)\,] = q(A^*)$. El proceso se puede repetir con los roles invertidos para dar una segunda estimación insesgada. **Ésta es la idea del double learning.** Nótese que aunque se aprenden dos estimaciones, **solo una se actualiza en cada paso**: double learning **duplica el requerimiento de memoria, pero no aumenta la cantidad de cómputo por paso**.

**Double Q-learning** extiende la idea a MDPs completos. Divide los pasos de tiempo en dos — por ejemplo, tirando una moneda en cada paso. Si sale cara, la actualización es:

$$
Q_1(S_t, A_t) \leftarrow Q_1(S_t, A_t) + \alpha\,[\, R_{t+1} + \gamma Q_2(S_{t+1}, \arg\max_a Q_1(S_{t+1}, a)) - Q_1(S_t, A_t) \,] \tag{6.10}
$$

Si saletails, se hace **exactamente la misma actualización con $Q_1$ y $Q_2$ intercambiadas**, de modo que se actualiza $Q_2$. Las dos funciones de valor aproximadas se tratan **completamente simétricamente**. (La política de comportamiento puede usar ambas estimaciones: una política $\varepsilon$-greedy para Double Q-learning podría basarse en el **promedio** —o la suma— de las dos estimaciones de valor de acción.)

**Pseudocódigo (Double Q-learning, para estimar $Q_1 \approx Q_2 \approx q_*$):**
1. **Parámetros:** step size $\alpha \in (0, 1]$, $\varepsilon > 0$ chico.
2. Inicializar $Q_1(s, a)$ y $Q_2(s, a)$ para todo $s \in \mathcal{S}^+$, $a \in \mathcal{A}(s)$, con $Q(\text{terminal}, \cdot) = 0$.
3. Por cada episodio: inicializar $S$.
4. Por cada paso: elegir $A$ desde $S$ con la política $\varepsilon$-greedy en $Q_1 + Q_2$; ejecutar $A$ y observar $R, S'$; **con probabilidad 0.5** aplicar el update de $Q_1$ con (6.10), **si no** el update de $Q_2$ con los índices intercambiados; $S \leftarrow S'$. Hasta que $S$ sea terminal.

**Ejercicio:** **6.13** — ¿cuáles son las ecuaciones de actualización para **Double Expected Sarsa** con una política target $\varepsilon$-greedy?

---

## (6.8) — Games, Afterstates, and Other Special Cases

**Qué representa:** el capítulo intenta presentar un enfoque uniforme para una clase amplia de tareas, pero siempre hay tareas excepcionales que se tratan mejor de forma especializada. El caso que el libro elige es el **tic-tac-toe del cap. 1**.

**El problema con el ejemplo del cap. 1.** Ahí se presentó un método TD para jugar al tic-tac-toe que aprendía algo mucho más parecido a una **función de valor de estado**. Si se mira de cerca, resulta que esa función aprendida **no es ni una action-value function ni una state-value function en el sentido usual**:

- Una **state-value function** convencional evalúa estados **en los que el agente tiene la opción de elegir una acción**.
- La del tic-tac-toe evalúa posiciones del tablero **después de que el agente ya hizo su movimiento**.

A estas se las llama ***afterstates***, y a las funciones de valor sobre ellas, ***afterstate value functions***.

**Cuándo son útiles.** Los afterstates son valiosos **cuando tenemos conocimiento de una parte inicial de la dinámica del entorno, pero no necesariamente de la dinámica completa**. Por ejemplo, en los juegos: típicamente **sabemos los efectos inmediatos de nuestros movimientos**. Sabemos, para cada jugada posible de ajedrez, cuál es la posición resultante, **pero no qué va a responder el oponente**. Las afterstate value functions son una forma natural de aprovechar ese tipo de conocimiento, y producen un método de aprendizaje más eficiente.

**El argumento de por qué son más eficientes (Ejemplo 6.1 del cap. 1, reproducido aquí).** Una action-value function convencional mapea *(posición, movimiento)* a una estimación del valor. Pero **muchos pares posición-movimiento producen la misma posición resultante**:

```
  posición₁ ─movimiento a─╮
                         ├─▶  (misma "afterposition")  ──▶  un solo valor
  posición₂ ─movimiento b─╯
```

En esos casos los pares posición-movimiento **son distintos pero producen la misma afterposition**, y por lo tanto **deben tener el mismo valor**. Una action-value function convencional tendría que evaluar **ambos pares por separado**; una afterstate value function **los evalúa inmediatamente como iguales**. **Todo lo que se aprenda sobre el par de la izquierda se transfiere instantáneamente al par de la derecha.**

**No es solo un truco de juegos.** Los afterstates aparecen en muchas tareas. Por ejemplo, en **tareas de colas** hay acciones como asignar clientes a servidores, rechazar clientes o descartar información. En esos casos **las acciones están definidas en términos de sus efectos inmediatos, que se conocen completamente**.

**Y el resto del marco sigue valiendo.** Es imposible describir todos los tipos posibles de problemas especializados y sus algoritmos. Sin embargo, **los principios desarrollados en el libro deberían aplicar ampliamente**: los métodos con afterstates todavía se describen apropiadamente en términos de **GPI**, con una política y una función de valor (de afterstates) interactuando esencialmente de la misma manera. Y en muchos casos **todavía se enfrenta la elección entre métodos on-policy y off-policy** para manejar la necesidad de exploración persistente.

**Ejercicio:** **6.14** — describir cómo la tarea de **Jack's Car Rental** (Ejemplo 4.1, del cap. 4) podría reformularse en términos de afterstates. ¿Por qué, en términos de esta tarea específica, una reformulación así **aceleraría la convergencia**?

---

## (6.9) — Summary

**Lo que aporta el capítulo:**

- **TD learning** es una clase nueva de método de aprendizaje, y una alternativa a los métodos Monte Carlo para resolver el problema de **predicción**. En ambos casos, la extensión al problema de **control** es vía la idea de **GPI** (abstracta de la programación dinámica): políticas y funciones de valor aproximadas deberían interactuar de manera que **ambas se muevan hacia sus valores óptimos**.
- Los **dos procesos** que forman GPI: uno maneja la función de valor para predecir con precisión los retornos de la política actual (**predicción**); el otro maneja la política para mejorarla localmente (p. ej., volverla $\varepsilon$-greedy) respecto de la función de valor actual.
- **La complicación de la exploración.** Cuando el proceso de predicción se basa en experiencia, aparece una complicación: mantener **exploración suficiente**. Los métodos de control TD se clasifican según cómo resuelven esto: **Sarsa es on-policy**, **Q-learning es off-policy**, y **Expected Sarsa también es off-policy** tal como se presenta acá. Existe una **tercera vía** que el capítulo no incluye: los métodos **actor–critic**, que se cubren completo en el cap. 13.
- **Son los métodos de RL más ampliamente usados hoy**, probablemente por su gran simplicidad: se pueden aplicar online, con una cantidad mínima de cómputo, a experiencia generada por interacción con el entorno; y se pueden expresar **casi por completo con ecuaciones individuales** implementables en programas chicos.

**Lo que viene después (la hoja de ruta del libro).** En los próximos capítulos los algoritmos se van haciendo "un poco más complicados y significativamente más potentes". Todos los nuevos algoritmos **conservan la esencia** de estos:

- Se procesa experiencia **online**, con poco cómputo.
- Son **impulsados por TD errors**.

Los casos especiales introducidos en este capítulo se deberían llamar propiamente métodos TD ***one-step, tabular, model-free***. En los dos capítulos siguientes se los extiende a:

1. Formas ***n*-step*** (cap. 7) → un **puente hacia Monte Carlo**.
2. Formas que **incluyen un modelo del entorno** (cap. 8) → un **puente hacia la planificación y la programación dinámica**.

Y en la **segunda parte del libro** se los extiende a **aproximación de funciones** en vez de tablas (cap. 9 en adelante) → un **puente hacia el aprendizaje profundo y las redes neuronales**.

**Y una ampliación de alcance importante.** El capítulo discutió los métodos TD enteramente dentro del contexto de los problemas de RL, pero **los métodos TD son en realidad más generales que eso**. Son **métodos generales para aprender a hacer predicciones de largo plazo sobre sistemas dinámicos**. Por ejemplo, pueden ser relevantes para predecir datos financieros, expectativas de vida, resultados electorales, patrones climáticos, comportamiento animal, demanda sobre centrales eléctricas o compras de clientes. Fue recién **cuando los métodos TD se analizaron como métodos de predicción puros, independientes de su uso en RL**, que sus propiedades teóricas se entendieron bien. Aun así, estas otras aplicaciones potenciales **no han sido exploradas extensamente** hasta el momento.

---

## Tabla comparativa: los cuatro algoritmos de control TD

Todos son **tabulares, model-free, one-step** y arrancan de GPI. Lo que cambia es **qué estiman** y **qué le ponen como target**:

| | **Sarsa** (6.4) | **Q-learning** (6.5) | **Expected Sarsa** (6.6) | **Double Q-learning** (6.7) |
|---|---|---|---|---|
| **Ecuación** | (6.7) | (6.8) | (6.9) | (6.10) |
| **Estima** | $q_\pi$ (política actual) | $q_*$ (independiente de $\pi$) | según la política del target | $Q_1, Q_2 \approx q_*$ (dos copias) |
| **Target** | $R_{t+1} + \gamma Q(S_{t+1}, A_{t+1})$ | $R_{t+1} + \gamma \max_a Q(S_{t+1}, a)$ | $R_{t+1} + \gamma \sum_a \pi(S_{t+1}, a) Q(S_{t+1}, a)$ | $R_{t+1} + \gamma Q_2(S_{t+1}, \arg\max_a Q_1)$ |
| **¿Usa la acción real siguiente?** | **Sí** ($A_{t+1}$) | No | No (espera sobre $\pi$) | No (espera sobre el $\arg\max$) |
| **Tipo** | on-policy | off-policy | on-policy si $\pi$ = comportamiento; off-policy si difieren | off-policy (por construcción) |
| **Convergencia** | c.p. 1 a óptimo si todos los pares se visitan infinitas veces y $\pi \to$ greedy (p. ej. $\varepsilon = 1/t$) | c.p. 1 a $q_*$ si todos los pares se siguen actualizando + condiciones de step-size | se selló teóricamente (van Seijen et al. 2009) | hereda la de Q-learning; elimina el sesgo |
| **Sesgo de maximización** | Sí (menor) | **Sí, fuerte** | Sí (menor que Q-learning) | **No** |
| **Costo computacional** | Bajo | Bajo | Más caro (espera sobre acciones) | Bajo (2 tablas, 1 update por paso) |
| **Fortaleza** | Seguro en la práctica, aprende rápido online | Simple, convergencia a óptimo garantizada | Combina lo mejor: domina a Sarsa y generaliza Q-learning | Elimina el sesgo, dobla la memoria |
| **Debilidad** | Convergencia lenta si hay muchas acciones no-greedy | Aprende valores que su propia política no va a seguir (cae al precipicio) | Más caro | Doble memoria |

**Ejemplo de la tabla en acción — cliff walking (Ej. 6.6):**

| | Ruta que aprende | Comportamiento online |
|---|---|---|
| **Q-learning** | por el borde del precipicio (la óptima) | Peor: cae al precipicio por la exploración $\varepsilon$-greedy |
| **Sarsa** | por arriba, más larga pero más segura (la *roundabout policy*) | Mejor: tiene en cuenta el costo de explorar |
| **Expected Sarsa** | como Sarsa, sin la varianza de elegir $A_{t+1}$ | El mejor de los tres en un rango amplio de $\alpha$ |
| **Double Q-learning** | (elimina el sesgo de maximización) | Casi no afectado por el sesgo |

> Ojo con un detalle que el texto sí aclara: aunque Q-learning **aprende los valores de la política óptima**, su desempeño *online* es peor. Y si $\varepsilon$ se redujera gradualmente, **ambos convergerían asintóticamente a la política óptima**.

---

## Cómo se conecta con los capítulos 4, 5, 7 y 12

- El cap. **4** (DP) dio el esqueleto: **GPI**, *policy improvement* y las ecuaciones de Bellman como reglas de actualización. Pero con la **muleta del modelo completo** $p(s', r \mid s, a)$.
- El cap. **5** (MC) tomó ese mismo esqueleto y lo hizo funcionar **solo con episodios**, pero **sin bootstrap** (esperaba al final del episodio y no usaba sus propias estimaciones). Era el extremo opuesto.
- El cap. **6** (TD) **mantiene "aprender de la experiencia" (sin modelo) pero reintroduce el *bootstrapping*** de DP: aprende de sus propias estimaciones, **paso a paso**. Es el eslabón que faltaba, y explica por qué TD suele ser más rápido que MC.
- **El eje de todo el libro son dos propiedades separables:** *¿necesita modelo?* y *¿usa bootstrap?*. DP = modelo + bootstrap; MC = sin modelo + sin bootstrap; TD = sin modelo + bootstrap. Los capítulos siguientes exploran las otras combinaciones.
- El cap. **7** (*n*-step bootstrapping) extiende TD(0) hacia MC: el *n*-step target promedia los TD errors de $n$ pasos hacia adelante, interpolando entre **TD puro** ($n = 1$) y **MC puro** ($n = \infty$).
- El cap. **12** (TD($\lambda$)) **unifica sin costuras** TD y MC: en vez de esperar $n$ pasos fijos, el parámetro $\lambda$ permite *mezclar* los TD errors de todos los horizontes con pesos geométricos decrecientes ($\lambda = 0$ es TD(0); $\lambda = 1$ es MC).
- El cap. **8** (Dyna y la planificación) extiende TD para que **incluya un modelo**, cerrando el otro extremo del eje.
- La **segunda parte** (caps. 9 en adelante) reemplaza las tablas por **aproximación de funciones** (redes neuronales, tile coding), pero mantiene la esencia TD: **online, con poco cómputo, e impulsado por TD errors**.
- **En el cap. 13** aparecen los métodos **actor–critic**, la tercera vía de control TD que este capítulo menciona pero no desarrolla.

---

## Nota sobre la transcripción de las ecuaciones

> En la conversión local del EPUB (`bibliografia/libro/`) **todas las ecuaciones y figuras del capítulo 6 quedaron como imágenes `.gif`**, que no pude leer directamente. Las **diez ecuaciones (6.1)–(6.10)** de este resumen fueron reconstruidas a partir del texto circundante (que las numera y las describe) y de las referencias cruzadas internas del propio capítulo — por ejemplo, el ejercicio 6.1 confirma que (6.5) es el TD error y (6.2) la actualización de TD(0); el ejercicio 6.8 confirma que (6.6) es el error MC como suma de TD errors; y el texto de 6.5 confirma que (6.8) es el update de Q-learning. Los **valores numéricos** del Ejemplo 6.2 (los valores verdaderos del random walk) y del Ejemplo 6.4 fueron **derivados y verificados** contra el sistema de ecuaciones de Bellman y contra el `v_π(C) = 0.5` que el texto sí explicita. Aun así, conviene **cotejar las ecuaciones contra el PDF** (`bibliografia/SuttonBartoIPRLBook2ndEd.pdf`) antes de entregar la tarea.
