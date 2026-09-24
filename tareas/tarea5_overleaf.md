A diferencia de los modelos anteriores, Los métodos Monte Carlo no necesitan un modelo y puede aprender solo de la experiencia.

Esto nos da algunas ventajas:
\begin{itemize}
    \item No necesitamos la distribución de probabilidad exacta de las transiciones sino que nos basta con aproximarla con sampleos
    \item Es necesario que la tarea sea episódica (El learning es episodio a episodio no step a step)
    \item El learning ahora toma en cuenta toda la cadena de acciones de un episodio y no una sola, también puede aprender evaluando un subset de eventos en vez de tener que ver todos
    \item Al igual que en dynamic programming, Usamos el framework GPI mejorando los value functions promediando retornos observados
\end{itemize}

Para cada $v_\pi(s)$ estimamos su valor promediando los retornos observados cuando pasamos por el estado $s$:

\textbf{First Visit MC:} Promediamos los retornos solamente mirando las primeras veces que pasamos por $s$ en el episodio

\textbf{Every Visit MC:} Promediamos los retornos mirando todas las veces que pasamos por $s$ en el episodio

\medskip

Ambos convergen a $v_\pi(s)$ con un número suficientemente grande de muestras. A diferencia de DP el diagrama episódico solamente muestra una secuencia de acciones desde el root node hasta el final, en vez de todas las posibles acciones a cada paso. La estimación de un estado es independiente de las demás y no se construye usando la de sucesores y es menos costoso ya que podemos evaluar un estado sin evaluar el resto. Aplicado GPI a esta metodología es similar a DP solo que acá en vez de mejorar los value functions mejoramos los action Values

\begin{align}
\pi'(s) = \arg\max_a q(a, s) \tag{5.1}
\end{align}

para cada $s$, sin necesitar $p$. Y el \textbf{teorema de mejora de política} (sección 4.2) garantiza que si

\begin{align}
q_\pi(s, \pi'(s)) \geq v_\pi(s) \quad \forall s \tag{5.2}
\end{align}

entonces $\pi' \geq \pi$ (mejora estricta salvo que ya sea óptimo). Así, con exploring starts + evaluación exacta, el proceso converge a $\pi_*$ y $q_*$ \textbf{con solo episodios muestreados}.

\medskip

Tras cada episodio, usamos sus retornos para evaluar y luego mejorar la política en los estados visitados. Ese algoritmo es \textbf{Monte Carlo ES (Exploring Starts)}:

\begin{enumerate}
    \item Inicializar $\pi(s)$ y $Q(s,a)$ arbitrarios; listas $Returns(s,a)$ vacías.
    \item Elegir $S_0, A_0$ al azar (todos los pares con probabilidad $> 0$).
    \item Generar el episodio siguiendo $\pi$; recorrerlo hacia atrás con $G \leftarrow \gamma G + R_{t+1}$.
    \item Para cada par $(S_t, A_t)$ que no haya aparecido antes en el episodio: agregar $G$ a sus retornos, actualizar $Q$ al promedio, y fijar $\pi(S_t) \leftarrow \arg\max_a Q(S_t, a)$.
\end{enumerate}

\textbf{Propiedad clave:} MC ES \textbf{no puede converger a una política subóptima} --- si lo hiciera, $Q$ convergería a \textit{esa} política y eso a su vez forzaría un cambio de política. Solo hay estabilidad cuando política y valor son óptimos.

\medskip

Como no tenemos Modelo tenemos que estimar los pares Estado-Valor en vez de el valor del Estado (Ya que no sabemos a qué estado $s'$ nos va a llevar la acción $a$)

y esto puede resultar un problema ya que puede darse el caso que nunca evaluemos algunos Estado-Valores y por ende no tengamos evidencia para estimar esos casos, Por eso hay que asegurarnos de garantizar exploración y visitar todos los estados

\medskip

Para abordar el problema de los pares Estado-Valor que nunca sean visitados y garantizar exploración vamos a implementar una Política On-Policy y Off-Policy:

\begin{itemize}
    \item La policy On-Policy va a ser una $\varepsilon$-soft que va a ejecutar acciones al azar algunas veces y otras veces va a ejecutar acciones greedy sobre $Q(a,s)$. Esta policy On garantiza que vamos a explorar siempre
    \item la Off-Policy que va a aprender de los datos generados por la primera. Esta va a ser una policy greedy sobre $Q(a,s)$
\end{itemize}

También se llama a estas policies Behaviour (on policy) y Target (off policy) porque vamos a aprender la policy óptima (off) usando información generada por la de behaviour (on). Algo necesario de esto es que Condición de coverage: toda acción posible bajo la política off sea posible en la política on

\medskip

El truco para poder estimar los Estado-Valor de la política target usando los datos de la behaviour es usar Importance Sampling ya que si promediáramos los retornos estaríamos estimando $b$ y no $\pi$

\begin{align}
\rho_{t:T-1} = \prod_{k=t}^{T-1} \frac{\pi(A_k \mid S_k)}{b(A_k \mid S_k)} \tag{5.3}
\end{align}

