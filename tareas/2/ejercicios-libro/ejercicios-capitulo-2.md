# Tarea 2 — Ejercicios del Capítulo 2 (Multi-armed Bandits)

**Fuente:** Sutton & Barto, *Reinforcement Learning: An Introduction* (2da ed.), **Capítulo 2**.
**Ubicación en el libro:** los 11 ejercicios están dispersos al final de las secciones 2.2 a 2.10.

> **Contexto previo:** el capítulo estudia el dilema exploración–explotación en su forma más pura — un *k*-armed bandit sin estados ni recompensa diferida. Métodos cubiertos: *greedy*, *ε-greedy*, *sample average* vs. *step-size constante*, *optimistic initial values*, *UCB*, *gradient bandit* (soft-max) y *associative search*. Reglas clave:
> $$Q_{n+1} = Q_n + \frac{1}{n}[R_n - Q_n] \qquad\text{vs.}\qquad Q_{n+1} = Q_n + \alpha[R_n - Q_n]$$
> $$A_t = \arg\max_a\Big[Q_t(a) + c\sqrt{\tfrac{\ln t}{N_t(a)}}\Big] \quad\text{(UCB)} \qquad \pi_t(a) = \frac{e^{H_t(a)}}{\sum_b e^{H_t(b)}} \quad\text{(soft-max)}$$

**Índice**

1. [Ejercicio 2.1](#ejercicio-21--ε-greedy-con-dos-acciones)
2. [Ejercicio 2.2 — Bandit example](#ejercicio-22--bandit-example)
3. [Ejercicio 2.3](#ejercicio-23--greedy-vs-ε-greedy-a-largo-plazo)
4. [Ejercicio 2.4](#ejercicio-24--pesos-de-un-step-size-variable)
5. [Ejercicio 2.5 (programming)](#ejercicio-25--programming-no-estacionario)
6. [Ejercicio 2.6 — Mysterious Spikes](#ejercicio-26--mysterious-spikes)
7. [Ejercicio 2.7 — Unbiased Constant-Step-Size Trick](#ejercicio-27--unbiased-constant-step-size-trick)
8. [Ejercicio 2.8 — UCB Spikes](#ejercicio-28--ucb-spikes)
9. [Ejercicio 2.9](#ejercicio-29--soft-max-con-dos-acciones)
10. [Ejercicio 2.10](#ejercicio-210--associative-search)
11. [Ejercicio 2.11 (programming)](#ejercicio-211--programming-parameter-study-no-estacionario)

---

## Ejercicio 2.1 — ε-greedy con dos acciones

> **Exercise 2.1** In *ε*-greedy action selection, for the case of two actions and *ε* = 0.5, what is the probability that the greedy action is selected?

### Respuesta

La selección ε-greedy funciona en dos etapas: con probabilidad $\varepsilon$ se elige una acción **al azar entre todas** (aquí, uniforme entre 2), y con probabilidad $1-\varepsilon$ se elige la **greedy**.

$$P(\text{greedy}) = (1-\varepsilon)\cdot 1 + \varepsilon\cdot\frac{1}{2} = 1 - \varepsilon + \frac{\varepsilon}{2} = 1 - \frac{\varepsilon}{2}$$

Con $\varepsilon = 0.5$:

$$P(\text{greedy}) = 1 - 0.25 = \boxed{0.75}$$

**Lectura:** la acción greedy se elige el **75%** de las veces y la no-greedy el 25% (siempre $1 - \varepsilon/2 = 0.75$ y $\varepsilon/2 = 0.25$). Nótese que con $\varepsilon = 0.5$ la mitad del tiempo "greedy" y la mitad "azar" se solapan: cuando toca el azar, la mitad de las veces cae en la greedy de todos modos. Nota general: para $k$ acciones, $P(\text{greedy}) = 1 - \varepsilon + \varepsilon/k$.

---

## Ejercicio 2.2 — Bandit example

> **Exercise 2.2: Bandit example** Consider a *k*-armed bandit problem with *k* = 4 actions, denoted 1, 2, 3, and 4. Consider applying to this problem a bandit algorithm using *ε*-greedy action selection, sample-average action-value estimates, and initial estimates of *Q*₁(*a*) = 0, for all *a*. Suppose the initial sequence of actions and rewards is *A*₁ = 1, *R*₁ = 1, *A*₂ = 2, *R*₂ = 1, *A*₃ = 2, *R*₃ = 2, *A*₄ = 2, *R*₄ = 2, *A*₅ = 3, *R*₅ = 0. On some of these time steps the *ε* case may have occurred, causing an action to be selected at random. On which time steps did this definitely occur? On which time steps could this possibly have occurred?

### Respuesta

**Tabla de estimaciones** (sample average, $Q_1(a)=0$ para todas):

| $t$ | $A_t$ | $R_t$ | $Q$ antes de elegir | conjunto greedy |
|---|---|---|---|---|
| 1 | 1 | 1 | $Q=(0,0,0,0)$ | $\{1,2,3,4\}$ (empate) |
| 2 | 2 | 1 | $Q=(1,0,0,0)$ | $\{1\}$ (estricta) |
| 3 | 2 | 2 | $Q=(1,1,0,0)$ | $\{1,2\}$ (empate) |
| 4 | 2 | 2 | $Q=(1,1.5,0,0)$ | $\{2\}$ (estricta) |
| 5 | 3 | 0 | $Q=(1,1.67,0,0)$ | $\{2\}$ (estricta) |

Después de cada paso: $Q(1)=1$; luego $Q(2)=1$; luego $Q(2)=(1+2)/2=1.5$; luego $Q(2)=(1+2+2)/3\approx1.67$.

- **$t=1$: posiblemente.** Todas valen 0 → todas son greedy; la acción 1 pudo salir tanto del desempate aleatorio entre greedys como del caso ε.
- **$t=2$: definitivamente.** Greedy era estrictamente la acción 1 ($Q=1$), pero se eligió la 2 → solo pudo salir del caso ε.
- **$t=3$: posiblemente.** Greedy eran {1, 2} ($Q=1$ cada una); la acción 2 pudo salir del desempate greedy o del caso ε.
- **$t=4$: posiblemente.** La 2 era greedy estricta; pudo ser selección greedy *o* que el ε cayera justo en la greedy.
- **$t=5$: definitivamente.** La 2 era estrictamente greedy ($1.67$) y se eligió la 3 → solo pudo salir del caso ε.

**Respuesta:** *definitivamente* en los pasos **2 y 5**; *posiblemente* en los pasos **1, 3 y 4**.

---

## Ejercicio 2.3 — Greedy vs. ε-greedy a largo plazo

> **Exercise 2.3** In the comparison shown in Figure 2.2, which method will perform best in the long run in terms of cumulative reward and probability of selecting the best action? How much better will it be? Express your answer quantitatively.

### Respuesta

**A largo plazo gana ε = 0.01** en ambas métricas; luego ε = 0.1; el greedy puro es el peor porque se queda clavado en la acción que tuvo mejor suerte en sus primeras muestras (según la sección 2.3, en solo ~un tercio de las tareas encontró la óptima).

**Probabilidad de seleccionar la acción óptima (cuantitativo).** Con *sample averages* todas las $Q_t(a) \to q_*(a)$, así que asintóticamente la greedy *es* la óptima. Para un ε-greedy con $k=10$:

$$P(\text{óptima}) = 1 - \varepsilon + \frac{\varepsilon}{k} = 1 - 0.9\,\varepsilon$$

- $\varepsilon = 0.1$: $1 - 0.09 = \mathbf{0.91}$ (nunca pasa del 91%, como dice la sección 2.3)
- $\varepsilon = 0.01$: $1 - 0.009 = \mathbf{0.991}$
- greedy: no converge a nada garantizado; se estanca en $\approx 0.35$ (lo que sus primeras muestras le permitieron)

Diferencia $\varepsilon=0.01$ vs. $\varepsilon=0.1$: **0.081** más de probabilidad de elegir la óptima.

**Recompensa (cuantitativo).** En el testbed, $q_*(\text{óptima}) \approx 1.54$ (esperanza del máximo de 10 variables $N(0,1)$) y el promedio de las subóptimas $\approx -0.17$ (la suma de las 10 vale 0 en esperanza). La recompensa esperada asintótica de un ε-greedy es:

$$\bar q \approx 1.54 - \varepsilon(1 - 1/k)\,(1.54 + 0.17) \approx 1.54 - 1.54\,\varepsilon$$

- $\varepsilon = 0.1$: $\approx \mathbf{1.39}$ por paso
- $\varepsilon = 0.01$: $\approx \mathbf{1.53}$ por paso
- greedy: se estanca cerca de $\approx 1.0$ (promedio de la figura 2.2)

**Cuánto mejor:** ε = 0.01 le gana a ε = 0.1 por $\approx 0.14$ de recompensa por paso — unas **~140 unidades de recompensa acumulada** en 1000 pasos — y le gana al greedy por $\approx 0.5$ por paso (~500 acumuladas). La contrapartida es que ε = 0.01 tarda mucho más en descubrir la óptima: gana *a largo plazo*, no al principio.

---

## Ejercicio 2.4 — Pesos de un step-size variable

> **Exercise 2.4** If the step-size parameters, $\alpha_n$, are not constant, then the estimate $Q_n$ is a weighted average of previously received rewards with a weighting different from that given by (2.6). What is the weighting on each prior reward for the general case, analogous to (2.6), in terms of the sequence of step-size parameters?

### Respuesta

Partimos de la regla general de actualización incremental (ec. 2.4) aplicada $n$ veces:

$$Q_{n+1} = Q_n + \alpha_n\,[\,R_n - Q_n\,] = (1-\alpha_n)\,Q_n + \alpha_n\,R_n$$

Desarrollando recursivamente (sustituyendo $Q_n$ por su propia expresión, etc.):

$$\boxed{\,Q_{n+1} = \Big[\prod_{j=1}^{n}(1-\alpha_j)\Big] Q_1 \;+\; \sum_{i=1}^{n} \Big[\alpha_i \prod_{j=i+1}^{n}(1-\alpha_j)\Big] R_i\,}$$

Es decir, el peso de la recompensa $R_i$ es:

$$w_i^{(n)} = \alpha_i \prod_{j=i+1}^{n}(1-\alpha_j)$$

y el peso de la estimación inicial $Q_1$ es $w_0^{(n)} = \prod_{j=1}^{n}(1-\alpha_j)$.

**Verificación con los casos conocidos:**
- **Step-size constante** ($\alpha_j = \alpha$): $w_i = \alpha(1-\alpha)^{n-i}$ y $w_0 = (1-\alpha)^n$ → exactamente la ec. (2.6) (promedio ponderado por recencia exponencial).
- **Sample average** ($\alpha_j = 1/j$): $\prod_{j=i+1}^{n}(1-\tfrac1j) = \tfrac{i}{n}$, luego $w_i = \tfrac1i\cdot\tfrac{i}{n} = \tfrac1n$ → todos los pesos iguales, como corresponde a un promedio simple, y $w_0 = 0$ (la estimación inicial se borra).

La suma de pesos siempre es 1 (se puede probar por inducción), así que sigue siendo un promedio ponderado.

---

## Ejercicio 2.5 — (programming) No estacionario

> **Exercise 2.5 (programming)** Design and conduct an experiment to demonstrate the difficulties that sample-average methods have for nonstationary problems. Use a modified version of the 10-armed testbed in which all the *q*\*(*a*) start out equal and then take independent random walks (say by adding a normally distributed increment with mean zero and standard deviation 0.01 to all the *q*\*(*a*) on each step). Prepare plots like Figure 2.2 for an action-value method using sample averages, incrementally computed, and another action-value method using a constant step-size parameter, *α* = 0.1. Use *ε* = 0.1 and longer runs, say of 10,000 steps.

### Respuesta

*(Respuesta conceptual: diseño del experimento y resultado esperado.)*

**Diseño del experimento**

1. **Entorno:** 10-armed testbed modificado. En cada paso, *antes* de elegir acción, a cada $q_*(a)$ se le suma un incremento $N(0, 0.01^2)$ independiente (random walk). Todas arrancan iguales (p. ej. $q_*(a)=0$), de modo que no hay ventaja inicial artificial para ninguna acción. La recompensa sigue siendo $R_t \sim N(q_*(A_t), 1)$.
2. **Métodos a comparar:** ambos ε-greedy con $\varepsilon = 0.1$; uno con *sample average* incremental ($\alpha_n = 1/n$) y otro con $\alpha = 0.1$ constante. Inicialización $Q_1(a)=0$.
3. **Protocolo:** 2000 runs × 10.000 pasos (runs más largos que los 1000 del testbed original, porque el random walk acumula desviación $\sqrt{t}\cdot0.01$ — a 10.000 pasos, $\sigma \approx 1$, del mismo orden que la señal). Gráficos análogos a la figura 2.2: recompensa media por paso y probabilidad de seleccionar la acción óptima *en ese paso* (óptima definida con los $q_*(t)$ vigentes, no con los iniciales).

**Resultado esperado (por qué sample average falla)**

- El promedio muestral le da **el mismo peso a todas las recompensas pasadas**, incluidas las viejas que corresponden a valores de $q_*$ que ya no existen. Con varianza creciente del random walk, $Q_t(a)$ es esencialmente un promedio de una historia que ya no describe el presente → **lag severo**: la estimación persigue al valor verdadero con un retraso enorme y la acción "óptima" identificada es frequentemente la óptima *hace muchos pasos*. La curva de probabilidad de óptima queda plana y baja (típicamente muy por debajo del nivel que alcanza en el testbed estacionario).
- Con $\alpha = 0.1$ constante, los pesos decaen exponencialmente: solo las ~últimas $1/\alpha = 10$ recompensas importan → las estimaciones **siguen** el random walk con poco retraso. La curva se mantiene alta y estable (~0.9 de probabilidad de óptima, del order del $1-0.9\varepsilon$).
- **Recompensa media:** el método de $\alpha=0.1$ claramente superior durante casi toda la ejecución; el sample average arranca igual (ambos en 0, sin información) y nunca cierra la brecha.

**Conexión con la teoría (ec. 2.7):** el sample average cumple $\sum\alpha_n = \infty$, $\sum\alpha_n^2 < \infty$ y converge — pero a un valor que es el promedio histórico, inútil aquí; el $\alpha$ constante viola la segunda condición, *no* converge, y por eso mismo logra el seguimiento deseado. Este es exactamente el argumento de la sección 2.5: la no estacionariedad es el caso típico en RL.

---

## Ejercicio 2.6 — Mysterious Spikes

> **Exercise 2.6: Mysterious Spikes** The results shown in Figure 2.3 should be quite reliable because they are averages over 2000 individual, randomly chosen 10-armed bandit tasks. Why, then, are there oscillations and spikes in the early part of the curve for the optimistic method? In other words, what might make this method perform particularly better or worse, on average, on particular early steps?

### Respuesta

La clave: **aunque las 2000 tareas sean distintas, la dinámica determinista del truco optimista es casi idéntica en todas**, así que sus efectos se alinean entre runs y sobreviven al promediado (no se cancelan como el ruido de las tareas).

**Mecanismo:**

1. **Arranque simétrico.** Todas las acciones empiezan en $Q_1(a) = +5$, idénticas. El greedy no tiene preferencia → desempate aleatorio. Las primeras ~10 jugadas prueban cada acción (o casi) una vez, y como las recompensas son $N(0,1)$, todas las estimaciones bajan de +5 a $\approx 4.5$ **más o menos al mismo ritmo** ($\alpha=0.1$ las mueve parejo). Mientras las diferencias entre estimaciones sean más chicas que el ruido, el orden greedy es básicamente **"la que hace más tiempo que no se elige"**: una acción elegida baja ($4.5 \to \approx 4.15$ con su siguiente muestra), pasa a estar por debajo de las no elegidas (que se quedaron en $4.5$), y le toca el turno a otra. Se produce un **ciclo quasi-periódico de rotación** entre acciones.

2. **Por qué sobrevive al promedio sobre 2000 tareas:** el ciclo está gobernado por la aritmética del descuento ($5 \to 4.5 \to 4.05 \dots$) y por el desempate aleatorio, no por los valores reales de cada tarea. En todos los runs el mismo patrón de "quién lleva el turno" ocurre aproximadamente en los mismos pasos → las oscillaciones de recompensa media se **suman** en lugar de cancelarse. Las tareas aleatorias solo modularan la amplitud.

3. **Por qué en pasos tempranos y por qué picos.** Al inicio el orden de selección lo domina el *turno* (mecánico), no la calidad real de las acciones → la recompensa media oscila arriba/abajo según si en ese paso el turno coincide o no con acciones buenas. A medida que las estimaciones se alejan de +5 y las diferencias reales $q_*(a)$ empiezan a pesar más que el sesgo de "quién fue muestreado cuándo", el ciclo se rompe, el greedy se estabiliza en la acción realmente óptima y la curva se suaviza en su nivel alto. Es decir: los picos son la **transición entre el régimen mecánico (turno entre estimaciones casi empatadas) y el régimen guiado por la calidad real**.

**Corolario:** es la misma razón por la que el optimismo es un *trick* de exploración temporal: explota la simetría inicial para forzar la exploración de todas las acciones, y ese forcejoe simétrico es lo que vemos como oscilación.

---

## Ejercicio 2.7 — Unbiased Constant-Step-Size Trick

> **Exercise 2.7: Unbiased Constant-Step-Size Trick** In most of this chapter we have used sample averages to estimate action values because sample averages do not produce the initial bias that constant step sizes do (see the analysis in (2.6)). However, sample averages are not a completely satisfactory solution because they may perform poorly on nonstationary problems. Is it possible to avoid the bias of constant step sizes while retaining their advantages on nonstationary problems? One way is to use a step size of
> $$\alpha_n = \frac{\alpha}{o_n}$$
> to process the *n*th reward for a particular action, where *α* > 0 is a conventional constant step size, and $o_n$ is a trace of one that starts at 0: $o_0 = 0$, $o_n = o_{n-1} + \alpha(1 - o_{n-1})$. Carry out an analysis like that in (2.6) to show that $Q_n$ is an exponential recency-weighted average *without initial bias*.

### Respuesta

**El truco:** en vez de $\alpha_n = \alpha$ constante, usar

$$\alpha_n = \frac{\alpha}{o_n}, \qquad o_0 = 0,\quad o_n = o_{n-1} + \alpha(1 - o_{n-1})$$

**1. Que los pesos sumen 1 (promedio bien definido).** La recurrencia de $o_n$ se resuelve en forma cerrada:

$$o_n = 1 - (1-\alpha)^n$$

Aplicando la forma general del ejercicio 2.4, los pesos sobre las recompensas son $w_i = \alpha_i\prod_{j>i}(1-\alpha_j)$ con $\alpha_j = \alpha/o_j$. Un chequeo numérico con $\alpha=0.1$ y $n=5$ da pesos $\approx (0.160,\,0.178,\,0.198,\,0.220,\,0.244)$, que suman 1: **los pesos se renormalizan solos**. En general $\sum_{i=1}^n w_i = 1$ (se demuestra por inducción usando que $1-\alpha_n = 1-\alpha/o_n$ y la recurrencia de $o_n$).

**2. Que no haya sesgo inicial (lo "unbiased").** Como $o_1 = \alpha$, resulta $\alpha_1 = \alpha/\alpha = 1$, o sea:

$$Q_2 = Q_1 + 1\cdot[R_1 - Q_1] = R_1$$

La primera recompensa **borra por completo** la estimación inicial: el peso de $Q_1$ es $\prod_j (1-\alpha_j) = 0$. En cambio, con $\alpha$ constante el peso de $Q_1$ es $(1-\alpha)^n > 0$ para todo $n$ (ec. 2.6): el sesgo inicial decae pero nunca desaparece.

**3. Que conserve la ventaja no estacionaria.** $o_n \to 1$ cuando $n$ crece, luego $\alpha_n = \alpha/o_n \to \alpha$. El paso efectivo **no** decae como $1/n$ (que es lo que mata al sample average en problemas no estacionarios): se estabiliza en la constante $\alpha$, con lo que las estimaciones siguen dando preponderancia a las recompensas recientes.

**Síntesis:** el truco logra lo mejor de ambos mundos — paso inicial $\alpha_1=1$ que elimina la estimación inicial (cero sesgo), pesos que siempre suman 1, y paso asintótico $\alpha$ constante que mantiene el tracking. Es el mismo espíritu que la familia de condiciones (2.7), pero sin el costo de convergencia lentísima.

---

## Ejercicio 2.8 — UCB Spikes

> **Exercise 2.8: UCB Spikes** In Figure 2.4 the UCB algorithm shows a distinct spike in performance on the 11th step. Why is this? Note that for your answer to be fully satisfactory it must explain both why the reward increases on the 11th step and why it decreases on the subsequent steps. Hint: if *c* = 1, then the spike is less prominent.

### Respuesta

Con $k=10$: en los pasos 1 a 10, UCB siempre prefiere las acciones con $N_t(a)=0$ (se las considera maximizadoras), así que **cada acción se prueba exactamente una vez** y al llegar a $t=11$ todas tienen $N=1$.

**Por qué sube en el paso 11:**

- En $t=11$, el término de exploración $c\sqrt{\ln t / N_t(a)}$ es **idéntico para las 10 acciones** (mismo $t$, mismo $N=1$). El bonus no desempata nada → UCB elige puramente $\arg\max_a Q_{11}(a)$, es decir, la acción con **mayor valor estimado basado en una sola muestra ruidosa**.
- Elegir el máximo entre 10 muestras ruidosas tiene un **efecto de selección transversal**: el ganador es la acción que tuvo la mejor *combinación* de valor real + suerte. En esperanza, $E[q_*(\text{argmax de } q_*+\text{ruido})]$ está claramente por encima de la media (y suele ser la óptima real), porque el ruido positivo correlaciona la muestra alta con valores reales altos. La recompensa fresca de ese paso refleja el valor real del ganador → **pico**.

**Por qué baja en los pasos siguientes:**

1. **Regresión a la media.** La muestra del paso 11 era *inflada* (fue elegida justamente por ser la máxima). Su segunda muestra, al ser fresca, tira el estimado $Q$ hacia el valor real del ganador — que es bueno, pero no tanto como decía el pico de una muestra. El estimado cae.
2. **El bonus recomparte.** El ganador pasa a $N=2$, con bonus $/\sqrt{2}$, mientras que las demás acciones tienen $N=1$ y bonus grande. UCB se va rotando por las acciones restantes.
3. **Selección descendente.** Las acciones restantes van siendo elegidas ordenadas por sus (infladas) muestras únicas, de mayor a menor. Cada recompensa fresca refleja el valor real de la acción en esa posición del ranking → la curva **desciende escalonadamente** desde el pico hasta que el bonus $N$-creciente equilibra todo y comienza la subida suave normal de aprendizaje.

**El hint ($c=1$ → pico menos prominente):** con $c$ chico, el término greedy domina antes: en el paso 12 el ganador del paso 11 suele seguir siendo el $\arg\max$ (su ventaja en $Q$ supera al bonus ajeno de $\approx 0.45c$), así que UCB lo **re-elige** en vez de caminar por el ranking. Como el paso 12 da una recompensa fresca de la misma acción buena que el paso 11, no hay caída pronunciada → el "pico" (subida y baja) se achata. Con $c$ grande, la rotación por acciones con $N=1$ hace que cada paso siguiente descienda por el ranking → pico marcado.

---

## Ejercicio 2.9 — Soft-max con dos acciones

> **Exercise 2.9** Show that in the case of two actions, the soft-max distribution is the same as that given by the logistic, or sigmoid, function often used in statistics and artificial neural networks.

### Respuesta

La soft-max (ec. 2.9) con $k=2$:

$$\pi(1) = \frac{e^{H(1)}}{e^{H(1)} + e^{H(2)}}$$

Dividí numerador y denominador por $e^{H(1)}$:

$$\pi(1) = \frac{1}{1 + e^{H(2)-H(1)}} = \frac{1}{1 + e^{-\,[\,H(1)-H(2)\,]}} = \sigma\big(H(1)-H(2)\big)$$

y análogamente $\pi(2) = \sigma\big(H(2)-H(1)\big) = 1 - \pi(1)$, donde

$$\sigma(x) = \frac{1}{1+e^{-x}}$$

es exactamente la **función logística/sigmoide** de la estadística y las redes neuronales.

**Interpretación:** con dos acciones solo importa la **diferencia de preferencias** $\Delta H = H(1)-H(2)$: si $\Delta H = 0$, $\sigma(0) = 0.5$ (equiprobables); $\Delta H \to +\infty$ implica $\pi(1)\to 1$. La elección de referencia (sumar una constante a ambas preferencias no cambia $\Delta H$) coincide con la invariancia de la soft-max ya señalada en la sección 2.8. El gradient bandit queda así: dos acciones $\leftrightarrow$ una sola preferencia relativa $\Delta H$ que se empuja con un gradiente escalar, análogo a un neurón de salida con activación sigmoide.

---

## Ejercicio 2.10 — Associative search

> **Exercise 2.10** Suppose you face a 2-armed bandit task whose true action values change randomly from time step to time step. Specifically, suppose that, for any time step, the true values of actions 1 and 2 are respectively 0.1 and 0.2 with probability 0.5 (case A), and 0.9 and 0.8 with probability 0.5 (case B). If you are not able to tell which case you face at any step, what is the best expectation of success you can achieve and how should you behave to achieve it? Now suppose that on each step you are told whether you are facing case A or case B (although you still don't know the true action values). This is an associative search task. What is the best expectation of success you can achieve in this task, and how should you behave to achieve it?

### Respuesta

**Caso 1 — sin pista (bandit puro no estacionario).** Cada paso el caso es A o B con prob. 0.5 y no hay forma de distinguirlo. Los valores esperados de cada acción, marginalizando sobre el caso:

$$\mathbb{E}[q(1)] = 0.5(0.1) + 0.5(0.9) = 0.5 \qquad \mathbb{E}[q(2)] = 0.5(0.2) + 0.5(0.8) = 0.5$$

Las dos acciones tienen **exactamente el mismo valor esperado**, así que ninguna política (fija o aleatoria) supera $0.5$. Toda estrategia es equivalente: siempre 1, siempre 2, o cualquier mezcla.

- **Mejor expectativa: 0.5** de recompensa por paso, alcanzada por *cualquier* comportamiento. No hay nada que aprender — es un bandit no estacionario sin señal, donde los métodos de la sección 2.5 no pueden ganar nada.

**Caso 2 — con pista (associative search / contextual bandit).** Ahora la situación es observable: hay dos "contextos" (A y B) y hay que aprender una **política contexto → acción**:

- en el contexto **A** → elegir la acción **2** (0.2 > 0.1)
- en el contexto **B** → elegir la acción **1** (0.9 > 0.8)

$$\mathbb{E}[\text{recompensa}] = 0.5(0.2) + 0.5(0.9) = \boxed{0.55}$$

**Lectura (por qué importa):** la pista *contextual* vale **+0.05** de recompensa esperada por paso (0.55 vs 0.50). Es el ejemplo mínimo de que **aprender a asociar acciones a situaciones paga**, incluso cuando cada acción solo afecta la recompensa inmediata. Notar que la mejor acción *cambia* con el caso: sin contexto, cualquier política fija es igual de buena; con contexto, hace falta una política $s \mapsto a$ — exactamente el puente entre el bandit clásico (secc. 2.1–2.8) y el RL completo (cap. 3), donde además las acciones afectarían la situación siguiente.

---

## Ejercicio 2.11 — (programming) Parameter study no estacionario

> **Exercise 2.11 (programming)** Make a figure analogous to Figure 2.6 for the nonstationary case outlined in Exercise 2.5. Include the constant-step-size *ε*-greedy algorithm with *α* = 0.1. Use runs of 200,000 steps and, as a performance measure for each algorithm and parameter setting, use the average reward over the last 100,000 steps.

### Respuesta

*(Respuesta conceptual: diseño del experimento y resultado esperado.)*

**Diseño del experimento**

1. **Entorno:** el testbed no estacionario del ejercicio 2.5 ($q_*(a)$ con random walks $N(0,0.01^2)$ por paso).
2. **Métodos y parámetros:** las variantes del capítulo 2 con sus *parameter studies* — ε-greedy con sample average (variando $\varepsilon$), ε-greedy con $\alpha=0.1$ constante (variando $\varepsilon$), optimistic greedy ($Q_1=+5$, variando... el valor inicial o $\alpha$), gradient bandit (variando $\alpha$), UCB (variando $c$). Cada parámetro variado por factores de 2 en escala log, como en la figura 2.6.
3. **Métrica:** runs de 200.000 pasos, promediando la recompensa **solo sobre los últimos 100.000** (descartamos el transitorio inicial para medir el *steady state* de tracking, no el arranque). Cada punto del gráfico = promedio sobre los runs.

**Resultado esperado**

- **Todos los métodos con sample average rinden mal**, con cualquier $\varepsilon$: sus curvas quedan planas y bajas en el fondo del gráfico, porque promediar toda la historia es inútil frente al random walk. Es el punto central del ejercicio.
- **Las variantes con $\alpha$ constante dominan**, con curvas en U invertida típica respecto de $\varepsilon$: muy poco $\varepsilon$ → no alcanza a seguir las acciones que se volvieron óptimas; demasiado $\varepsilon$ → gasta recompensa explorando de más. El óptimo anda por $\varepsilon$ chico/intermedio ($\approx 0.01$–$0.1$) y $\alpha \approx 0.1$.
- **Optimistic initial values no aportan** (su impulso explorador ocurre solo al comienzo, que además está descartado por la métrica); **UCB pierde su ventaja** o directamente no compite, porque su bonus $\sqrt{\ln t/N}$ asume estacionariedad (el bonus decrece con $t$ aunque $q_*$ siga cambiando) — la limitación ya señalada en la sección 2.7.
- **Gradient bandit con $\alpha$ constante** compite razonablemente, con su característica U invertida respecto del $\alpha$.
- **Moraleja general:** en un problema no estacionario el *ranking* de métodos se invierte respecto de la figura 2.6: lo que gana es el que puede **olvidar** (constante $\alpha$ o explícitamente no-estacionario), no el que acumula evidencia indefinidamente.

---

## Ideas clave del capítulo (link con los ejercicios)

- **Feedback evaluativo vs. instructivo:** 2.1–2.3 practican la mecánica básica de elegir bajo incertidumbre sin instrucción de la acción correcta; es la esencia que distingue al RL.
- **Regla general `NewEstimate ← OldEstimate + StepSize[Target − OldEstimate]`:** aparece en 2.2, 2.4, 2.5 y 2.7, y es la misma estructura que la actualización TD del **cap. 1** (secc. 1.5) y de todo el libro.
- **Estacionariedad como supuesto oculto:** 2.4, 2.5, 2.7, 2.11 son todos sobre cuándo ese supuesto se rompe — el caso *típico* en RL, no la excepción.
- **Sesgo vs. varianza y valor inicial:** 2.6 y 2.7 son dos caras del mismo problema (el $Q_1$ como parámetro que hay que elegir).
- **Exploración dirigida vs. aleatoria:** UCB (2.8) explora por incertidumbre; optimistic values (2.6) por decepción temporal; ε-greedy (2.1–2.3) por azar — los tres caminos del capítulo.
- **Del bandit al RL completo:** 2.10 muestra que basta una *pista* del contexto para que aparezca el aprendizaje de políticas — el puente hacia MDPs (**cap. 3**), y los métodos de este capítulo reaparecen como subrutinas desde el **cap. 5**.
