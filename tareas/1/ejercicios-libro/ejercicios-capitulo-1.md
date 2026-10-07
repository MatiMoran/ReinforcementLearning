# Tarea 1 — Ejercicios del Capítulo 1 (Introduction)

**Fuente:** Sutton & Barto, *Reinforcement Learning: An Introduction* (2da ed.), **Capítulo 1**.
**Ubicación en el libro:** los cinco ejercicios del capítulo están al final de la sección **1.5 — An Extended Example: Tic-Tac-Toe**.

> **Contexto previo:** el algoritmo del ejemplo juega X contra un oponente imperfecto. Mantiene una tabla con un valor por estado (estimación de la probabilidad de ganar desde ese tablero), se mueve *greedy* la mayoría de las veces y ocasionalmente hace un *exploratory move* al azar. Después de cada movimiento greedy hace el *backup* con la regla TD:
> $$V(S_t) \leftarrow V(S_t) + \alpha\,[\,V(S_{t+1}) - V(S_t)\,]$$
> Los movimientos exploratorios **no producen aprendizaje**. Con α decreciente, el método converge a las probabilidades reales de ganar (dado oponente fijo) y a la política óptima contra ese oponente.

**Índice**

1. [Ejercicio 1.1 — Self-Play](#ejercicio-11--self-play)
2. [Ejercicio 1.2 — Symmetries](#ejercicio-12--symmetries)
3. [Ejercicio 1.3 — Greedy Play](#ejercicio-13--greedy-play)
4. [Ejercicio 1.4 — Learning from Exploration](#ejercicio-14--learning-from-exploration)
5. [Ejercicio 1.5 — Other Improvements](#ejercicio-15--other-improvements)

---

## Ejercicio 1.1 — Self-Play

> **Exercise 1.1: Self-Play** Suppose, instead of playing against a random opponent, the reinforcement learning algorithm described above played against itself, with both sides learning. What do you think would happen in this case? Would it learn a different policy for selecting moves?

### Respuesta

**Qué pasaría:** el juego dejaría de ser un problema de "aprender contra un oponente fijo" y se volvería un problema de **juego competitivo** donde el entorno (el oponente) cambia a la vez que el agente. Los dos lados comparten el mismo esquema de aprendizaje: cada uno tiene su tabla de valores, se mueve greedy salvo exploraciones, y hace backups TD después de sus movimientos greedy.

**Consecuencias esperadas:**

1. **El entorno es no estacionario para cada lado.** La convergencia garantizada por la sección 1.5 ("para cualquier oponente fijo") ya no aplica directamente: la política del oponente cambia mientras uno aprende, de modo que las probabilidades de ganar que se intentan estimar se desplazan todo el tiempo. Lo más probable es que el sistema oscile o se estabilice en un equilibrio, en lugar de convergir a las probabilidades "verdaderas" contra un oponente inmóvil.

2. **Aparece una dinámica de mejora mutua (y de exploitablez).** Cada lado castiga los errores del otro, así que ambos se vuelven progresivamente más duros. Contra un oponente random, la función de valor aprende una probabilidad de ganar muy alta en casi cualquier estado ventajoso; contra un oponente que también aprende, esas probabilidades se comprimen hacia valores más realistas (más tablas y empates entre jugadores fuertes), y el aprendizaje se concentra en los pocos estados donde todavía hay margen de error.

3. **Sí, aprendería una política distinta.** La política aprendida contra un oponente random maximiza la probabilidad de *encontrar* sus errores; contra un oponente que aprende, lo que conviene es jugar de forma más "segura" y explotar los errores *residuales* que el oponente todavía comete (por ejemplo, dejando de ofrecer trampas de varias jugadas que un oponente random caería y uno aprendiz no). Es la misma razón por la que la sección 1.5 advierte que el método converge a la política óptima *contra ese oponente en particular*: cambia el oponente, cambia la política óptima.

**Matiz importante:** el procedimiento converge (con α decreciente y suficiente exploración) a un **equilibrio estable** — análogo al concepto de juego perfecto: ambos lados juegan de modo que ninguno puede empeorar unilateralmente. Notar que este setup es el ancestro directo de lo que más adelante aparece en self-play de AlphaGo (sección 16.6.2) y de que, sin embargo, seguir haciendo exploratory moves mantiene un nivel mínimo de "ruido" en ambos lados.

---

## Ejercicio 1.2 — Symmetries

> **Exercise 1.2: Symmetries** Many tic-tac-toe positions appear different but are really the same because of symmetries. How might we amend the learning process described above to take advantage of this? In what ways would this change improve the learning process? Now think again. Suppose the opponent did not take advantage of symmetries. In that case, should we? Is it true, then, that symmetrically equivalent positions should necessarily have the same value?

### Respuesta

**Cómo aprovechar las simetrías:** el tablero de tic-tac-toe tiene **8 simetrías** (4 rotaciones × 2 reflexiones), de modo que como máximo 8 tableros distintos son en realidad el mismo estado. Para aprovecharlo hay dos equivalentes:

- **Canonicalizar el estado:** antes de buscar/actualizar en la tabla, transformar el tablero a una *forma canónica* (p. ej. la menor representación lexicográfica entre sus 8 simetrías) y usar esa clave. Toda la experiencia de un tablero se acumula en una sola entrada.
- **Promover el backup a orbitas:** en la regla TD, en lugar de actualizar un solo `V(S_t)`, actualizar los 8 valores simétricos con el mismo incremento `α[V(S_{t+1}) − V(S_t)]`.

**Cómo mejora el aprendizaje:**

1. **Reduce el espacio de estados ~8×** (de ~5.478 tableros legales a unos pocos cientos de clases de equivalencia): menos estados que explorar y visitar cada uno mucho más seguido.
2. **Acelera la convergencia:** cada muestra actualiza 8 entradas a la vez (o se reutiliza en una sola entrada canónica), lo que reduce drásticamente la varianza de las estimaciones y hace que la exploración rinda mucho más: los exploratory moves dejan de gastarse en "descubrir" tableros que ya se conocen en otra orientación.
3. Es un caso particular de **generalización por invariancia** — la misma idea que más adelante motivaría las redes convolucionales (que imponen invariancias por construcción).

**¿Y si el oponente NO usa simetrías?** Aquí está el truco de la pregunta. El valor de un estado se define como *la probabilidad de ganar desde ese estado jugando contra este oponente concreto*. Si el oponente trata distinto tableros que para nosotros son equivalentes (p. ej. siempre responde en el borde si lo mira "de un lado" y en el centro si lo ve rotado), entonces **no, no es verdad que los estados simétricos tengan necesariamente el mismo valor**: la probabilidad de ganar depende de las respuestas futuras del oponente, y esas respuestas difieren entre estados simétricos.

**Conclusión:**

- Si el oponente **sí** es simétrico en su forma de jugar (por ejemplo, un oponente random: la distribución de sus jugadas es invariante por simetría), imponer simetría en nuestra tabla es *exactamente* correcto y solo aporta ventajas.
- Si el oponente **no** es simétrico, forzar simetría impone un **sesgo**: estamos asumiendo que los estados de la órbita son iguales cuando no lo son. En la práctica conviene hacerlo igual, porque la *antisimetría* del oponente suele ser pequeña y el sesgo se compensa con la enorme ganancia de varianza/muestras; pero conceptualmente la igualdad de valores deja de ser un teorema y pasa a ser una **hipótesis de modelo**.

---

## Ejercicio 1.3 — Greedy Play

> **Exercise 1.3: Greedy Play** Suppose the reinforcement learning player was *greedy*, that is, it always played the move that brought it to the position that it rated the best. Might it learn to play better, or worse, than a nongreedy player? What problems might occur?

### Respuesta

**Aprendería peor, no mejor.** El jugador *greedy puro* nunca hace exploratory moves, con lo que:

1. **Nunca visita muchos estados.** Solo experimenta los tableros alcanzables siguiendo sus propias elecciones greedy desde el estado inicial. Existe un enorme conjunto de estados que jamás se verán (p. ej. tableros donde cometió una mala jugada temprana, o donde el oponente jugó de forma improbable). Para esos estados la tabla queda con el valor inicial 0.5, que es puro *invented*.

2. **Los valores que sí actualiza quedan sesgados.** La regla TD propaga valores solo a lo largo de la trayectoria greedy. Si el jugador nunca explora, las estimaciones de "probabilidad de ganar" dejan de ser estimaciones de esa probabilidad y pasan a ser predicciones auto-confirmantes de su propia política actual.

3. **Aparece el problema clásico de convergencia prematura.** Un error inicial de la tabla se auto-perpetúa: si un estado bueno quedó con valor bajo, el jugador nunca entra ahí, nunca lo re-evalúa, y por lo tanto nunca descubre que era bueno. Al revés: un estado malo sobreestimado atrae al jugador, que ahí pierde... pero si el aprendizaje está ligado a los backups TD convencionales, la señal que recibe es ruidosa y depende de con qué oponente pierda. El sistema converge (si lo hace) a la política greedy *actual*, no a la óptima contra el oponente — es decir, se queda en un óptimo local del espacio de políticas.

4. **Desaparece la garantía de la sección 1.5.** Converger a las probabilidades verdaderas de ganar requiere que cada estado se estime *dado el uso que se hace de él*, y la exploración es lo que hace que la distribución de visitas cubra el espacio. Sin ella, la condición de "suficiente exploración" que exige cualquier método de control por TD/MC no se cumple.

**Problemas concretos que podrían ocurrir:**

- El jugador se vuelve **predecible** y, contra un oponente que no es random, pierde partidas que el jugador *nongreedy* habría ganado.
- **Efecto "trampa de jugadas múltiples":** la sección 1.5 menciona que el jugador RL aprende a armar trampas de varias jugadas. Un jugador greedy puro puede no aprenderlas: armar la trampa exige una jugada intermedia que *empeora* el valor inmediato del tablero (o que no es la de mayor valor estimado en ese instante), y nunca la haría.
- **Falsa confianza:** la tabla queda llena de valores extremos (cerca de 0 o 1) mal calibrados, de modo que el jugador "cree" que tiene ganado un tablero que en realidad no lo está.

**Dato clave:** explorar *cuesta* recompensa inmediata (se juega una jugada subóptima en esa partida) pero *paga* a futuro con mejores estimaciones. Ese es exactamente el **dilema exploración–explotación** de la sección 1.1, y la respuesta del libro es siempre: explorar lo suficiente, pero con una fracción decreciente si se quiere convergencia.

---

## Ejercicio 1.4 — Learning from Exploration

> **Exercise 1.4: Learning from Exploration** Suppose learning updates occurred after *all* moves, including exploratory moves. If the step-size parameter is appropriately reduced over time (but not the tendency to explore), then the state values would converge to a different set of probabilities. What (conceptually) are the two sets of probabilities computed when we do, and when we do not, learn from exploratory moves? Assuming that we do continue to make exploratory moves, which set of probabilities might be better to learn? Which would result in more wins?

### Respuesta

**Las dos colecciones de probabilidades:**

- **Sin aprender de los exploratory moves (el algoritmo original):** el valor de un estado converge a la probabilidad de ganar **siguiendo la política greedy** desde ese estado — es decir, *P(ganar | desde S, jugamos greedy a partir de ahora contra este oponente)*. Los exploratory moves solo sirven para visitar estados, pero no contaminan ni actualizan sus valores; el objetivo aprendido es el de "lo que va a pasar cuando hagamos lo correcto".

- **Aprendiendo también de los exploratory moves:** el valor converge a la probabilidad de ganar bajo la **política mezcla** efectiva que realmente se ejecuta — *P(ganar | desde S, seguimos el esquema de jugar greedy la mayor parte del tiempo y explorar con probabilidad ε)*. Como la exploración continúa (según el enunciado, la tendencia a explorar no se reduce), la política que se evalúa incluye esas jugadas aleatorias.

En lenguaje moderno: la primera es el valor de la política **greedy implícita** $V_*(\text{greedy})$; la segunda es el valor de la política $\varepsilon$-greedy **que realmente se ejecuta**, $V^{\pi_\varepsilon}$. Notar que la primera coincide con la política que *resultaría* de la segunda tras "limpiar" la exploración.

**¿Cuál conviene aprender?**

1. **Siempre se juega con exploración** (la probabilidad no decrece): conviene aprender **la segunda** (la de la política mezcla). Razón: el valor debe reflejar lo que realmente va a ocurrir. Si aprendemos el valor de la política puramente greedy pero seguimos ejecutando movimientos exploratorios, nuestras estimaciones quedan **optimistas respecto de la realidad**: sobreestimamos la calidad de los estados porque imaginamos que siempre jugaremos lo mejor. Cada exploratory move posterior "gasta" recompensa que el valor no había descontado.

2. **Ganaría más partidas el jugador que aprende con la segunda... pero hay que matizar.** El valor de la política mezcla es el correcto para *seleccionar* jugadas si vamos a seguir mezclando: nos dice qué estado es mejor *dado que a veces vamos a errarle*, lo que es exactamente la información que se necesita para elegir entre dos jugadas greedy candidatas cuando el futuro incluye ruido de exploración. Además, al hacer updates también en los exploratory moves, cada jugada — buenas o malas — aporta señal de aprendizaje: hay **más muestras efectivas** y las estimaciones convergen con menos varianza.

   La contrapartida: la política resultante es optimal *respecto del objetivo mezclado*, que es ligeramente peor que el óptimo puro (porque explora "de más"). Si en cambio el objetivo es jugar lo mejor posible **en cada partida ya entrenado**, la primera colección es la que describe la política que queremos ejecutar al final, y esa sí daría más wins *una vez que la exploración se apague*. Por eso la pregunta desemboca en el trade-off clásico: la segunda es mejor **mientras se siga explorando**, la primera es la que interesa como objetivo final.

**Síntesis:** con ε fijo, aprender de todo → valores de la política ε-greedy (auto-consistente con la conducta, menos varianza, más wins en el corto plazo); aprender solo de greedy → valores de la política greedy (sesgados respecto de lo que se hace, pero correctos como objetivo a largo plazo si se retira la exploración).

---

## Ejercicio 1.5 — Other Improvements

> **Exercise 1.5: Other Improvements** Can you think of other ways to improve the reinforcement learning player? Can you think of any better way to solve the tic-tac-toe problem as posed?

### Respuesta

**Mejoras al jugador RL tal como está descrito:**

1. **Usar las simetrías** (ejercicio 1.2): canónizar tableros o propagar los backups a toda la órbita de 8 simetrías. Redución de estados ~8× y ganancia enorme de muestras.

2. **Inicialización informada en lugar de 0.5.** No partir de tabula rasa: los tableros con tres X ya son 1 y con tres O o llenos son 0 (ya lo hace el libro), pero además se pueden pre-setear valores para estados con línea de dos y casilla libre, o incorporar la regla "quien tiene turno con una amenaza abierta gana" — es conocimiento del juego, no del oponente. Acelera muchísimo la convergencia sin sacrificar nada.

3. **Backup a más de un paso (n-step / λ-return).** La regla de la sección 1.5 hace el backup solo entre estados *adyacentes* ($V(S_t) \to V(S_{t+1})$). Propagar a lo largo de toda la secuencia de jugadas de la partida (o con un eligibility-trace TD(λ)) hace que la recompensa final llegue mucho más rápido a las jugadas iniciales — anticipa el n-step return (cap. 7) y TD(λ) (cap. 6).

4. **ε decreciente + paso de aprendizaje α decreciente.** Mantener una mínima exploración pero reducirla, y decaer α conforme a condiciones estándar ($\sum \alpha = \infty$, $\sum \alpha^2 < \infty$) para garantizar convergencia al valor verdadero.

5. **Mejor manejo de la exploración:** hacer los exploratory moves con probabilidad proporcional a la incertidumbre/información (exploración dirigida) en vez de uniforme al azar entre los no-greedy; o explorar solo en las partes del árbol que todavía están mal estimadas.

6. **Tabla de acciones en lugar de estados** (valores estado-acción): evaluar $Q(s,a)$ en vez de $V(s)$. Permite decidir bien incluso cuando un estado se alcanza por primera vez y evita comparar valores de estados hijas ya promediados. Es el puente directo hacia los métodos de control del cap. 5 y 6.

7. **Aprender también del lado que no juega / self-play** (ejercicio 1.1) para entrenar contra un oponente que mejora, o usar **modelos del oponente** estimados de la experiencia (sección 1.5 los menciona y el cap. 8 los trata).

8. **Generalización** para no depender de la tabla completa: agrupar estados por features (p. ej. "tengo dos en línea con casilla abierta") o usar una red neuronal — la clave, según la sección 1.5, para escalar a espacios como el backgammon de Tesauro (~$10^{20}$ estados).

**¿Una mejor forma de resolver el problema tal como está planteado?**

El planteo es: *oponente imperfecto, desconocido, sin modelo; maximizar probabilidad de ganar*. Bajo esas condiciones, hay dos familias de solución claramente mejores que la tabla TD ingenua:

- **Modelo-based con estimación del oponente + planificación.** Se estima de la experiencia la política del oponente (con qué probabilidad juega cada jugada en cada tablero) y se resuelve el MDP resultante con **dynamic programming / minimax bajo modelo estocástico**. La propia sección 1.5 lo señala: "about the best one can do" es aprender un modelo del oponente y luego correr DP; y aclara que no es tan distinto de los métodos RL del libro. Da la solución *óptima contra el modelo estimado* y aprovecha que el juego es chico (búsqueda exhaustiva posible).

- **DP/minimax clásico no sirve tal cual**, porque exige conocer de antemano al oponente (el argumento de la sección 1.5 contra minimax: asume un oponente que maximiza, y nunca llegaría a un estado desde el que pierde aunque en la práctica siempre gana ahí).

En resumen: para *este* problema en particular, la solución más robusta es **aprender modelo del oponente + resolver el MDP**, o bien un método RL con valor estado-acción, simetrías, n-step/TD(λ) y ε decreciente — todos los cuales mejoran sustancialmente al algoritmo base sin cambiar su naturaleza *model-free*.

---

## Ideas clave del capítulo (link con los ejercicios)

- **Trial-and-error + recompensa diferida** (los dos rasgos distintivos del RL) son exactamente lo que practican los 5 ejercicios: todos giran alrededor de *qué tan bien estima el jugador las consecuencias a futuro* de sus jugadas.
- **Recompensas vs. valores:** los ejercicios 1.3 y 1.4 son en esencia sobre qué significa bien estimar un valor — no confundir la recompensa inmediata de la partida con la probabilidad de ganar desde un estado.
- **Exploración–explotación** (1.1): central en 1.1, 1.3 y 1.4; es el dilema que el **cap. 2** (k-armed bandit) aísla en su forma más pura.
- **Regla TD** de la sección 1.5: ancestro directo de los métodos del **cap. 6** (TD prediction/control).
- **Métodos evolutivos vs. funciones de valor:** contraste explícito en 1.5 y usado como marco de referencia en 1.1 y 1.5.
