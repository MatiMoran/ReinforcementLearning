# Tarea 4 — Dynamic Programming (Capítulo 4)

**Fuente:** Sutton & Barto, *Reinforcement Learning: An Introduction* (2da ed.), **Capítulo 4** (Dynamic Programming).

> **Aclaración:** el capítulo 4 reinicia la numeración de ecuaciones (4.1–4.10), retomando las ecuaciones de Bellman del capítulo 3. La sección 4.1 es *policy evaluation*, 4.2 *policy improvement*, 4.3 *policy iteration*, 4.4 *value iteration*, 4.5 *asynchronous DP*, 4.6 *generalized policy iteration*, 4.7 *efficiency* y 4.8 el *summary* (donde aparece el concepto de *bootstrapping*).

**Índice**

1. Encuadre: DP en una frase
2. (4.1) Policy Evaluation (Prediction)
3. (4.2) Policy Improvement
4. (4.3) Policy Iteration
5. (4.4) Value Iteration
6. (4.5) Asynchronous Dynamic Programming
7. (4.6) Generalized Policy Iteration (GPI)
8. (4.7) Efficiency of Dynamic Programming
9. (4.8) Summary y el concepto de *bootstrapping*
10. Cómo se conecta con los capítulos 3, 5 y 6

---

## Encuadre: DP en una frase

La programación dinámica (DP) es una **colección de algoritmos para computar políticas óptimas dado un modelo perfecto del entorno** (un MDP finito con dinámica $p(s', r \mid s, a)$ conocida). La idea rectora del capítulo —y del RL en general— es:

> Las ecuaciones de Bellman dejan de ser meras condiciones de optimalidad y se convierten en **reglas de actualización** (asignaciones) para ir mejorando aproximaciones de $v_\pi$, $v_*$, $q_\pi$ o $q_*$.

Las dos ecuaciones de partida (Bellman optimality, retomadas del cap. 3):

$$
v_*(s) = \max_a \sum_{s', r} p(s', r \mid s, a)\, [\, r + \gamma\, v_*(s') \,] \tag{4.1}
$$

$$
q_*(s, a) = \sum_{s', r} p(s', r \mid s, a)\, [\, r + \gamma\, \max_{a'} q_*(s', a') \,] \tag{4.2}
$$

---

## (4.1) — Policy Evaluation (Prediction)

**Qué representa:** el problema de *predicción*: dada una política $\pi$ arbitraria, calcular $v_\pi(s)$ para todo estado $s$.

$$
v_\pi(s) \doteq \mathbb{E}_\pi[ G_t \mid S_t = s ] \tag{4.3}
$$

Como la dinámica se conoce, la ecuación de Bellman para $v_\pi$ es un **sistema de $|S|$ ecuaciones lineales con $|S|$ incógnitas**:

$$
v_\pi(s) = \sum_a \pi(a\mid s) \sum_{s', r} p(s', r \mid s, a)\, [\, r + \gamma\, v_\pi(s') \,] \tag{4.4}
$$

En principio se puede resolver directo (tedioso pero directo). La versión iterativa — *iterative policy evaluation* — convierte (4.4) en una regla de actualización:

$$
v_{k+1}(s) = \sum_a \pi(a\mid s) \sum_{s', r} p(s', r \mid s, a)\, [\, r + \gamma\, v_k(s') \,] \tag{4.5}
$$

**Idea high-level:**
- La secuencia $\{v_k\}$ converge a $v_\pi$ cuando $k \to \infty$ (basta $\gamma < 1$ o terminación garantizada). El punto fijo de (4.5) es $v_\pi$ por la propia ecuación de Bellman.
- Cada iteración barre **todos** los estados (un *sweep*) y reemplaza el valor viejo por uno nuevo calculado con los valores de los sucesores: eso es un **expected update** (actualización esperada), porque promedia sobre todos los posibles $s'$ y sus probabilidades en lugar de usar una muestra.
- La versión *in-place* (un solo arreglo, sobrescribiendo) converge más rápido que la de dos arreglos, porque aprovecha datos frescos apenas se generan. El orden de barrido en la versión in-place influye en la velocidad de convergencia.
- Criterio de parada práctico: cortar cuando $\max_s |v_{k+1}(s) - v_k(s)| < \theta$ (pequeño threshold de precisión), aunque formalmente converge solo en el límite.

**Ejemplo 4.1: gridworld 4×4.** Estados no terminales $\mathcal{S} = \{1, \ldots, 14\}$; 4 acciones (up, down, right, left) deterministas; moverse fuera de la grilla deja el estado igual. Tarea **episódica y sin descuento** con recompensa **−1 en cada paso** hasta llegar al estado terminal. Con la política **equiprobable** (todas las acciones con igual probabilidad), $v_\pi(s)$ es el **negativo del número esperado de pasos desde $s$ hasta terminar**. La figura 4.1 muestra la secuencia $\{v_k\}$ convergiendo por sweeps (partiendo de $v_0 = 0$), y cómo la política greedy asociada a cada estimación ya es casi óptima desde las primeras iteraciones.

---

## (4.2) — Policy Improvement

**Qué representa:** dado el $v_\pi$ de una política, encontrar **otra mejor**. La pregunta concreta: en un estado $s$, ¿conviene desviarse de $\pi(s)$ y elegir una acción $a \neq \pi(s)$? El valor de "hacer $a$ una vez y después seguir $\pi$" es:

$$
q_\pi(s, a) = \sum_{s', r} p(s', r \mid s, a)\, [\, r + \gamma\, v_\pi(s') \,] \tag{4.6}
$$

El criterio clave: si $q_\pi(s, a) > v_\pi(s)$, conviene elegir $a$ siempre que se visite $s$, y esa política nueva es mejor globalmente.

**Teorema de mejora de política.** Sean $\pi$ y $\pi'$ políticas deterministas tales que para todo $s$:

$$
q_\pi(s, \pi'(s)) \geq v_\pi(s) \tag{4.7}
$$

entonces $\pi'$ es tan buena o mejor que $\pi$: $v_{\pi'}(s) \geq v_\pi(s)$ para todo $s$ (ec. 4.8). La demostración: ir expandiendo el lado $q_\pi$ con (4.6) y reaplicando (4.7) una y otra vez hasta alcanzar $v_{\pi'}(s)$.

**Política greedy.** El caso extremo: cambiar *todos* los estados, eligiendo en cada uno la acción que luce mejor según $q_\pi$:

$$
\pi'(s) = \arg\max_a q_\pi(s, a) \tag{4.9}
$$

Por construcción cumple (4.7), así que $\pi' \geq \pi$. Llamamos **policy improvement** al proceso de derivar una política mejor haciendo *greedy* respecto a $v_\pi$.

**Idea high-level:** si la nueva greedy es *tan buena pero no mejor* que la vieja ($v_\pi = v_{\pi'}$), entonces (4.9) es realmente la ecuación de Bellman de optimalidad (4.1): ya sos óptimo. Es decir, hay mejora estricta siempre, salvo que ya estés en el óptimo. **Caso estocástico:** si hay empates en el $\arg\max$, la nueva política puede repartir probabilidad entre las acciones empatadas (las subóptimas quedan en probabilidad cero).

**Ejemplo visual:** en la figura 4.1, pasar de la política aleatoria a la greedy de $v_\pi$ salta de valores de hasta −14 a valores entre −1 y −3 en todos los estados ($v_{\pi'} \geq v_\pi$ en todas partes).

---

## (4.3) — Policy Iteration

**Qué representa:** el ciclo **evaluar ⟶ mejorar ⟶ evaluar ⟶ mejorar…** hasta converger:

$$
\pi_0 \xrightarrow{\text{eval}} v_{\pi_0} \xrightarrow{\text{mejora}} \pi_1 \xrightarrow{\text{eval}} v_{\pi_1} \xrightarrow{\text{mejora}} \pi_2 \to \cdots \to \pi_*
$$

Cada política mejora estrictamente a la anterior (salvo que ya sea óptima). Como un MDP finito tiene **finitas** políticas, el proceso converge a la política óptima en **tiempo finito**. Cada evaluación arranca del $v$ de la política anterior (no de cero), lo que acelera mucho la convergencia.

**Pseudocódigo del algoritmo (de la caja del libro):**
1. **Inicialización:** $V(s)$ y $\pi(s)$ arbitrarios para todo $s$.
2. **Policy evaluation:** iterar (4.5) hasta que $\max_s |v_{k+1}(s) - v_k(s)| < \theta$.
3. **Policy improvement:** fijar $\pi'(s) = \arg\max_a \sum_{s',r} p(s',r\mid s,a)\,[r + \gamma V(s')]$; si $\pi' = \pi$, devolver $\pi \approx \pi_*$; si no, volver al paso 2 con $\pi'$.

**Ejemplo 4.2: Jack's car rental.** Dos sucursales de alquiler de autos. Marco temporal: días; estado = número de autos en cada ubicación al final del día; acción = autos netos movidos durante la noche (máx. 5, con costo $2 por auto); ingresos: +$10 por cada alquiler; llegadas y devoluciones son **Poisson** ($\lambda = 3$ y $4$ para alquileres, $3$ y $2$ para devoluciones); tope de 20 autos por ubicación; $\gamma = 0.9$; tarea continua. Policy iteration, partiendo de "no mover autos", converge a la política óptima en **sorprendentemente pocas iteraciones** (figura 4.2) aun con $21 \times 21$ estados y 11 acciones posibles por estado.

**Ejercicios a destacar:**
- **4.4:** el pseudocódigo del libro tiene un *bug sutil* — si las políticas alternan entre dos igualmente buenas, el algoritmo podría no terminar; hay que modificar el criterio de cierre.
- **4.5:** cómo definir policy iteration para *action values* ($q_*$): el algoritmo análogo al de $v_*$; el libro pide prestarle especial atención porque esa idea se usa en todo lo que sigue.
- **4.7 (programación):** re-resolver Jack's car rental con una empleada que mueve un auto gratis por noche y costo extra de estacionamiento si hay >10 autos en una ubicación (no linealidades que solo DP maneja bien).

---

## (4.4) — Value Iteration

**Qué representa:** la versión "perezosa" de policy iteration: **cortar la policy evaluation después de un solo sweep**. Evaluación truncada y mejora se fusionan en una sola actualización:

$$
v_{k+1}(s) = \max_a \sum_{s', r} p(s', r \mid s, a)\, [\, r + \gamma\, v_k(s') \,] \tag{4.10}
$$

**Idea high-level:**
- (4.10) es simplemente la **ecuación de optimalidad de Bellman (4.1) convertida en regla de actualización**. Comparada con la actualización de policy evaluation (4.5), la única diferencia es el $\max_a$ en lugar del promedio según $\pi$.
- Converge a $v_*$ bajo las mismas condiciones que garantizan la existencia de $v_*$. En la práctica se corta cuando el cambio en un sweep es menor a un $\theta$.
- Cada sweep hace "un poco de evaluación y un poco de mejora". Toda la familia de *truncated policy iteration* son secuencias de sweeps de evaluación y de value iteration mezclados: como el $\max$ es la única diferencia entre los dos tipos de actualización, agregarle el $\max$ a algunos sweeps de evaluación basta. Todos convergen a una política óptima para MDPs finitos con descuento.

**Ejemplo 4.3: Gambler's problem.** Un apostador apuesta sobre una secuencia de caras o cecas hasta alcanzar su meta de $100 (recompensa +1) o quedarse sin dinero. Estado = capital $s \in \{1, \ldots, 99\}$; acciones = apuestas $a \in \{0, \ldots, \min(s,\, 100-s)\}$; recompensa +1 solo al llegar a la meta, 0 en todas las demás transiciones; así $v(s) = $ **probabilidad de ganar** desde $s$. Con $p_h$ conocida, toda la dinámica se conoce y value iteration lo resuelve. La figura 4.3 muestra $v$ evolucionando por sweeps y la política final para $p_h = 0.4$: hay toda una familia de políticas óptimas, correspondientes a los empates (ties) en el $\arg\max$ respecto de $v_*$. **Ejercicio 4.8:** ¿por qué la política óptima es tan curiosa (con capital 50 apuesta todo, con 51 no)? **Ejercicio 4.9 (programación):** implementarlo para $p_h = 0.25$ y $0.55$, con dos estados dummy de terminación con valores 0 y 1.

---

## (4.5) — Asynchronous Dynamic Programming

**Qué representa:** los DP clásicos requieren **barridos (sweeps)** completos del set de estados; con $10^{20}$ estados (backgammon) ni siquiera un sweep es posible. Los **métodos asincrónicos** actualizan estados **en cualquier orden**, in-place, con los valores que haya disponibles en el momento — sin sweeps sistemáticos.

**Idea high-level:**
- Requisito de convergencia: cada estado debe actualizarse **infinitas veces** (el orden puede incluso ser estocástico; en el caso episódico sin descuento hay que evitar algunos ordenamientos patológicos, pero es fácil hacerlo).
- No hace falta congelarse en ningún sweep largo: se puede mejorar la política apenas aparece información útil. La flexibilidad se usa para propagar la información de valor de forma eficiente y enfocar las actualizaciones donde importan.
- Permiten **intercalar cómputo con interacción real**: se actualizan estados a medida que el agente los visita, y la información más fresca guía sus decisiones (tema que reaparece en el cap. 8).

*Advertencia de honestidad:* no es magia ni menos cómputo total; solo reorganiza dónde se gasta el esfuerzo.

---

## (4.6) — Generalized Policy Iteration (GPI)

**Qué representa:** la idea unificadora de casi todo RL: **dos procesos interactuando** alrededor de una política aproximada y una función de valor aproximada:
- **Policy evaluation:** dado $\pi$, mover $v$ hacia $v_\pi$.
- **Policy improvement:** dado $v$, hacer $\pi$ greedy respecto a $v$.

En policy iteration alternan completos; en value iteration se pisan (un sweep de evaluación entre cada mejora); en DP asincrónico se intercalan a la granularidad de estados individuales.

**Idea high-level:** da igual la granularidad — **si ambos procesos se estabilizan, la política y el valor son óptimos**: el $v$ se estabiliza solo cuando es consistente con $\pi$, y $\pi$ solo cuando es greedy respecto a $v$; ambas cosas a la vez implican que se cumple la ecuación de Bellman de optimalidad (4.1). La intuición geométrica del libro: los dos procesos tiran hacia dos "rectas" (restricciones) no ortogonales — *compiten* (hacer la política greedy invalida el $v$; hacer $v$ consistente rompe la greedy) pero *cooperan*: el sistema conjunto converge al punto de equilibrio óptimo. Casi todos los métodos de RL se describen como GPI, no solo DP.

---

## (4.7) — Efficiency of Dynamic Programming

**Qué representa:** pese a su fama de caro, DP es **eficiente comparado con otras formas de resolver MDPs**.

- **Tiempo polinomial:** en peor caso, el tiempo es polinomial en el número de estados $n$ y de acciones $k$, con garantía de hallar $\pi_*$ aunque existen $k^n$ políticas deterministas. Es **exponencialmente más rápido que la búsqueda directa** en el espacio de políticas (que tendría que examinarlas exhaustivamente para dar la misma garantía).
- **Vs. programación lineal:** LP da mejores garantías de peor caso en algunos casos, pero se vuelve impracticable a ~100× menos estados que DP.
- **Maldición de la dimensionalidad:** el número de estados suele crecer exponencialmente con la cantidad de variables de estado; es una dificultad *inherente al problema*, no defecto del método (DP la maneja mejor que la búsqueda directa o LP).
- En la práctica se resuelven MDPs con **millones de estados**; policy iteration y value iteration convergen mucho más rápido que su peor caso, sobre todo con buenas inicializaciones. Para espacios gigantes se prefiere DP asincrónico: a lo largo de una trayectoria óptima aparecen pocos estados, y ahí es donde conviene enfocar el cómputo.

---

## (4.8) — Summary y el concepto de *bootstrapping*

**Qué queda del capítulo:**

- **Policy evaluation** (4.1): computar $v_\pi$ iterativamente (predicción).
- **Policy improvement** (4.2): armar una política mejor con greedy a partir de $v_\pi$ (teorema 4.7–4.8).
- **Policy iteration** (4.3) y **value iteration** (4.4): los dos métodos DP por excelencia; con el modelo completo, convergen en forma confiable a $v_*$ y $\pi_*$.
- Todos los métodos DP usan **expected updates**: actualizaciones basadas en todos los sucesores posibles y sus probabilidades, que son las ecuaciones de Bellman vueltas *asignaciones*. Hay cuatro (una por función de valor: $v_\pi, v_*, q_\pi, q_*$), cada una con su backup diagram.
- **GPI** (4.6) como marco mental unificador; **asynchronous DP** (4.5) como variación sin sweeps; **eficiencia** (4.7) como argumento de viabilidad práctica.

**El concepto estrella: bootstrapping.** Todo DP actualiza la estimación de un estado **usando las estimaciones de los sucesores**: "estimás a partir de otras estimaciones". Ese rasgo separa a DP de lo que viene:

- **Cap. 5 (Monte Carlo):** sin modelo **y sin** bootstrapping (usa retornos muestreados de verdad).
- **Cap. 6 (TD learning):** sin modelo, **pero con** bootstrapping (aprende de sus propias estimaciones).

Estas dos propiedades son separables y se combinan de muchas maneras; DP vive en el extremo "modelo completo + bootstrap".

---

## Cómo se conecta con los capítulos 3, 5 y 6

- El cap. **3** te dio las funciones de valor y las ecuaciones de Bellman; el **4** las convierte en **algoritmos de actualización iterativos** que asumen un modelo perfecto ($p$ conocida).
- La ecuación de Bellman (cap. 3) es la matemática; **policy/value iteration** (cap. 4) son su receta computacional; **GPI** es el patrón que unifica a ambos y reaparece como lente para leer todos los métodos del libro.
- La limitación central de DP — *necesita la dinámica completa* — es exactamente lo que los capítulos 5 y 6 van a aflojar: primero sin modelo ni bootstrapping (Monte Carlo), después sin modelo pero con bootstrapping (TD). DP es el piso teórico sobre el que se construye el resto.