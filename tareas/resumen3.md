# Tarea 3 — Finite Markov Decision Processes (Capítulo 3)

**Fuente:** Sutton & Barto, *Reinforcement Learning: An Introduction* (2da ed.), **Capítulo 3** (Finite Markov Decision Processes).

> **Aclaración:** el capítulo 3 es el formal: convierte en matemática la intuición del capítulo 1. Define los MDP finitos (agente–entorno, dinámica $p$, retornos, funciones de valor y ecuaciones de Bellman), presenta el marco unificado para tareas episódicas y continuas, y cierra con las políticas óptimas y la discusión práctico-teórica de la optimalidad. Secciones: 3.1 *agent–environment interface*, 3.2 *goals and rewards*, 3.3 *returns and episodes*, 3.4 *unified notation*, 3.5 *policies and value functions*, 3.6 *optimal policies and optimal value functions*, 3.7 *optimality and approximation* y 3.8 *summary*.

**Índice**

1. Encuadre: qué es un MDP (en 30 segundos)
2. (3.1) The Agent–Environment Interface
3. (3.2) Goals and Rewards
4. (3.3) Returns and Episodes
5. (3.4) Unified Notation for Episodic and Continuing Tasks
6. (3.5) Policies and Value Functions
7. (3.6) Optimal Policies and Optimal Value Functions
8. (3.7) Optimality and Approximation
9. (3.8) Summary
10. Cómo se conecta con los capítulos 1, 2 y 4

---

## Encuadre: qué es un MDP (en 30 segundos)

Un *proceso de decisión de Markov* es la formalización de un problema de decisión secuencial: un **agente** observa un **estado** $S_t$, elige una **acción** $A_t$, recibe una **recompensa** $R_{t+1}$ y pasa a un nuevo estado $S_{t+1}$, una y otra vez:

$$
S_0 \rightarrow A_0 \rightarrow R_1, \; S_1 \rightarrow A_1 \rightarrow R_2, \; S_2 \rightarrow A_2 \rightarrow R_3, \ldots \tag{3.1}
$$

Lo que hace "de Markov" al proceso es que la dinámica se resume en $p(s', r \mid s, a)$: la probabilidad de llegar a $s'$ y cobrar $r$ depende **solo** del estado y acción actuales, no de todo el pasado. Mientras que en el cap. 2 estimábamos $q_*(a)$ por acción, en los MDP estimamos valores por **estado y acción** $q_*(s, a)$ o $v_*(s)$: hay *reward delay* y la necesidad de *trade-off* entre recompensa inmediata y futura. Un MDP es la versión matemáticamente idealizada del problema de RL, para la cual se pueden hacer afirmaciones teóricas precisas.

---

## (3.1) — The Agent–Environment Interface

**Qué representa:** la definición del problema. El **agente** es el aprendiz y tomador de decisiones; el **entorno** es todo lo demás. Interactúan en pasos de tiempo discretos $t = 0, 1, 2, \ldots$: en cada paso el agente recibe el estado $S_t \in \mathcal{S}$, elige $A_t \in \mathcal{A}(s)$, y un paso después recibe $R_{t+1} \in \mathcal{R} \subset \mathbb{R}$ y el nuevo estado $S_{t+1}$. En un *MDP finito* los conjuntos $\mathcal{S}$, $\mathcal{A}$ y $\mathcal{R}$ son finitos y las variables $R_t$ y $S_t$ tienen distribuciones de probabilidad discretas bien definidas según el estado y la acción previos:

$$
p(s', r \mid s, a) \doteq \Pr\{ S_t = s', R_t = r \mid S_{t-1} = s, A_{t-1} = a \} \tag{3.2}
$$

La función $p$ define la **dinámica** del MDP (es una función determinista ordinaria de cuatro argumentos hacia $[0,1]$). Naturalmente debe sumar 1 en cada $(s,a)$:

$$
\sum_{s' \in \mathcal{S}} \sum_{r \in \mathcal{R}} p(s', r \mid s, a) = 1 \qquad \text{para todo } s \in \mathcal{S}, a \in \mathcal{A}(s) \tag{3.3}
$$

**De $p$ se deriva todo lo demás:**
- **Probabilidades de transición** (tres argumentos):
$$
p(s' \mid s, a) \doteq \Pr\{ S_t = s' \mid S_{t-1} = s, A_{t-1} = a \} = \sum_{r \in \mathcal{R}} p(s', r \mid s, a) \tag{3.4}
$$
- **Recompensa esperada** de un par estado–acción (dos argumentos):
$$
r(s, a) \doteq \mathbb{E}[\, R_t \mid S_{t-1} = s, A_{t-1} = a \,] = \sum_{r \in \mathcal{R}} r \sum_{s' \in \mathcal{S}} p(s', r \mid s, a) \tag{3.5}
$$
- **Recompensa esperada** de una tripla estado–acción–estado siguiente (tres argumentos):
$$
r(s, a, s') \doteq \mathbb{E}[\, R_t \mid S_{t-1} = s, A_{t-1} = a, S_t = s' \,] = \sum_{r \in \mathcal{R}} r\, \frac{p(s', r \mid s, a)}{p(s' \mid s, a)} \tag{3.6}
$$

**Idea high-level:**
- **La propiedad de Markov es una restricción sobre el *estado*, no sobre el proceso:** el estado debe incluir toda la información del pasado que haga *diferencia para el futuro*. El libro la asume en todo el libro (y discute construir estados Markov en el cap. 17).
- **Flexibilidad del marco:** los pasos no son necesariamente intervalos de tiempo real; las acciones pueden ser de bajo nivel (voltajes de motores) o alto nivel (ir a almorzar, estudiar); los estados pueden ser sensoriales, simbólicos, mentales o subjetivos. Toda información que sea útil para decidir puede ser un estado.
- **El límite agente–entorno no es el límite físico:** se dibuja *más cerca del agente*: los músculos, motores y sensores suelen ser parte del entorno. La regla es: *todo lo que el agente no puede cambiar arbitrariamente es entorno*. El límite representa el límite del **control absoluto**, no del conocimiento (podés saber todo sobre el entorno — como un cubo de Rubik — y aun así la tarea ser difícil).

**Ejemplos del libro:**
- **Ej. 3.1 (Bioreactor):** acciones = temperaturas y velocidades de agitado objetivo; estados = lecturas de sensores + insumos simbólicos; recompensas = tasa de producción del químico útil. Típico: estados y acciones con representaciones *estructuradas* (vectores), recompensas siempre un número.
- **Ej. 3.3 (Recycling Robot):** un robot junta latas; estado = nivel de batería (solo `high` / `low`). En `high` solo puede `search` o `wait`; en `low`, también `recharge`. Recompensa: +1 por lata, −3 si se le agota la batería (lo rescatan). La dinámica queda tabulada en probabilidades de transición y retornos esperados, o como un **transition graph** (nodos de estado y de acción; las flechas que salen de un nodo acción suman 1).
- **Ejercicios 3.3 (¿dónde trazar el límite conduciendo?), 3.4 (escribir $p(s',r|s,a)$ para el robot).**

---

## (3.2) — Goals and Rewards

**Qué representa:** la formalización del objetivo. En cada paso el entorno manda un número simple $R_t$; el objetivo informal del agente es **maximizar la recompensa acumulada a largo plazo**, no la inmediata. Esto se resume en la *reward hypothesis*:

> **Reward hypothesis:** todo lo que queremos significar con "objetivos y propósitos" puede pensarse como la **maximización del valor esperado de la suma acumulada de una señal escalar recibida (la recompensa)**.

**Ejemplos de cómo se usan las recompensas:** caminar → proporcional al avance hacia adelante; escapar de un laberinto → −1 por cada paso previo a escapar (fomenta rapidez); reciclador → 0 la mayor parte del tiempo y +1 por lata; ajedrez → +1 ganar, −1 perder, 0 tablas y posiciones no terminales.

**Idea high-level (la regla de oro del diseño de recompensas):** el agente siempre maximiza lo que le defines. La señal de recompensa comunica **qué** quieres que logre, *no cómo*. Si la usás para inculcar conocimiento previo (subobjetivos), el agente puede encontrar una manera de cumplir el subobjetivo sin el objetivo real — p. ej., premiar capturar piezas en ajedrez lleva a un agente que captura piezas y pierde la partida. Es crítico que la recompensa indique **verdaderamente** lo que se quiere lograr.

---

## (3.3) — Returns and Episodes

**Qué representa:** formalizar "maximizar la recompensa a largo plazo". Se busca maximizar la **esperanza del retorno** $G_t = $ alguna función específica de la secuencia de recompensas. Hay dos casos según la tarea:

- **Tareas episódicas:** la interacción se rompe naturalmente en **episodios** (partidas, laberintos, interacciones repetidas). Cada episodio termina en un **estado terminal**, seguido de un *reset* a un estado inicial estándar. Se distingue $\mathcal{S}$ (estados no terminales) de $\mathcal{S}^+$ (todos + terminal). El retorno es la suma simple:
$$
G_t \doteq R_{t+1} + R_{t+2} + \cdots + R_T \tag{3.7}
$$
donde $T$ es un paso final (variable aleatoria que cambia de episodio a episodio). *Analogía:* es el marcador de una partida — en ajedrez, $G_t = +1$ (gané), −1 (perdí), o 0 (tablas).

- **Tareas continuas:** la interacción no se rompe en episodios (control de procesos, robot de vida larga). Con $T = \infty$, la suma (3.7) podría ser infinita. La solución es el **descuento**:
$$
G_t \doteq \sum_{k=0}^{\infty} \gamma^k R_{t+k+1} \tag{3.8}
$$
donde $0 \leq \gamma \leq 1$ es la **discount rate**: una recompensa a $k$ pasos vale solo $\gamma^{k-1}$ veces lo que valdría hoy. Si $\gamma < 1$ y las recompensas son acotadas, la suma converge. *Analogía financiera:* $100$ pesos el año que viene no valen $100$ hoy; valen $100\gamma$.

**Idea high-level sobre $\gamma$:**
- $\gamma = 0$ → agente **"miope"**: solo maximiza $R_{t+1}$ (solo sirve si cada acción afecta solo la recompensa inmediata).
- $\gamma = 1$ → el futuro vale igual que el presente (solo válido si la suma converge, p. ej. episodios finitos).
- Valores intermedios → agente "farsighted": $\gamma = 0.9$ da peso $0.9^{10} \approx 35\%$ a una recompensa a 10 pasos.

**Retornos sucesivos (una relación clave para la teoría y los algoritmos):** para todo $t < T$ (definiendo $G_T = 0$):
$$
G_t \doteq R_{t+1} + \gamma\, G_{t+1} \tag{3.9}
$$
Es la versión "redundante" de mirar el futuro: conociendo $G_{t+1}$ y la recompensa actual, tengo $G_t$. Es la **semilla de todas las ecuaciones de Bellman**.

**Caso de recompensa constante +1:** garantiza que el retorno infinito no explota:
$$
G_t = 1 + \gamma + \gamma^2 + \cdots = \frac{1}{1-\gamma} \tag{3.10}
$$

**Ejemplo 3.4: Pole-Balancing.** Mantener un poste en equilibrio sobre un carrito. Puede tratarse como **episódico** (cada intento es un episodio; recompensa +1 por paso sin fallar → retorno = pasos hasta fallar) o **continuo con descuento** (recompensa −1 en cada falla, 0 en el resto → retorno relacionado con $-\gamma^K$, con $K$ pasos hasta fallar). **Ejercicio 3.7 (laberinto):** si el agente solo recibe +1 al escapar y 0 el resto, y no mejora — ¿le comunicaste efectivamente qué quieres? (pista: sin **señal por pasos** no hay gradiente informativo).

---

## (3.4) — Unified Notation for Episodic and Continuing Tasks

**Qué representa:** una sola notación para hablar con precisión de ambos casos a la vez.

- **Un episodio = una serie de episodios:** técnicamente se habla de $S_{t,i}$ (tiempo $t$ del episodio $i$), pero casi nunca hace falta distinguir episodios, así que se abusa de la notación escribiendo $S_t$.
- **El truco del estado absorbente:** la terminación del episodio se modela como entrar a un **estado absorbente** que solo se transita a sí mismo generando recompensas 0. Así, episódico y continuo quedan unificados: sumar los primeros $T$ retornos o la secuencia infinita (con ceros después del terminal) da lo mismo, aunque haya descuento.

**El retorno general** (una fórmula para ambos casos):
$$
G_t \doteq \sum_{k=0}^{T-t-1} \gamma^k R_{t+k+1} \tag{3.11}
$$
incluyendo la posibilidad de $T = \infty$ o $\gamma = 1$, **pero no ambos**. Es simplemente (3.7) y (3.8) fundidas en una. (Más adelante, el cap. 10 introducirá una formulación a la vez continua y sin descuento.)

---

## (3.5) — Policies and Value Functions

**Qué representa:** casi todos los algoritmos de RL estiman **funciones de valor**: funciones que estiman *qué tan bueno* es estar en un estado (o hacer una acción en un estado), en términos de **retorno esperado**. Como el retorno depende de las acciones futuras, las funciones de valor están definidas respecto a **políticas**.

**Política:** un mapeo estados → probabilidades de elegir cada acción:
$$
\pi(a \mid s) = \Pr\{ A_t = a \mid S_t = s \}
$$
Es una función ordinaria; el "$\mid$" recuerda que define una distribución sobre $a \in \mathcal{A}(s)$ para cada $s$. Los métodos de RL especifican cómo cambiar la política con la experiencia.

**Funciones de valor:**
- **Función de valor de estado** — retorno esperado arrancando en $s$ y siguiendo $\pi$:
$$
v_\pi(s) \doteq \mathbb{E}_\pi[\, G_t \mid S_t = s \,] \tag{3.12}
$$
(el valor del estado terminal, si existe, siempre es 0). *Analogía:* un "semáforo" de cada estado — cuán bueno es estar ahí *de aquí en adelante*.
- **Función de valor de acción** — retorno esperado partiendo de $s$, tomando $a$ y después siguiendo $\pi$:
$$
q_\pi(s, a) \doteq \mathbb{E}_\pi[\, G_t \mid S_t = s, A_t = a \,] \tag{3.13}
$$

**Idea high-level:** $v_\pi$ y $q_\pi$ se pueden estimar de la experiencia (promediar retornos reales = **métodos Monte Carlo**, cap. 5). Con muchos estados, se mantienen como funciones parametrizadas (Parte II).

**La ecuación de Bellman (3.14), en criollo: "lo que vale estar acá = lo que gano ahora + lo que vale donde voy a parar".** Las funciones de valor satisfacen relaciones recursivas. Para cualquier política $\pi$ y estado $s$:

$$
v_\pi(s) = \sum_a \pi(a\mid s)\, \sum_{s', r} p(s', r \mid s, a)\, \big[\, r + \gamma\, v_\pi(s') \,\big] \tag{3.14}
$$

**Traducción:** el valor de $s$ = promedio (ponderado por política y dinámica) de "lo que gano ya mismo + lo que vale el estado al que voy, descontado". Lo infinito quedó reducido a mirar un solo paso adelante; el resto lo cuenta el valor del vecino. El **backup diagram** (estado raíz → ramas de acciones → posibles $s'$) representa esta transferencia de información "hacia atrás" que está en el corazón de los métodos de RL. $v_\pi$ es la **solución única** de su ecuación de Bellman.

### Caso de juguete: gridworld 3×3 (ecuación de Bellman evaluada)

Una grilla de 3×3 (9 casillas). En cada casilla el agente mueve N, S, E u O (movimientos **deterministas**):
- Entrar a la **meta** (abajo a la derecha): **+10** y termina el episodio.
- Chocar contra una pared: te quedás donde estabas y cobrás **−1**.
- Cualquier otro movimiento: **0**.
- Descuento $\gamma = 0.9$.

Como el movimiento es determinista, cada $(s,a)$ tiene un único $(s',r)$: la $p$ vale 1 solo para ese par y 0 para el resto, así que (3.14) se encoge a

$$
v_\pi(s) = r + \gamma\, v_\pi(s')
$$

Tomemos la política determinista *"ir a la meta a lo derecho"* (E, E, S, S desde la salida). Armamos las ecuaciones de atrás hacia adelante; **cada fila es una Bellman evaluada**:

| Casilla | Muevo | $r$ | Quedo en | Cálculo | $v_\pi$ |
|---|---|---|---|---|---|
| meta | — | — | terminal | — | 0 |
| (1,2) | S | +10 | meta | $10 + 0.9 \cdot 0$ | 10 |
| (0,2) | S | 0 | (1,2) | $0 + 0.9 \cdot 10$ | 9 |
| (0,1) | E | 0 | (0,2) | $0 + 0.9 \cdot 9$ | 8.1 |
| (0,0) partida | E | 0 | (0,1) | $0 + 0.9 \cdot 8.1$ | 7.29 |

```
+---------+---------+---------+
| 7.29    | 8.1     | 9       |   ← camino: E, E, S, S
+---------+---------+---------+
|   ?     |   ?     | 10      |
+---------+---------+---------+
|   ?     |   ?     | 0 (meta)|
+---------+---------+---------+
```

**Tres cosas para llevarte:**
1. **El valor "fluye" desde la meta hacia atrás.** $v(\text{salida}) = 0.9^3 \cdot 10$: la salida vale la recompensa de la meta, **descontada por los 3 pasos que la separan** (la definición de retorno descontado, (3.8), aplicada en reversa). Bellman hace que cada estado le pase "su valor" al anterior.
2. **Cada casilla aporta una ecuación.** Las 9 casillas *todas* cumplen (3.14); la del centro depende de sus 4 vecinas y las vecinas de la del centro… se arma un **sistema de 9 ecuaciones con 9 incógnitas** cuya solución única es $v_\pi$. Eso es exactamente lo que hace el **Ejemplo 3.5 (Gridworld 5×5 del libro)**: resuelve (3.14) como sistema lineal y dibuja $v_\pi$. Ahí el estado `A` vale menos que su recompensa inmediata +10 (porque `A` te manda a `A'`, cerca del borde negativo), y `B` vale *más* que +5 (porque `B'` tiene valor positivo y quizá cae en `A`/`B`).
3. **Funciona para cualquier política… y para la mejor.** Si la política fuera aleatoria, $\sum_a \pi(a\mid s)$ vuelve a promediar las direcciones; si ponés un $\max_a$ donde estaba el promedio, obtenés la **ecuación de optimalidad de Bellman** (3.19–3.20): el valor óptimo = recompensa de la *mejor* acción + $\gamma \times$ el valor óptimo del siguiente estado.

**Ejemplo 3.6: Golf.** Penalización −1 por golpe; el valor de un estado es el *negativo del número de golpes hasta el hoyo*. Con putter hay contornos de valor −1 (green), −2, −3, … hasta el tee (6 golpes); los bunkers valen $-\infty$. Se ve cómo el valor de un estado depende de los vecinos y de la política que se use (solo putter vs. usar driver cuando conviene).

**Ejercicios destacados:** **3.14** (verificar numéricamente que el centro del gridworld, +0.7, cumple (3.14) con sus vecinos), **3.17** (la ecuación de Bellman para action values), **3.15/3.16** (sumar una constante a las recompensas: en tareas continuas con descuento no cambia los valores relativos; en episódicas *sí* puede cambiar el comportamiento).

---

## (3.6) — Optimal Policies and Optimal Value Functions

**Qué representa:** resolver un problema de RL ≈ encontrar una política que logre mucha recompensa a largo plazo. Las funciones de valor definen un **orden parcial** sobre políticas: $\pi \geq \pi' \iff v_\pi(s) \geq v_{\pi'}(s)$ para todo $s \in \mathcal{S}$. Siempre existe **al menos una política óptima** ($\pi_*$; puede haber varias). Todas comparten la **función de valor óptima** $v_*$ y la **función de valor de acción óptima** $q_*$:

$$
v_*(s) \doteq \max_{\pi} v_\pi(s) \qquad \text{para todo } s \in \mathcal{S} \tag{3.15}
$$

$$
q_*(s, a) \doteq \max_{\pi} q_\pi(s, a) \qquad \text{para todo } s, a \tag{3.16}
$$

$q_*$ se escribe en términos de $v_*$ (retorno esperado tomando $a$ en $s$ y luego siguiendo una política óptima):
$$
q_*(s, a) = \mathbb{E}[\, R_{t+1} + \gamma\, v_*(S_{t+1}) \mid S_t = s, A_t = a \,] \tag{3.17}
$$

**La ecuación de optimalidad de Bellman.** Como $v_*$ es la función de valor de una política, cumple su Bellman; y por ser *óptima*, su condición de consistencia se escribe sin referencia a ninguna política: el valor de un estado bajo una política óptima debe igualar el retorno esperado de la **mejor acción** desde ese estado:

$$
v_*(s) = \max_{a \in \mathcal{A}(s)} \mathbb{E}[\, R_{t+1} + \gamma\, v_*(S_{t+1}) \mid S_t = s, A_t = a \,] \tag{3.18}
$$

$$
v_*(s) = \max_a \sum_{s', r} p(s', r \mid s, a)\, [\, r + \gamma\, v_*(s') \,] \tag{3.19}
$$

$$
q_*(s, a) = \sum_{s', r} p(s', r \mid s, a)\, \left[\, r + \gamma\, \max_{a'} q_*(s', a') \,\right] \tag{3.20}
$$

Son **sistemas de $n$ ecuaciones no lineales con $n$ incógnitas** (una por estado), con solución única para MDPs finitos. Los backup diagrams son los de $v_\pi/q_\pi$ pero con un arco extra en los puntos de elección del agente para indicar el $\max$ en vez del promedio según $\pi$.

**Idea high-level:**
- **Una vez que tenés $v_*$, es fácil obtener la política óptima:** para cada $s$ hay una o más acciones donde se alcanza el máximo en (3.19); *toda* política que asigne probabilidad no nula solo a esas acciones es óptima. Es una **búsqueda de un paso**: cualquier política **greedy respecto de $v_*$** es óptima, porque $v_*$ ya tiene internalizadas las consecuencias de todo el comportamiento futuro — convierte el retorno esperado óptimo de largo plazo en una cantidad local e inmediatamente disponible.
- **Con $q_*$ es aún más fácil:** no hace falta la búsqueda de un paso ni saber nada de las dinámicas del entorno: $q_*$ *cachea* los resultados de todas las búsquedas de un paso como una función de pares estado–acción. Basta elegir cualquier acción que maximice $q_*(s, a)$.
- **La solución exacta rara vez es útil directamente** (es como una búsqueda exhaustiva): requiere (1) conocer con precisión las dinámicas, (2) recursos computacionales suficientes y (3) la propiedad de Markov. En problemas de ~$10^{20}$ estados (backgammon), no se puede. En RL típicamente hay que **conformarse con soluciones aproximadas**.
- **Ejemplos 3.8/3.9:** resolver la optimalidad del gridworld (política óptima que maximiza $v_*$; el mejor estado vale 24.4) y del recycling robot (con 2 estados, un sistema de 2 ecuaciones no lineales con solución única para cualquier elección valida de los parámetros).

---

## (3.7) — Optimality and Approximation

**Qué representa:** la brecha entre el ideal de optimalidad y lo que se hace en la práctica. Aunque definir las funciones/políticas óptimas organiza el enfoque del libro y permite entender propiedades teóricas, es un **ideal que los agentes solo aproximan en grados variables** — incluso con un modelo completo y preciso, casi nunca se puede simplemente *computar* la política óptima (el backgammon y el ajedrez lo demuestran, con miles de años de cómputo).

**Las dos restricciones duras del problema:**
- **Cómputo disponible por paso de tiempo.**
- **Memoria disponible:** para construir aproximaciones de funciones de valor, políticas y modelos. Con conjuntos de estado pequeños y finitos se usan **tablas** (el *caso tabular*: un array con una entrada por estado o par estado–acción). Con muchos estados, las funciones deben **aproximarse** con representaciones parametrizadas compactas.

**Idea high-level — la oportunidad de la aproximación online:** muchos estados se visitan con tan baja probabilidad que tomar malas decisiones ahí impacta poco la recompensa total. El carácter **online** del RL permite **concentrar el esfuerzo de aprendizaje en los estados frecuentes** a expensas de los infrecuentes; por eso un TD-Gammon puede jugar con habilidad excepcional aunque tome malas decisiones en una fracción grande de los estados que nunca ocurren en partidas contra expertos. Esa es una propiedad clave que distingue al RL de otros enfoques de solución aproximada de MDPs.

---

## (3.8) — Summary

**Qué queda del capítulo:**

- **El problema → tres señales** que pasan entre agente y entorno: **acciones** (elecciones del agente), **estados** (base de las elecciones) y **recompensas** (base para evaluarlas). *Policy* = regla estocástica para elegir acciones como función de los estados.
- **MDP finito:** formulación con probabilidades de transición bien definidas en conjuntos finitos; gran parte de la teoría de RL se restringe ahí, aunque los métodos son más generales.
- **Retorno:** la función de recompensas futuras a maximizar (en esperanza). Sin descuento para **episódicas**, con descuento para **continuas**, unificados con la notación del estado absorbente.
- **Funciones de valor:** $v_\pi$ y $q_\pi$ asignan a cada estado (o par) el retorno esperado siguiendo la política. Las **óptimas** ($v_*, q_*$) asignan el mayor retorno alcanzable por cualquier política. Hay *una sola* terna / función de valor óptima pero **muchas políticas óptimas**; toda política **greedy respecto de las funciones de valor óptimas** es óptima.
- **Ecuaciones de optimalidad de Bellman:** condiciones de consistencia que las funciones de valor óptimas cumplen; en principio resolubles para obtener $v_*/q_*$ y de ahí una política óptima con relativa facilidad.
- **Conocimiento completo vs incompleto:** en problemas de *complete knowledge* el agente tiene un modelo completo y exacto ($p$ de (3.2)); en los de *incomplete knowledge* no. Aun con el modelo, suele faltar cómputo y memoria → **aproximaciones**. La noción de optimalidad es organizadora, pero la meta práctica es aproximar.

---

## Cómo se conecta con los capítulos 1, 2 y 4

- El **cap. 1** dio la intuición (elementos del RL, política/recompensa/valor/modelo); el **3** la convierte en matemática: MDPs, retornos, funciones de valor y Bellman — *el formalismo que el libro resuelve en el resto*.
- El **cap. 2 (bandits)** era el caso sin asociación (estimar $q_*(a)$); los MDPs agregan el aspecto **asociativo** (elegir distinto según el estado) y el **reward delay**. Los contextual bandits del 2.9 son el puente.
- El **cap. 4 (DP)** toma las ecuaciones de Bellman (3.14, 3.19, 3.20) y las convierte en **algoritmos de actualización iterativos**, asumiendo el modelo perfecto $p$; lo que el 3 define como condiciones de optimalidad, el 4 las usa como reglas de cómputo.