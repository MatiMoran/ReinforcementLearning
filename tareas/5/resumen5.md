# Tarea 5 — Monte Carlo Methods (Capítulo 5)

**Fuente:** Sutton & Barto, *Reinforcement Learning: An Introduction* (2da ed.), **Capítulo 5** (Monte Carlo Methods).

> **Aclaración:** el capítulo 5 es el primero que aprende **sin modelo** del entorno: estima funciones de valor y políticas óptimas a partir de *experiencia* (episodios muestreados), promediando **retornos completos**. La numeración de ecuaciones vuelve a empezar en (5.1). Secciones: 5.1 *MC prediction*, 5.2 *action values*, 5.3 *MC control*, 5.4 *sin exploring starts*, 5.5 *off-policy via importance sampling*, 5.6 *incremental implementation*, 5.7 *off-policy MC control*, 5.8 y 5.9 (avanzadas, opcionales) sobre importance sampling, y 5.10 el resumen.

**Índice**

1. Encuadre: aprender sin modelo
2. (5.1) Monte Carlo Prediction
3. (5.2) Monte Carlo Estimation of Action Values
4. (5.3) Monte Carlo Control
5. (5.4) Monte Carlo Control without Exploring Starts
6. (5.5) Off-policy Prediction via Importance Sampling
7. (5.6) Incremental Implementation
8. (5.7) Off-policy Monte Carlo Control
9. (5.8) Discounting-aware Importance Sampling
10. (5.9) Per-decision Importance Sampling
11. (5.10) Summary: MC vs DP
12. Cómo se conecta con los capítulos 3, 4 y 6

---

## Encuadre: aprender sin modelo

En el capítulo 4 (DP) resolvíamos el MDP asumiendo que conocemos la dinámica completa $p(s', r \mid s, a)$. Acá se suelta ese supuesto: los métodos Monte Carlo (MC) aprenden solo de **experiencia** — secuencias muestreadas de estados, acciones y recompensas de interacción real o simulada.

> **Qué comparten con DP:** el patrón *generalized policy iteration* (GPI: evaluar ⟶ mejorar ⟶ evaluar…). La diferencia: DP **computa** $v_\pi$ con el modelo; MC **aprende** $v_\pi$ promediando retornos observados.

**Idea high-level:**
- MC promedia **retornos completos** de episodios, no recompensas sueltas. Como vuelven a la media del retorno, converge a $v_\pi(s)$ por la ley de los grandes números.
- Solo sirve para **tareas episódicas** (todo episodio debe terminar); aprende de a un episodio, no paso a paso.
- Tres ventajas sobre DP: (1) aprende **sin modelo**, (2) funciona con *simulación* (basta generar episodios muestreados, aun cuando sea imposible escribir las probabilidades $p$ explícitas — ej. blackjack), (3) puede **enfocarse** en un subconjunto de estados sin evaluar el resto.

> Relación con bandits (cap. 2): MC promedia *retornos* por par estado–acción, como los bandits promedian *recompensas* por acción; la diferencia es que acá hay muchos estados acoplados (lo que pasa en uno depende de las acciones en los siguientes), y el problema es no-estacionario porque todas las decisiones van aprendiéndose a la vez.

---

## (5.1) — Monte Carlo Prediction

**Qué representa:** estimar $v_\pi(s)$, el valor de un estado bajo una política $\pi$ fija, promediando los **retornos observados tras cada visita** a $s$.

- **First-visit MC:** promedia los retornos tras la **primera** vez que se visita $s$ en cada episodio.
- **Every-visit MC:** promedia los retornos tras **todas** las visitas a $s$.

Ambos convergen a $v_\pi(s)$ al crecer el número de visitas. Para first-visit es directo: cada retorno es una estimación i.i.d. de $v_\pi(s)$ con varianza finita; la ley de los grandes números hace que el promedio converja al valor esperado (y el error cae como $1/\sqrt{n}$). (Every-visit también converge, aunque la demostración es menos directa.)

**Pseudocódigo (first-visit MC prediction):**
1. Inicializar $V(s)$ arbitrario y una lista $Returns(s)$ vacía para cada $s$.
2. Para cada episodio: generar el episodio siguiendo $\pi$.
3. Recorrerlo de atrás hacia adelante con $G \leftarrow \gamma G + R_{t+1}$.
4. Si es la primera vez que aparece el estado, agregar $G$ a sus retornos y actualizar $V(s) \leftarrow$ promedio de esos retornos.

**Idea high-level:**
- **No bootstrap:** la estimación de cada estado es independiente de las demás (no se construye sobre estimaciones de sucesores, como en DP). Por eso el costo de evaluar *un solo* estado no depende del resto — se pueden generar episodios arrancando del estado que interese.
- **Backup diagram:** el de MC muestra la **trayectoria completa** hasta el terminal (solo la muestra de un episodio), contra el de DP que muestra todas las transiciones de un solo paso. Esa diferencia gráfica refleja la diferencia algorítmica de fondo.
- En la práctica, MC necesitó 500.000 partidas para aproximar muy bien la función de valor del blackjack.

**Ejemplo 5.1: Blackjack.** Cada partida = un episodio. Recompensas +1 / −1 / 0 (ganar, perder, empatar), $\gamma = 1$ (sin descuento), por lo que la recompensa terminal *es* el retorno. Acciones: hit o stick. Estados: (suma del jugador 12–21, carta visible del dealer ace–10, tienes as usable o no) → **200 estados**. La política evaluada: *stick* solo con 20 o 21, *hit* en el resto. Aunque se conoce el juego, aplicar DP sería un dolor: hay que computar probabilidades complicadas (p. ej., la de ganar con suma 14 y stick, según la carta del dealer); en cambio generar partidas muestreadas es trivial.

**Ejercicios:** **5.1** (¿por qué los valores saltan en las últimas filas de la figura?) y **5.2** (¿cambiaría mucho usar every-visit en blackjack?).

**Ejemplo 5.2: Soap Bubble.** Calcular la altura de una burbuja de jabón con marco de alambre irregular: en superficie, la altura de cada punto es el promedio de sus vecinos. El método iterativo clásico (tipo iterative policy evaluation) ajusta cada punto hacia el promedio de sus 4 vecinos hasta converger. El **método MC**: caminatas aleatorias desde el punto de interés hasta tocar el borde; el promedio de las alturas de borde a las que llegan las caminatas aproxima la altura del punto. Si solo te importa un punto (o unos pocos), MC puede ser mucho más eficiente que el barrido local.

---

## (5.2) — Monte Carlo Estimation of Action Values

**Qué representa:** sin modelo, **$v_\pi(s)$ no alcanza** para actuar: para elegir acción necesitás mirar un paso adelante (modelo) o tener el valor de cada **par estado–acción** $q_\pi(s,a)$. Por eso el objetivo primario pasa a estimar $q_*$.

- Igual que para estados, pero ahora se habla de **visitas a pares** $(s,a)$: el par es visitado en un episodio si se tomó la acción $a$ estando en $s$. First-visit y every-visit se definen análogamente (primera vez del par en el episodio versus todas las veces) y convergen cuadráticamente.

**El problema: mantener exploración.** Si $\pi$ es determinista, cada episodio solo visita **una** acción por estado: los demás pares $(s,a)$ nunca reciben retornos y sus estimaciones nunca mejoran. Como el propósito de $q$ es *comparar acciones*, esto es un problema serio.

**Dos salidas (el capítulo desarrolla ambas):**
- **Exploring starts:** asumir que cada episodio arranca en un par $(s,a)$ elegido al azar, con probabilidad no nula para todos. Garantiza que todo par se visite infinitas veces en el límite. Útil en simulación, poco realista en interacción real.
- **Políticas estocásticas** con probabilidad no nula de elegir todas las acciones (se explora siempre): base de los métodos on-policy $\varepsilon$-greedy y off-policy.

**Ejercicio 5.3:** dibujar el backup diagram para la estimación MC de $q_\pi$.

---

## (5.3) — Monte Carlo Control

**Qué representa:** MC + GPI para encontrar la política óptima. Se alterna evaluación completa (muchos episodios, con exploring starts) y mejora (greedy). La clave por la cual no hace falta modelo: como tenemos **action values**, la mejora es directa:

$$
\pi'(s) = \arg\max_a q(a, s) \tag{5.1}
$$

para cada $s$, sin necesitar $p$. Y el **teorema de mejora de política** (sección 4.2) garantiza que si

$$
q_\pi(s, \pi'(s)) \geq v_\pi(s) \quad \forall s \tag{5.2}
$$

entonces $\pi' \geq \pi$ (mejora estricta salvo que ya sea óptimo). Así, con exploring starts + evaluación exacta, el proceso converge a $\pi_*$ y $q_*$ **con solo episodios muestreados**, sin conocer la dinámica.

**De las hipótesis ideales al algoritmo práctico.** Evaluar con "infinitos episodios" es inviable: hay que truncar. La solución natural (y la que usa GPI): **alternar evaluación y mejora episodio por episodio** — tras cada episodio, usar sus retornos para evaluar y luego mejorar la política en los estados visitados. Ese algoritmo es **Monte Carlo ES (Exploring Starts)**:

1. Inicializar $\pi(s)$ y $Q(s,a)$ arbitrarios; listas $Returns(s,a)$ vacías.
2. Elegir $S_0, A_0$ al azar (todos los pares con probabilidad > 0).
3. Generar el episodio siguiendo $\pi$; recorrerlo hacia atrás con $G \leftarrow \gamma G + R_{t+1}$.
4. Para cada par $(S_t, A_t)$ que no haya aparecido antes en el episodio: agregar $G$ a sus retornos, actualizar $Q$ al promedio, y fijar $\pi(S_t) \leftarrow \arg\max_a Q(S_t, a)$.

**Propiedad clave:** MC ES **no puede converger a una política subóptima** — si lo hiciera, $Q$ convergería a *esa* política y eso a su vez forzaría un cambio de política. Solo hay estabilidad cuando política y valor son óptimos. (Nota: la convergencia total no está demostrada formalmente; es una de las preguntas teóricas abiertas más conocidas del RL.)

**Ejemplo 5.3: resolver blackjack con MC ES.** Se arman exploring starts fáciles en simulación (elegir cartas del dealer, suma y as usable al azar). La política óptima hallada coincide con la "basic strategy" de Thorp (1966), con una sola excepción en la política con as usable. **Ejercicio 5.4:** el pseudocódigo es ineficiente (guarda listas de retornos y promedia a cada rato); usar actualización incremental tipo cap. 2.

---

## (5.4) — Monte Carlo Control without Exploring Starts

**Qué representa:** eliminar el supuesto de exploring starts. La única forma general de asegurar que todas las acciones se elijan infinitas veces es **seguir eligiéndolas**. Dos familias:

- **On-policy:** se evalúa/mejora la misma política que genera los datos (pero se explora siempre dentro de ella).
- **Off-policy:** se aprende una política *target* (usualmente la óptima determinista) con datos generados por otra *behavior* (exploratoria). Se ve en 5.5–5.7.

Acá, un método **on-policy** con políticas *soft*: $\pi(a|s) > 0$ para todo $s, a$, que van acercándose a la política óptima determinista.

**$\varepsilon$-greedy (la pieza clave):** la mayoría de las veces elige la acción con mayor $Q$ estimado; con probabilidad $\varepsilon$ elige al azar. Formalmente, las no-greedy tienen probabilidad $\varepsilon/|\mathcal{A}(s)|$ cada una, y la greedy toma el resto. Las $\varepsilon$-greedy son un caso de políticas **$\varepsilon$-soft** ($\pi(a|s) \geq \varepsilon/|\mathcal{A}(s)|$).

**Teorema de mejora para $\varepsilon$-soft:** si $\pi$ es $\varepsilon$-soft y $\pi'$ es $\varepsilon$-greedy respecto de $q_\pi$, entonces $\pi' \geq \pi$ (por el teorema de mejora de política: $q_\pi(s, \pi'(s))$ es un promedio ponderado de valores, menor o igual que el máximo). Y la igualdad solo se da cuando ambas son **óptimas entre las $\varepsilon$-soft**.

**El truco del "entorno modificado":** en vez de probar optimalidad $\varepsilon$-soft directamente, se define un entorno nuevo que "mete el $\varepsilon$ adentro": con probabilidad $\varepsilon$ elige la acción al azar y con $1-\varepsilon$ se comporta como el original. Lo óptimo *en el entorno nuevo con políticas generales* = lo óptimo *en el original con políticas $\varepsilon$-soft*. Como ese $v_*$ nuevo es único y la condición de optimalidad de Bellman se satisface, la política es óptima entre las $\varepsilon$-soft.

**Resumen del resultado:** se elimina el exploring starts a cambio de quedarse con la **mejor política $\varepsilon$-soft** (no la greedy pura). La actualización de $Q$ se asume exacta; el esquema sigue siendo GPI.

---

## (5.5) — Off-policy Prediction via Importance Sampling

**Qué representa:** el dilema de todo control: querés aprender el valor de decisiones **óptimas**, pero necesitás comportarte **subóptimamente** para explorarlas. On-policy era un compromiso (aprende una política casi-óptima pero que explora). Off-policy separa las dos cosas:

- **Target policy $\pi$:** la que se aprende (y que será óptima).
- **Behavior policy $b$:** la que genera los datos (exploratoria).

Condición de **coverage:** toda acción posible bajo $\pi$ debe tener probabilidad no nula bajo $b$ ($\pi(a|s)>0 \Rightarrow b(a|s)>0$); por eso $b$ es estocástica/soft mientras $\pi$ puede ser determinista.

**Importance sampling:** recién se puede promediar retornos de $b$ con expectativa $v_b$, pero queremos $v_\pi$. Se ponderan los retornos por el **ratio de importance sampling** — la probabilidad relativa de la trayectoria bajo las dos políticas:

$$
\rho_{t:T-1} = \prod_{k=t}^{T-1} \frac{\pi(A_k \mid S_k)}{b(A_k \mid S_k)} \tag{5.3}
$$

Clave: las probabilidades de transición $p$ del MDP aparecen iguales arriba y abajo y **se cancelan**: el ratio solo depende de las dos políticas y de la secuencia de acciones. Con esto, $\mathbb{E}[\,\rho_{t:T-1} G_t \mid S_t=s\,] = v_\pi(s)$: el retorno escalado tiene la expectativa correcta.

**Dos variedades para $V(s)$:**

- **Ordinary importance sampling** (promedio simple):

$$
V(s) = \frac{\sum_{t \in \mathcal{T}(s)} \rho_{t:T(t)-1}\, G_t}{|\mathcal{T}(s)|} \tag{5.5}
$$

- **Weighted importance sampling** (promedio ponderado):

$$
V(s) = \frac{\sum_{t \in \mathcal{T}(s)} \rho_{t:T(t)-1}\, G_t}{\sum_{t \in \mathcal{T}(s)} \rho_{t:T(t)-1}} \tag{5.6}
$$

**Idea high-level (sesgo vs varianza):** ordinary es **insesgado** pero de **varianza (posiblemente) infinita** (si un ratio vale 10, la estimación vale 10× el retorno observado). Weighted es **sesgado** (sesgo → 0 asintóticamente) pero de **varianza finita siempre** (el mayor peso de cualquier retorno es 1) y de varianza → 0 asintótica incluso con ratios de varianza infinita. **En la práctica gana casi siempre weighted.**

**Ejemplo 5.4: blackjack off-policy.** Evaluar un solo estado (dealer muestra un 2, suma 13, as usable) con datos generados por una behavior aleatoria (hit/stick 50/50) y target "stick solo en 20/21". El valor real es ≈ −0.27726 (computado con 100 millones de episodios directos). Ambas variedades se acercan, pero la **weighted converge con mucho menos error** (figura 5.3).

**Ejemplo 5.5: varianza infinita.** MDP de un solo estado con dos acciones (`right` → terminal; `left` → 0.9 vuelve a $s$, 0.1 terminal con +1). Target: siempre `left`; behavior: 50/50. El valor correcto es 1. Con ordinary, aun tras millones de episodios los estimates no convergen (varianza infinita); con weighted, tras el primer episodio que termina con `left`, el estimate es exactamente 1 (los episodios con `right` tienen ratio 0 y no aportan).

**Ejercicio 5.6:** análogo de (5.6) para $Q(s,a)$.

---

## (5.6) — Incremental Implementation

**Qué representa:** computar los promedios **incrementalmente**, episodio a episodio, con las técnicas del cap. 2 (sección 2.4), reemplazando "recompensas" por "retornos".

**Caso ordinary:** como es un promedio simple, sirve la misma actualización incremental del cap. 2, usando los retornos escalados por el ratio.

**Caso weighted:** hace falta mantener, además de $V_n$, la **suma de pesos** $C_n$ (ec. 5.7–5.8):

$$
V_{n+1} = V_n + \frac{W_n}{C_n}\, (G_n - V_n), \qquad C_{n+1} = C_n + W_n
$$

con $C_0 = 0$. El pseudocódigo *off-policy MC prediction* itera: tomar una behavior $b$ con cobertura, generar episodio, y recorrerlo hacia atrás actualizando $Q(s,a)$ y $C(s,a)$ con peso acumulado $W$.

**Idea high-level:** el mismo algoritmo sirve para on-policy haciendo $b = \pi$ (entonces el ratio $W$ es siempre 1). La aproximación $Q$ converge a $q_\pi$ para todos los pares encontrados, aunque las acciones se elijan con otra política.

**Ejercicios:** **5.9** (modificar first-visit MC para usar actualización incremental) y **5.10** (derivar la regla (5.8) desde el promedio ponderado).

---

## (5.7) — Off-policy Monte Carlo Control

**Qué representa:** control **off-policy** completo, la segunda familia de métodos de control. La **behavior policy $b$** es soft (explora todo); la **target policy $\pi$** es greedy respecto de $Q$ (por eso puede volverse determinista y óptima). Para garantizar convergencia, $b$ debe ser $\varepsilon$-soft (todos los pares visitados infinitas veces).

**Pseudocódigo del algoritmo (GPI + weighted importance sampling):**
1. Inicializar $Q(s,a)$, $C(s,a)=0$, $\pi(s) = \arg\max_a Q(s,a)$.
2. Para cada episodio: elegir $b$ soft, generar episodio con $b$, recorrer hacia atrás con $G \leftarrow \gamma G + R_{t+1}$.
3. Mantener $W$ (el ratio acumulado); para cada par: actualizar $C$ y $Q$ con la regla weighted incremental; corregir $\pi$ greedy; actualizar $W \leftarrow W \cdot \pi(A_t|S_t)/b(A_t|S_t)$ y cortar si $A_t \neq \pi(S_t)$ (los pasos no-greedy anulan el resto del episodio, porque el ratio va a cero).

**Idea high-level:**
- El método **solo aprende de las colas de los episodios** (los tramos donde todas las acciones restantes son greedy). Si hay muchas acciones no-greedy, el aprendizaje es lento, sobre todo para estados al principio de episodios largos. El antídoto natural es TD (cap. 6); con $\gamma < 1$, también ayuda la sección 5.8.
- Hay que romper empates en el $\arg\max$ de forma consistente.

**Ejercicio 5.11:** en la actualización incremental de $W$, el peso correcto para el par $(S_t, A_t)$ es solo $\pi(A_t|S_t)/b(A_t|S_t)$ y no el ratio completo $\rho_{t:T-1}$: los factores posteriores $k > t$ aparecen iguales en el numerador y el denominador del promedio ponderado de (5.6) y por lo tanto se cancelan. Actualizar $W$ paso a paso y usar la versión truncada en cada par es exacto.
**Ejercicio 5.12 (programación, "Racetrack"):** control MC aplicado a un auto de carrera en una grilla (velocidades discretas, 9 acciones de aceleración, recompensa −1 por paso, borde de pista y ruido). Aplicar un método MC para hallar la política óptima desde cada estado inicial.

---

## (5.8) — Discounting-aware Importance Sampling

**Qué representa:** una mejora de los estimadores off-policy que aprovecha la **estructura interna del retorno como suma descontada**, reduciendo la varianza cuando $\gamma < 1$.

**El problema:** si los episodios son largos y $\gamma$ chico, la mayor parte del ratio de importance sampling del retorno es **irrelevante** y solo agrega ruido. Ejemplo extremo del libro: 100 pasos, $\gamma = 0$. El retorno es $G_0 = R_1$, pero su ratio es un producto de **100 factores**: solo el primer factor importa; los otros 99 son independientes del retorno, de esperanza 1, y no cambian la esperanza del update pero le suman (potencialmente infinita) varianza.

**La idea:** tratar el descuento como una **probabilidad de terminación "parcial"**. El retorno $G_t$ se ve como una suma de **flat partial returns** con horizonte $h$:

$$
\bar G_{t:h} = R_{t+1} + R_{t+2} + \cdots + R_h
$$

(sin descuento, cortados en el horizonte $h$), de modo que

$$
G_t = \sum_{k=t}^{T-1} \gamma^{k-t}\, \bar G_{t:k+1}
$$

y se escalan estos *tramos* con un ratio truncado solo hasta el horizonte (los factores posteriores se descartan). Se definen así un estimador **ordinary** y un **weighted** "discounting-aware" (este último es la ec. 5.10, que el ejercicio 5.14 aprovecha). Cuando $\gamma = 1$ no cambian nada respecto de 5.5/5.6.

---

## (5.9) — Per-decision Importance Sampling

**Qué representa:** otra forma de mirar la estructura del retorno (ahora útil **aun con $\gamma = 1$**) para bajar la varianza.

**La idea:** cada término del numerador de los estimadores es una suma de productos "recompensa × ratio". Se puede demostrar que los factores del ratio que ocurren **después** de cada recompensa tienen esperanza 1 y no aportan en expectativa; repitiendo sub-término a sub-término, el ratio de cada recompensa $R_{k+1}$ se reemplaza por el **truncado** solo hasta el instante $k$. El resultado es el estimador **per-decision** $\bar\rho$: mismo sesgo nulo que ordinary (en first-visit), pero menor varianza.

**Advertencia:** no hay (hasta donde se conoce) una versión **per-decision de weighted** que sea consistente (que converja con datos infinitos). *Ejercicios $\star$:* **5.13** (derivar el estimador per-decision desde la identidad clave del capítulo) y **5.14** (adaptar el control off-policy al estimador truncado).

---

## (5.10) — Summary: MC vs DP

**Lo que aportan los métodos MC** (ventajas sobre DP):
1. Aprenden comportamiento óptimo **directo de la interacción**, sin modelo.
2. Funcionan con *simulación* o *sample models*: es fácil simular episodios aunque sea inviable escribir la tabla de probabilidades de DP.
3. **Enfoque en un subconjunto de estados**: evaluar con precisión una región sin pagar el costo del resto.
4. (Se desarrolla más adelante en el libro) Menos daño ante violaciones de la propiedad de Markov, porque **no bootstrap**.

**Exploración:** la exploración suficiente es el problema central del control MC. Exploring starts (solo simulación), on-policy (la política explora siempre, busca la mejor que aún explora) u off-policy (explora pero aprende una determinista óptima).

**Off-policy:** learning de un target policy con datos de un behavior policy vía **importance sampling**. Ordinary = insesgado, varianza grande/infinita; weighted = sesgado pero varianza finita, preferido en la práctica. Aún son áreas de investigación activa (tanto predicción como control off-policy).

**Las DOS diferencias grandes con DP:**
1. MC opera sobre **experiencia muestreada** (no necesita modelo).
2. MC **no bootstrap** (no actualiza estimaciones con otras estimaciones).

Son propiedades **separables**: el cap. 6 combina (aprende de experiencia **y** bootstrap).

---

## Cómo se conecta con los capítulos 3, 4 y 6

- Cap. **3**: Bellman y funciones de valor (siguen siendo la meta: $v_\pi$, $q_*$).
- Cap. **4**: DP daba el esqueleto — GPI, policy improvement theorem, control — pero con la muleta del **modelo completo**. MC toma ese esqueleto GPI y lo hace funcionar **solo con episodios**.
- Cap. **6**: TD learning mantiene "aprender de experiencia" (sin modelo) pero **reintroduce el bootstrapping** de DP (aprende de sus propias estimaciones, paso a paso). MC es el extremo opuesto: espera el final del episodio y no usa estimaciones propias.
