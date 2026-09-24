# Tarea 1 — Introduction (Capítulo 1)

**Fuente:** Sutton & Barto, *Reinforcement Learning: An Introduction* (2da ed.), **Capítulo 1** (Introduction).

> **Aclaración:** el capítulo 1 es introductorio y **no tiene ecuaciones numeradas**; define qué es el aprendizaje por refuerzo (RL), lo contrasta con *supervised*/*unsupervised learning*, presenta los elementos de un sistema de RL, el dilema exploración–explotación, un ejemplo extendido (Tic-Tac-Toe) donde aparece la primera *temporal-difference* update, y un repaso histórico. Secciones: 1.1 *reinforcement learning*, 1.2 *examples*, 1.3 *elements*, 1.4 *limitations and scope*, 1.5 *extended example: tic-tac-toe*, 1.6 *summary* y 1.7 *early history*.

**Índice**

1. Encuadre: RL en una frase
2. (1.1) Reinforcement Learning
3. (1.2) Examples
4. (1.3) Elements of Reinforcement Learning
5. (1.4) Limitations and Scope
6. (1.5) An Extended Example: Tic-Tac-Toe
7. (1.6) Summary
8. (1.7) Early History of Reinforcement Learning
9. Cómo se conecta con el resto del libro

---

## Encuadre: RL en una frase

El aprendizaje por refuerzo es **"aprender qué hacer —cómo mapear situaciones (estados) a acciones— para maximizar una señal numérica de recompensa"**. El agente no recibe instrucciones de qué acción tomar: debe **descubrirlo probando** (*trial-and-error search*), y las acciones pueden afectar no solo la recompensa inmediata sino también las situaciones futuras y, a través de ellas, todas las recompensas siguientes (*delayed reward*).

> Esas dos características —**búsqueda por prueba y error** y **recompensa diferida**— son los dos rasgos distintivos del RL. La formalización matemática (MDPs, cap. 3, y las funciones de valor) servirá para aterrizar esta idea.

---

## (1.1) — Reinforcement Learning

**Qué representa:** posicionar el RL dentro del aprendizaje de máquinas y fijar su vocabulario. El nombre "reinforcement learning" nombra tres cosas a la vez — un **problema**, una **clase de métodos** que lo resuelven, y el **campo** que los estudia — y conviene mantener separados los tres sentidos (el error de confundirlos es fuente de confusiones).

**Dónde vive frente a los otros paradigmas:**
- **Supervised learning:** aprende de ejemplos etiquetados (situación → acción correcta) dados por un supervisor. En problemas interactivos es poco práctico obtener ejemplos correctos *y* representativos de todas las situaciones; en territorio desconocido el agente debe aprender de su propia experiencia.
- **Unsupervised learning:** busca estructura escondida en datos no etiquetados. El RL *no* es esto: aunque tampoco usa ejemplos correctos, no busca estructura, sino **maximizar una señal de recompensa**. Es un **tercer paradigma** (puede combinar propiedades de los otros dos, p. ej. usar supervisión para generalizar).

**Idea high-level:**
- **Exploración vs. explotación (el dilema central).** Para ganar recompensa hay que *explotar* las acciones que ya funcionaron, pero para descubrirlas hay que *explorar* acciones nuevas. Ninguno de los dos con exclusividad funciona: el agente debe probar variedad de acciones **y** favorecer progresivamente las mejores. En tareas estocásticas cada acción debe probarse muchas veces para estimar su recompensa esperada con fiabilidad. Este dilema ni siquiera aparece en el aprendizaje supervisado/no supervisado puro y sigue sin estar resuelto del todo.
- **El RL ataca el problema completo** de un agente con objetivos, que siente su entorno y actúa sobre él, bajo incertidumbre — en contraste con enfoques que estudian subproblemas aislados (p. ej. planificación sin modelos predictivos, o supervisión sin decir para qué sirve).
- **Interacción con otras disciplinas:** el RL es parte de un movimiento hacia principios generales (contra la idea de que la inteligencia es solo acumular hechos/heurísticas), y tiene fructíferos cruces con estadística, optimización, psicología y neurociencia (cap. 14 y 15).

---

## (1.2) — Examples

**Qué representa:** ejemplos que guiaron el desarrollo del RL. Varios: un maestro de ajedrez que combina *planning* con juicios intuitivos; un controlador adaptativo de una refinería que optimiza en tiempo real; un robot móvil que decide si entrar a un cuarto nuevo a buscar basura o volver a la base a recargar la batería (según el nivel de carga y si encontró el cargador fácil en el pasado); un cachorro de gacela que aprende a pararse y correr; Phil preparando el desayuno (una web compleja de submetas entrelazadas).

**Idea high-level:** rasgos que comparten todos y que son fáciles de pasar por alto:
- **Interacción** entre un agente activo que toma decisiones y su entorno.
- El agente busca un **objetivo** explícito (puede juzgar avance por lo que siente directamente: ganar/no ganar, producción, caerse o no, nivel de batería).
- Actúa bajo **incertidumbre**: los efectos de las acciones no son totalmente predecibles → hay que monitorear y reaccionar.
- Las acciones afectan el **futuro** del entorno → las decisiones correctas requieren tener en cuenta consecuencias **indirectas y diferidas** (foresight/planning).
- El agente **mejora con la experiencia**; el conocimiento previo influye en qué es fácil de aprender, pero la interacción es esencial.

---

## (1.3) — Elements of Reinforcement Learning

**Qué representa:** los cuatro subelementos de un sistema de RL. Algunos están siempre; el cuarto es opcional.

- **Policy (política):** modo de comportarse del agente: un mapeo estados → acciones. Es el **núcleo** (basta para determinar el comportamiento); puede ser una tabla, una función con cómputo extenso o un proceso de búsqueda; puede ser **estocástica** (probabilidades por acción).
- **Reward signal (señal de recompensa):** define el **objetivo**. El entorno manda un número en cada paso; el único objetivo del agente es **maximizar la recompensa total** a largo plazo. Define qué eventos son buenos/malos (análogo al placer/dolor); es la base primaria para alterar la política.
- **Value function (función de valor):** qué es bueno en el **largo plazo**. El *valor* de un estado es la recompensa total que se espera acumular desde él — valora los estados que *probablemente* sigan. Acciones se eligen por **valores**, no por recompensas inmediatas (un estado puede dar poca recompensa inmediata y alto valor si conduce a estados ricos en recompensa, o al revés).
- **Model (modelo) — opcional:** algo que imita el entorno y permite inferir cómo se comportará (dado estado y acción, predice el próximo estado y recompensa). Se usa para **planning**. Métodos que lo usan → **model-based**; los que no, **model-free** (puros *trial-and-error*, casi lo opuesto a planificar). El cap. 8 estudia sistemas que aprenden, modelan y planifican a la vez.

**Idea high-level:**
- Las recompensas son **primarias** y los valores **secundarios** (son *predicciones* de recompensa; sin recompensas no habría valores). Sin embargo, **con los valores se toman las decisiones**: electamos acciones que llevan a estados de mayor valor porque eso da más recompensa a largo plazo.
- Determinar valores es **mucho más difícil** que recibir recompensas: se deben estimar y re-estimar de las secuencias de observaciones de toda la vida. **El componente más importante de casi todo algoritmo de RL es un método eficiente para estimar valores** — quizá lo más importante aprendido del campo en seis décadas.

---

## (1.4) — Limitations and Scope

**Qué representa:** el alcance que el libro se auto-impone. Dos limitaciones centrales:

- **Estado dado vs. estado aprendido.** El RL depende fuertemente del concepto de estado (entrada de política y función de valor, entrada y salida del modelo). El libro **asume que la señal de estado ya viene construida** (la produce un sistema de pre-procesamiento nominalmente parte del entorno) y se concentra en decidir *qué acción tomar* en función de esa señal; **no** aborda cómo construir/cambiar/aprender la representación del estado (salvo brevemente en 17.3).

- **RL "aprendiendo en interacción" vs. métodos evolutivos.** Muchos métodos resuelven problemas de optimización sin estimar funciones de valor: *genetic algorithms*, *genetic programming*, *simulated annealing*. Estos **métodos evolutivos** aplican muchas políticas estáticas, cada una interactúa largo tiempo con una instancia del entorno, y las que más recompensa logran (y variaciones aleatorias) pasan a la siguiente generación. No aprenden durante la vida individual.

**Idea high-level:** pueden ser efectivos si el espacio de políticas es chico, bien estructurado, o hay mucho tiempo — y tienen ventaja cuando el agente no puede sentir el estado completo. Pero **desperdician la estructura del problema**: no usan que la política es una función estados→acciones, no notan por qué estados pasa el individuo ni qué acciones elige, y **no aprenden en interacción**. Por eso el libro no los cubre como métodos de RL.

---

## (1.5) — An Extended Example: Tic-Tac-Toe

**Qué representa:** el primer algoritmo concreto del libro (y la primera función de valor). Jugamos X contra un oponente imperfecto; meta: maximizar probabilidad de ganar (empates y derrotas igual de malos). No conocemos el modelo del oponente (necesario para DP/minimax), así que aprendemos por experiencia.

**Cómo se construye el aprendiz:**
- Tabla con una entrada por **estado** del tablero; cada número = estimación de la **probabilidad de ganar** desde ese estado (**valor** del estado; la tabla entera es la función de valor). Estados ganadores → 1, perdedores/llenos → 0, resto → 0.5.
- Se juegan muchas partidas. La mayoría de las veces se mueve **greedy** (al estado de mayor valor); ocasionalmente se hace un **exploratory move** (al azar entre los demás) para experimentar estados que nunca se verían. Los movimientos exploratorios **no producen aprendizaje**.
- Después de cada movimiento greedy, se "back-up" el valor del estado posterior al anterior:
$$
V(S_t) \leftarrow V(S_t) + \alpha\,[\, V(S_{t+1}) - V(S_t) \,]
$$
donde $\alpha$ es el **step-size parameter** (fracción positiva pequeña). Esta regla es un **método de temporal-difference (TD)**: el cambio se basa en la diferencia $V(S_{t+1}) - V(S_t)$ entre estimaciones en dos tiempos sucesivos.

**Idea high-level:**
- Si $\alpha$ decrece adecuadamente, converge (para oponente fijo) a las probabilidades reales de ganar y produce el **juego óptimo contra ese oponente**; incluso funciona contra oponentes que cambian lentamente si $\alpha$ no llega a cero.
- **Contraste con métodos evolutivos (lección grande):** el evolutivo congela la política, juega muchas partidas, y da crédito a *toda* la conducta de la partida por el resultado final — incluso **a movimientos que nunca hicieron**. La función de valor, en cambio, permite evaluar **estados individuales** aprovechando la información durante el juego (y produce el efecto de "planning" sin modelo ni búsqueda explícita).
- **Generalidad:** sirve para "jugar contra la naturaleza" (sin adversario), tareas continuas, y estados enormes/infinitos: Tesauro aplicó la misma idea con redes neuronales al **backgammon** (~$10^{20}$ estados) y superó a los mejores humanos — la capacidad de *generalizar* de la experiencia a estados nuevos es la clave en espacios grandes.
- **Model-free respecto del oponente**: no tiene modelo del oponente; los modelos no son necesarios, y aprenderlos (si se puede) o usarlos si están disponibles se ve en el cap. 8.
- No implica *tabula rasa*: se puede inyectar conocimiento previo, y el RL funciona también con estado oculto o no discreto. Ejercicios destacados: **1.1** (self-play con ambos lados aprendiendo), **1.3** (¿aprende mejor un jugador *puro* greedy?), **1.4** (¿qué probabilidades se computan si se aprende también de los exploratory moves?).

---

## (1.6) — Summary

**Qué queda del capítulo:** el RL es un enfoque computacional para **aprender a decidir** con objetivos a largo plazo, aprendiendo por **interacción directa** con el entorno, sin supervisión ejemplar ni modelos completos. Es, según los autores, el primer campo que aborda de verdad los problemas computacionales de aprender de la interacción.

**Idea high-level:**
- El marco formal son los **MDPs** (estados, acciones, recompensas): una representación sencilla de los rasgos esenciales del problema IA — causalidad, incertidumbre/nondeterminismo y objetivos explícitos.
- **Las funciones de valor son la clave** de casi todos los métodos del libro: son lo que permite **búsqueda eficiente en el espacio de políticas**, y distinguen al RL de los métodos evolutivos que buscan directamente en ese espacio guiados por la evaluación de políticas enteras.

---

## (1.7) — Early History of Reinforcement Learning

**Qué representa:** los tres hilos históricos que confluyeron a fines de los 80 en el RL moderno:

1. **Trial-and-error learning** (desde la psicología del aprendizaje animal). Antecedentes: Thorndike y la **Ley del Efecto** (1911): los comportamientos seguidos de satisfacción se refuerzan, los seguidos de incomodidad se debilitan; el término "reinforcement" aparece en 1927 vía Pavlov. En la computación temprana: el "pleasure-pain system" de **Turing** (1948), máquinas electromecánicas (Ross 1933, la tortuga mecánica de Grey Walter 1951, el ratón Theseus de Shannon 1952), **Minsky** (1954, SNARCs) y el *credit-assignment problem* (Minsky 1961): *¿cómo repartir crédito entre las muchas decisiones que produjeron un éxito?* — problema al que apuntan todos los métodos del libro. Hitos: **MENACE** de Michie (1961-63, tic-tac-toe con cajas de cuentas), **BOXES** de Michie & Chambers (pole-balancing), *learning automata* (Tsetlin, k-armed bandit), classifier systems de **Holland** (1976/86, con el *bucket-brigade* para credit assignment), y **Klopf** (1972) que resucitó el hilo resaltando los aspectos hedónicos del comportamiento.

2. **Optimal control + value functions + dynamic programming.** Bellman (años 50) con la **ecuación de Bellman** (extensión de la teoría de Hamilton–Jacobi) y los **MDPs**; Howard (1960) con *policy iteration*. DP sufre la **maldición de la dimensionalidad**, y su integración con el aprendizaje "en vivo" fue lenta (se lo veía como cómputo offline y hacia atrás en el tiempo); la integración plena llegó con **Watkins (1989) y Q-learning**.

3. **Temporal-difference learning** (hilo más chico y distintivo, propio del RL): aprender de la **diferencia entre estimaciones sucesivas** de un mismo valor. En psicología, los reforzadores secundarios; **Samuel** (1959, damas) propuso el primer método con ideas TD; **Sutton** (1978-88) lo separó del control y presentó **TD(λ)** (1988); **Witten** (1977) fue posiblemente la primera publicación tabular TD(0). La convergencia de los tres hilos: **Q-learning (Watkins, 1989)** y el éxito de **TD-Gammon (Tesauro, 1992)** trajeron atención al campo.

**Idea high-level:** el vínculo con **neurociencia** es uno de los desarrollos recientes más llamativos: la similitud entre los algoritmos TD y la actividad de las neuronas dopaminérgicas (cap. 15). Y vale la nota conceptual importante: los autores consideran a DP también "métodos de RL" (resuelven MDPs aunque requieran modelo completo), lo que unifica lo visto después en los capítulos 3–5.

---

## Cómo se conecta con el resto del libro

- El **cap. 2** formaliza el primer pedazo: el *k-armed bandit* (recompensa en una sola situación, dilema exploración–explotación puro, sin asociación estado↔acción).
- El **cap. 3** convierte en matemática lo que acá es verbal: MDPs, retornos, funciones de valor y ecuaciones de Bellman.
- El **cap. 4** (DP) es el hilo de optimal control; el **cap. 5** (Monte Carlo) y el **6** (TD) el de trial-and-error + TD; todos encajan en el marco GPI de evaluación/mejora.
- La regla TD del tic-tac-toe (secc. 1.5) es el ancestro directo de los métodos del **cap. 6**.