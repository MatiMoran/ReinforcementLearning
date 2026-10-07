# Tarea 2 — Multi-armed Bandits (Capítulo 2)

**Fuente:** Sutton & Barto, *Reinforcement Learning: An Introduction* (2da ed.), **Capítulo 2** (Multi-armed Bandits).

> **Aclaración:** el capítulo 2 estudia el RL en su forma más simple: un problema **no asociativo** en el que eliges una acción entre $k$ opciones y solo te importa maximizar la recompensa total — no hay estados ni consecuencias diferidas. Es el escenario perfecto para aislar el **conflicto exploración–explotación** y para comparar los métodos básicos de balance: *greedy*, *$\varepsilon$-greedy*, *optimistic initial values*, *UCB* y *gradient bandits*. Secciones: 2.1 el problema *k*-armed, 2.2 action-value methods, 2.3 el 10-armed testbed, 2.4 incremental implementation, 2.5 problemas no estacionarios, 2.6 optimistic initial values, 2.7 UCB, 2.8 gradient bandits, 2.9 associative search (contextual bandits) y 2.10 el resumen (con Gittins indexes y Thompson sampling).

**Índice**

1. Encuadre: feedback evaluativo (la esencia del RL)
2. (2.1) A *k*-armed Bandit Problem
3. (2.2) Action-value Methods
4. (2.3) The 10-armed Testbed
5. (2.4) Incremental Implementation
6. (2.5) Tracking a Nonstationary Problem
7. (2.6) Optimistic Initial Values
8. (2.7) Upper-Confidence-Bound Action Selection
9. (2.8) Gradient Bandit Algorithms
10. (2.9) Associative Search (Contextual Bandits)
11. (2.10) Summary
12. Cómo se conecta con los capítulos 1, 3 y 5

---

## Encuadre: feedback evaluativo (la esencia del RL)

Lo que distingue al RL de otros aprendizajes es que usa **información *que evalúa* las acciones tomadas** y no *que instruye* con la acción correcta. El feedback evaluativo indica *qué tan buena* fue la acción, pero no si era la mejor o la peor posible; el feedback instructivo (base del aprendizaje supervisado) indica la acción correcta independientemente de lo hecho. Por eso en el RL nace la necesidad de **exploración activa**: la búsqueda explícita de buen comportamiento.

> El capítulo 2 estudia el aspecto evaluativo en un entorno **no asociativo** (una sola situación, sin estados). Es el caso en el que más claramente se ve la diferencia entre lo evaluativo y lo instructivo, y nos da los métodos básicos que se extienden al problema completo en los capítulos siguientes.

---

## (2.1) — A *k*-armed Bandit Problem

**Qué representa:** el problema de aprendizaje más simple: te enfrentás repetidamente a una elección entre $k$ acciones (los *brazos* de la máquina). Tras cada elección recibís una recompensa numérica de una **distribución de probabilidad estacionaria** que depende de la acción elegida. Objetivo: maximizar la **recompensa total esperada** en un período (p. ej. 1000 pasos).

**Definición formal del valor.** Las acciones nunca elegidas tienen un valor desconocido que queremos estimar. Cada acción $a$ tiene un **valor** $q_*(a)$, su recompensa esperada:

$$
q_*(a) \doteq \mathbb{E}[\, R_t \mid A_t = a \,] \tag{2.1}
$$

Si conociéramos todos los $q_*(a)$, el problema sería trivial: siempre elige la de mayor valor. No los conocemos, pero mantenemos **estimaciones** $Q_t(a)$, y queremos que $Q_t(a) \approx q_*(a)$.

**Idea high-level — el conflicto exploración/explotación:**
- Si en un paso elegís una de las acciones de mayor estimación ($Q_t$ máxima), estás **explotando** tu conocimiento actual.
- Si elegís una acción no greedy, estás **explorando**: mejorás la estimación de esa acción.
- Explotar maximiza la recompensa *de este paso*; explorar puede dar *mayor* recompensa total *a largo plazo* (si hay descentradad, alguna de las acciones aparentemente peores probablemente es mejor que la greedy).

> La recomendación del libro: no buscar un balance "sofisticado" entre explorar y explotar (muchas teorías óptimas asumen estacionariedad o conocimiento previo que no se cumple en RL real) sino **apenas balancearlas**. En este capítulo se muestran métodos simples que lo hacen mucho mejor que explotar siempre.

---

## (2.2) — Action-value Methods

**Qué representa:** los métodos que estiman el valor de las acciones y lo usan para decidir. La forma natural de estimar $q_*(a)$ es promediar las recompensas realmente recibidas — el método *sample-average*:

$$
Q_t(a) \doteq \frac{\sum_{i=1}^{t-1} \mathbb{1}_{A_i = a}\, R_i}{\sum_{i=1}^{t-1} \mathbb{1}_{A_i = a}} \tag{2.2}
$$

donde $\mathbb{1}_{\text{predicate}}$ es 1 si el predicado es verdadero y 0 si no. Si el denominador es 0, $Q_t(a)$ se define con un valor por defecto (p. ej. 0). Por la **ley de los grandes números**, cuando el denominador tiende a infinito, $Q_t(a) \to q_*(a)$.

**Selección de acción.**
- **Greedy:** elegir siempre la acción con mayor estimación:
$$
A_t \doteq \arg\max_a Q_t(a)
$$
(explotación pura: no muestra acciones aparentemente inferiores).
- **$\varepsilon$-greedy:** comportarse greedy la mayoría del tiempo, pero con pequeña probabilidad $\varepsilon$ elegir al azar entre **todas** las acciones con igual probabilidad, independiente de las estimaciones.

**Idea high-level:**
- $\varepsilon$-greedy garantiza (asintóticamente) que **cada acción se muestrea infinitas veces**: todas las $Q_t(a)$ convergen a $q_*(a)$ y la probabilidad de elegir la acción óptima converge a $> 1 - \varepsilon$. Son solo garantías asintóticas; poco dicen de la efectividad práctica.
- **Ejercicio 2.1:** con dos acciones y $\varepsilon = 0.5$, ¿con qué probabilidad se elige la greedy? (Pista: la mitad del tiempo al azar, más la mitad del $\varepsilon$... en realidad: $\varepsilon/2$ va a la otra, así que la greedy se elige con $1 - \varepsilon/2 = 0.75$).

---

## (2.3) — The 10-armed Testbed

**Qué representa:** el banco de pruebas para comparar los métodos. Se generaron **2000 problemas** *k*-armed con $k = 10$. En cada uno, los valores reales $q_*(a)$ salen de una normal $N(0, 1)$; la recompensa real $R_t$ de elegir $A_t$ sale de $N(q_*(A_t), 1)$. Cada método corre **1000 pasos** por problema (*run*); se promedian los resultados sobre los 2000 runs.

**Resultados (fig. 2.2 de greedy vs. $\varepsilon$-greedy):**
- El **greedy** arranca un poco mejor (las primeras muestras) pero se aplana en un nivel bajo: recompensa por paso ~1 vs. ~1.55 óptimo. En solo ~un tercio de las tareas encontró la acción óptima; en el resto, sus primeras muestras de la óptima fueron decepcionantes y **nunca volvió a ella**.
- **$\varepsilon$-greedy con $\varepsilon = 0.1$** explora más, encuentra la óptima más temprano, pero nunca la elige más del 91% de las veces.
- **$\varepsilon = 0.01$** mejora más lento pero a la larga supera al 0.1 en ambos parámetros (recompensa y probabilidad de óptima). Reducir $\varepsilon$ con el tiempo combina lo mejor de ambos.

**Idea high-level:** la ventaja de $\varepsilon$-greedy depende de la tarea. Con mayor varianza de recompensa (más ruido), hace falta más exploración y $\varepsilon$-greedy le gana más cómodo; con varianza cero, el greedy le gana (sabe el valor verdadero tras una muestra). Pero incluso en el caso determinista **conviene explorar** si la tarea es **no estacionaria** (los valores cambian con el tiempo) — y la no estacionariedad es el caso más común en RL: aunque la tarea sea estacionaria y determinista, el aprendiz enfrenta un set de tareas *bandit-like* que cambian a medida que aprende y su política cambia.

---

## (2.4) — Incremental Implementation

**Qué representa:** cómo computar los promedios de forma eficiente, con **memoria constante y cómputo constante por paso** (en vez de guardar todas las recompensas y re-sumarlas). Consideramos una sola acción: $R_i$ es la recompensa de la $i$-ésima selección, y $Q_n$ el valor estimado tras $n-1$ selecciones.

$$
Q_{n+1} \doteq Q_n + \frac{1}{n}\big[\, R_n - Q_n \,\big] \tag{2.3}
$$

Vale incluso para $n = 1$ (con $Q_2 = R_1$). Solo requiere memoria para $Q_n$ y $n$.

**La regla general (aparece en todo el libro):**

$$
\text{NewEstimate} \leftarrow \text{OldEstimate} + \text{StepSize}\,\big[\, \text{Target} - \text{OldEstimate} \,\big] \tag{2.4}
$$

La expresión $[\text{Target} - \text{OldEstimate}]$ es un **error** en la estimación, que se reduce dando un paso hacia el "Target" (que puede ser ruidoso; en este caso, el target es la $n$-ésima recompensa).

**Pseudocódigo (algoritmo bandit completo con $\varepsilon$-greedy):**
1. Inicializar, para $a = 1$ a $k$: $Q(a) \leftarrow 0$, $N(a) \leftarrow 0$.
2. En cada paso $t$: con probabilidad $\varepsilon$ elegir $a$ al azar, si no $a \leftarrow \arg\max Q(a)$; recibir $R$; actualizar $N(a) \leftarrow N(a) + 1$ y $Q(a) \leftarrow Q(a) + \frac{1}{N(a)}[R - Q(a)]$.

**Idea high-level:** el paso usa un **step-size** $\alpha \doteq 1/n$ que varía entre pasos (disminuye al crecer $n$). En adelante el libro lo denota $\alpha$ o, en general, $\alpha_t(a)$.

---

## (2.5) — Tracking a Nonstationary Problem

**Qué representa:** los promedios vistos sirven para problemas **estacionarios** (las probabilidades de recompensa no cambian). En RL aparece mucho la no estacionariedad, donde conviene **dar más peso a las recompensas recientes** que a las lejanas. La forma más popular: un **step-size constante** $\alpha \in (0, 1]$:

$$
Q_{n+1} \doteq Q_n + \alpha\big[\, R_n - Q_n \,\big] \tag{2.5}
$$

Esto hace de $Q_{n+1}$ un *weighted average* de las recompensas pasadas y de la estimación inicial $Q_1$:

$$
Q_{n+1} \doteq (1-\alpha)^n Q_1 + \sum_{i=1}^{n} \alpha (1-\alpha)^{n-i} R_i \tag{2.6}
$$

El peso de $R_i$ decae **exponencialmente** con cuántas recompensas la separan del presente: es un *exponential recency-weighted average* (si $1-\alpha = 0$, todo el peso va a la última recompensa).

**Condiciones de convergencia (teoría de aproximación estocástica).** Para que la secuencia $\alpha_n(a)$ garantice convergencia con probabilidad 1:

$$
\sum_{n=1}^{\infty} \alpha_n(a) = \infty \qquad \text{y} \qquad \sum_{n=1}^{\infty} \alpha_n^2(a) < \infty \tag{2.7}
$$

La primera condición garantiza que los pasos son lo bastante grandes para superar condiciones iniciales; la segunda, que eventualmente se vuelven lo bastante chicos para converger.

**Idea high-level:**
- El *sample-average* ($\alpha_n = 1/n$) cumple ambas condiciones y converge. Un **$\alpha$ constante no cumple la segunda**: las estimaciones nunca convergen del todo sino que siguen variando siguiendo las recompensas recientes — **deseable en un entorno no estacionario**.
- Las secuencias que cumplen (2.7) son para teoría y suelen converger muy lento o requerir mucho tuning; **en la práctica casi no se usan**.

---

## (2.6) — Optimistic Initial Values

**Qué representa:** la dependencia de todos los métodos de los valores iniciales $Q_1(a)$. Esto introduce **bias estadístico**: en sample-average desaparece cuando todas las acciones se seleccionan al menos una vez; con $\alpha$ constante, es permanente aunque decrece (ec. 2.6). En la práctica el bias suele no ser problema (y puede ser útil: permite inyectar conocimiento previo sobre el nivel de recompensa esperable), pero convierte a las estimaciones iniciales en **parámetros que hay que elegir**.

**La técnica para fomentar exploración:** en vez de inicializar en 0 (como en el testbed), inicializar **optimistamente** — p. ej. $Q_1(a) = +5$ cuando los valores reales están alrededor de $N(0,1)$. Un +5 es *salvajemente optimista*: las primeras recompensas siempre quedan por debajo, el aprendiz "se decepciona" y cambia de acción, y así **todas las acciones se prueban varias veces** antes de converger. Resultado: un método **greedy puro** con valores iniciales optimistas explora bastante (fig. 2.3: arranca peor porque explora más, pero termina mejor porque su exploración decae con el tiempo).

**Idea high-level:**
- Es un *simple trick* efectivo en problemas **estacionarios**; **inútil para no estacionarios** porque su impulso explorador es inherentemente **temporal** ("el comienzo del tiempo solo ocurre una vez").
- La misma crítica aplica al sample-average (trata el inicio como evento especial al promediar todo con igual peso). Aun así, estos métodos simples (o combinaciones) suelen ser suficientes en la práctica y el resto del libro los usa con frecuencia.

---

## (2.7) — Upper-Confidence-Bound Action Selection

**Qué representa:** $\varepsilon$-greedy explora **indiscriminadamente** (sin preferir las acciones casi-greedy ni las inciertas). UCB elige acciones según su **potencial de ser óptimas**, considerando a la vez qué tan cerca están las estimaciones del máximo y cuánta incertidumbre tienen:

$$
A_t \doteq \arg\max_a \left[\, Q_t(a) + c \sqrt{\frac{\ln t}{N_t(a)}} \,\right] \tag{2.8}
$$

Si $N_t(a) = 0$, se considera a $a$ como maximizadora. El término de raíz cuadrada es una medida de la **incertidumbre/varianza** de la estimación de $a$; $c > 0$ controla el nivel de confianza (y de exploración). La cantidad maximizada es así una cota superior del valor posible de $a$.

**Por qué funciona:** cada vez que se elige $a$, $N_t(a)$ sube y la incertidumbre baja; cada vez que **no** se elige, $t$ sube pero $N_t(a)$ no, y la incertidumbre **crece**. El logaritmo natural hace que los incrementos se achiquen con el tiempo pero sean sin cota: todas las acciones se eligen eventualmente, pero las de menor valor (o ya muy muestreadas) se eligen con frecuencia decreciente.

**Idea high-level:**
- UCB suele ganarle a $\varepsilon$-greedy en el testbed (fig. 2.4), salvo en los primeros $k$ pasos donde elige al azar entre las no probadas.
- **Limitaciones para el RL completo:** es difícil de extender a problemas no estacionarios (requeriría métodos más complejos que los de 2.5) y a espacios de estado grandes con *function approximation* (Parte II). **Ejercicio 2.8:** el "spike" de UCB en el paso 11 (con $c$ chico es menos prominente).

### Ejemplo didáctico: UCB con 3 bandits

Tenemos 3 máquinas **A**, **B** y **C**, $c = 1$, recompensas ruidosas. Al principio $N_t(a) = 0$ para todas, así que UCB prueba cada una una vez (desempate al azar):

| $t$ | Acción | Recompensa | $Q(A)$ | $Q(B)$ | $Q(C)$ | $N(A), N(B), N(C)$ |
|---|---|---|---|---|---|---|
| 1 | A | 7 | 7.0 | 0 | 0 | 1, 0, 0 |
| 2 | B | 3 | 7.0 | 3.0 | 0 | 1, 1, 0 |
| 3 | C | 5 | 7.0 | 3.0 | 5.0 | 1, 1, 1 |

Paso 4: todas con $N = 1$; $\ln(4) \approx 1.386$, $\sqrt{\ln(4)/1} \approx 1.18$.
- $\mathrm{UCB}(A) = 7 + 1.18 = \mathbf{8.18}$, $\mathrm{UCB}(B) = 3 + 1.18 = 4.18$, $\mathrm{UCB}(C) = 5 + 1.18 = 6.18$ → **A** (su $Q$ es altísima).

| $t$ | Acción | Recompensa | $Q(A)$ | $Q(B)$ | $Q(C)$ | $N(A), N(B), N(C)$ |
|---|---|---|---|---|---|---|
| 4 | A | 6 | 6.5 | 3.0 | 5.0 | 2, 1, 1 |

Paso 5: $\ln(5) \approx 1.609$. $\mathrm{UCB}(A) = 6.5 + \sqrt{1.609/2} = 6.5 + 0.90 = \mathbf{7.40}$, $\mathrm{UCB}(B) = 4.27$, $\mathrm{UCB}(C) = 6.27$ → **A** otra vez (su bonus bajó de 1.18 a 0.90 porque su $N$ creció).

| $t$ | Acción | Recompensa | $Q(A)$ | $Q(B)$ | $Q(C)$ | $N(A), N(B), N(C)$ |
|---|---|---|---|---|---|---|
| 5 | A | 4 | 5.67 | 3.0 | 5.0 | 3, 1, 1 |

Paso 6: $\ln(6) \approx 1.792$. $\mathrm{UCB}(A) = 5.67 + \sqrt{1.792/3} = 5.67 + 0.77 = \mathbf{6.44}$, $\mathrm{UCB}(B) = 4.34$, $\mathrm{UCB}(C) = 5 + 1.34 = 6.34$ ← C se acerca.

| $t$ | Acción | Recompensa | $Q(A)$ | $Q(B)$ | $Q(C)$ | $N(A), N(B), N(C)$ |
|---|---|---|---|---|---|---|
| 6 | A | 5 | 5.50 | 3.0 | 5.0 | 4, 1, 1 |

Paso 7: $\ln(7) \approx 1.946$. $\mathrm{UCB}(A) = 5.50 + \sqrt{1.946/4} = 5.50 + 0.70 = 6.20$, $\mathrm{UCB}(B) = 4.40$, $\mathrm{UCB}(C) = 5 + 1.40 = \mathbf{6.40}$ ← **C gana**: A ya fue muy muestreada (bonus chico), C tiene el torno intacto.

| $t$ | Acción | Recompensa | $Q(A)$ | $Q(B)$ | $Q(C)$ | $N(A), N(B), N(C)$ |
|---|---|---|---|---|---|---|
| 7 | C | 7 | 5.50 | 3.0 | 6.0 | 4, 1, 2 |

**Moraleja:** un greedy se clava en A (máximo $Q = 5.5$); UCB "se aburrió" de A, probó C, y C resultó la mejor en la práctica.

---

## (2.8) — Gradient Bandit Algorithms

**Qué representa:** en vez de estimar valores de acción, se aprende una **preferencia numérica** $H_t(a)$ por cada acción. Más preferencia → más a menudo se elige, pero $H_t$ **no tiene interpretación de recompensa**: solo importan las preferencias relativas (sumar 1000 a todas no cambia nada). Las probabilidades de selección se calculan con una **distribución soft-max** (Gibbs/Boltzmann):

$$
\pi_t(a) \doteq \Pr\{ A_t = a \} \doteq \frac{e^{H_t(a)}}{\sum_{b=1}^{k} e^{H_t(b)}} \tag{2.9}
$$

Inicialmente todas las preferencias iguales (p. ej. 0) → todas las acciones equiprobables. **Ejercicio 2.9:** con dos acciones, la soft-max equivale a la función logística/sigmoide.

**El algoritmo (stochastic gradient ascent).** Tras elegir $A_t$ y recibir $R_t$:

$$
H_{t+1}(A_t) \doteq H_t(A_t) + \alpha\,(R_t - \bar{R}_t)\,(1 - \pi_t(A_t)) \tag{2.10}
$$

$$
H_{t+1}(a) \doteq H_t(a) - \alpha\,(R_t - \bar{R}_t)\,\pi_t(a) \qquad \text{para todo } a \neq A_t
$$

donde $\bar{R}_t$ es el **promedio de todas las recompensas** hasta $t$ (baseline, computable incrementalmente). Si la recompensa supera al baseline, se aumenta la probabilidad de $A_t$; si está por debajo, se reduce. Las no elegidas se mueven en dirección opuesta.

**Idea high-level:**
- El **baseline** reduce la **varianza** y es la razón por la que el algoritmo es *insensible* a desplazamientos globales de las recompensas (fig. 2.5: con recompensas alrededor de +4 en vez de 0, rinde igual; **sin baseline, degrada mucho**).
- **Por qué es gradient ascent:** la actualización (2.10) es, en valor esperado, igual a dar un paso en la **derivada parcial del rendimiento esperado** $\mathbb{E}[R_t] = \sum_x \pi_t(x) q_*(x)$ respecto de $H_t(a)$. No conocemos los $q_*(x)$, pero el **gradiente exacto se puede escribir como una esperanza muestreada** multiplicando por $\pi_t(x)/\pi_t(x)$ y usando $\partial \pi / \partial H$. El baseline $B_t$ puede ser cualquier escalar independiente de la acción (no cambia la esperanza porque $\sum_x \partial \pi_t(x)/\partial H_t(a) = 0$); no afecta el update esperado pero sí la varianza y la velocidad de convergencia. Elegir $\bar{R}_t$ es simple y funciona bien.

---

## (2.9) — Associative Search (Contextual Bandits)

**Qué representa:** el paso del *k*-armed bandit hacia el RL completo: tareas **asociativas**, donde hay más de una situación y la meta es aprender una **política** (mapeo situaciones → acciones).

**El ejemplo del libro:** varios problemas *k*-armed distintos, y en cada paso enfrentás uno elegido al azar. Sin ninguna señal, es un bandit no estacionario que cambia de valores al azar de paso a paso (los métodos de 2.5 fallan). Pero si al aparecer cada tarea recibís una **pista distintiva** (p. ej. el color de la máquina), podés aprender una política que asocie cada tarea (color) con la mejor acción en esa situación.

**Idea high-level:**
- Se llama *associative search* porque combina *búsqueda* por prueba y error con *asociación* de acciones a situaciones. Hoy se los llama **contextual bandits**.
- Es **intermedio** entre el bandit clásico y el RL completo: como el RL completo, implica aprender una política; pero como el bandit, cada acción afecta solo la **recompensa inmediata**. Si las acciones también afectan la **situación siguiente**, tenemos el problema de RL completo (cap. 3). **Ejercicio 2.10:** comparar lo mejor que se puede lograr en un 2-armed sin saber qué caso enfrentás vs. sabiéndolo.

---

## (2.10) — Summary

**Qué queda del capítulo:**

1. **$\varepsilon$-greedy:** elige al azar una fracción pequeña del tiempo.
2. **UCB:** determinista; explora favoreciendo en cada paso las acciones que recibieron menos muestras.
3. **Gradient bandits:** no estiman valores sino **preferencias**; eligen de forma gradual y probabilística con soft-max.
4. **Optimistic initial values:** el simple truco de inicializar optimista hace explorar hasta a los greedys.

**¿Cuál es mejor? (testbed, figs. 2.2–2.6):** en general, **UCB parece el mejor**. Todos tienen un parámetro y una forma de *parameter study*: se resume cada *learning curve* (promedio sobre 1000 pasos, área bajo la curva) como función del parámetro (en escala log, variando por factores de 2). Rasgo típico: **curvas de "U invertida"** — cada método rinde mejor para un valor intermedio del parámetro, ni muy grande ni muy chico. Todos son bastante **insensibles** a su parámetro (rinden bien en un rango de ~un orden de magnitud).

**Idea high-level:** pese a su simpleza, el libro los considera *state of the art* para balancear exploración/explotación; desde el cap. 5 estos métodos simples se usan como piezas del RL completo. Aun así, no son solución totalmente satisfactoria. Más allá del alcance del capítulo:
- **Gittins index:** valor de acción especial que en ciertos casos da soluciones óptimas, pero requiere conocer la distribución previa y no generaliza al RL completo.
- **Métodos Bayesianos / Thompson sampling:** asumen una distribución inicial conocida y la actualizan exactamente; en general caros, pero con *conjugate priors* son fáciles. Elegir por la probabilidad posterior de ser óptima suele rendir similar a los mejores métodos del capítulo.
- Computar el **balance óptimo** exacto equivale a convertir el bandit en un RL completo (el árbol de posibilidades crece $2^{2000}$ hojas con solo 2 acciones y 2 recompensas).

---

## Cómo se conecta con los capítulos 1, 3 y 5

- El **cap. 1** planteó el dilema exploración–explotación como rasgo distintivo; el **2** le da la primera formalización concreta (k-armed) y los métodos para balancearlo.
- En los **bandits** estimamos un valor $q_*(a)$ por acción y las acciones no afectan el futuro; en el **cap. 3 (MDPs)** estimamos $q_*(s, a)$ por *estado y acción*, con recompensa diferida y consecuencias sobre las situaciones siguientes. Los *contextual bandits* (2.9) son el puente exacto.
- Los métodos vistos acá (sample-average, step-sizes, $\varepsilon$-greedy, UCB, optimismo) reaparecen como **subrutinas** del RL completo a partir del **cap. 5**.