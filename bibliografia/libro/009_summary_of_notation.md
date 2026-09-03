# Summary of Notation

Capital letters are used for random variables, whereas lower case letters are used for the values of random variables and for scalar functions. Quantities that are required to be real-valued vectors are written in bold and in lower case (even if random variables). Matrices are bold capitals.

|  |  |
| --- | --- |
| ≐ | equality relationship that is true by definition |
| ≈ | approximately equal |
| ∝ | proportional to |
| Pr{*X = x*} | probability that a random variable *X* takes on the value *x* |
| *X ∼ p* | random variable *X* selected from distribution *p*(*x*) ≐ Pr{*X =x*} |
| 𝔼[*X*] | expectation of a random variable *X*, i.e., |
| arg max*a* *f*(*a*) | a value of *a* at which *f*(*a*) takes its maximal value |
| ln *x* | natural logarithm of *x* |
| *e**x* | the base of the natural logarithm, *e* ≈ 2.71828, carried to power *x*; *e*ln *x* = *x* |
| ℝ | set of real numbers |
| *f* : 𝒳 *→* 𝒴 | function *f* from elements of set 𝒳 to elements of set 𝒴 |
| ← | assignment |
| (*a, b*] | the real interval between *a* and *b* including *b* but not including *a* |
| *ε* | probability of taking a random action in an *ε*-greedy policy |
| *α, β* | step-size parameters |
| *γ* | discount-rate parameter |
| *λ* | decay-rate parameter for eligibility traces |
| 𝟙*predicate* | indicator function (𝟙*predicate* ≐ 1 if the *predicate* is true, else 0) |
| In a multi-arm bandit problem: | |
| *k* | number of actions (arms) |
| *t* | discrete time step or play number |
| *q*\*(*a*) | true value (expected reward) of action *a* |
| *Q**t*(*a*) | estimate at time *t* of *q*\*(*a*) |
| *N**t*(*a*) | number of times action *a* has been selected up prior to time *t* |
| *H**t*(*a*) | learned preference for selecting action *a* at time *t* |
| *π**t*(*a*) | probability of selecting action *a* at time *t* |
| *R**t* | estimate at time *t* of the expected reward given *π**t* |
| In a Markov Decision Process: | |
| *s, s*′ | states |
| *a* | an action |
| *r* | a reward |
| 𝒮 | set of all nonterminal states |
| 𝒮+ | set of all states, including the terminal state |
| 𝒜(*s*) | set of all actions available in state *s* |
| ℛ | set of all possible rewards, a finite subset of ℝ |
| ⊂ | subset of (e.g., ℛ ⊂ ℝ) |
| ∈ | is an element of; e.g. (*s* ∈ 𝒮, *r* ∈ ℛ) |
| |𝒮| | number of elements in set 𝒮 |
| *t* | discrete time step |
| *T, T*(*t*) | final time step of an episode, or of the episode including time step *t* |
| *A**t* | action at time *t* |
| *S**t* | state at time *t*, typically due, stochastically, to *S**t*−1 and *A**t*−1 |
| *R**t* | reward at time *t*, typically due, stochastically, to *S**t*−1 and *A**t*−1 |
| *π* | policy (decision-making rule) |
| *π*(*s*) | action taken in state *s* under *deterministic* policy *π* |
| *π*(*a*|*s*) | probability of taking action *a* in state *s* under *stochastic* policy *π* |
| *G**t* | return following time *t* |
| *h* | horizon, the time step one looks up to in a forward view |
| *G**t*:*t*+*n*, *G**t*:*h* | *n*-step return from *t* + 1 to *t* + *n*, or to *h* (discounted and corrected) |
| *G**t*:*h* | flat return (undiscounted and uncorrected) from *t* + 1 to *h* (Section 5.8) |
|  | *λ*-return (Section 12.1) |
|  | truncated, corrected *λ*-return (Section 12.3) |
|  | *λ*-return, corrected by estimated state, or action, values (Section 12.8) |
| *p*(*s*′*, r* | *s, a*) | probability of transition to state *s*′ with reward *r*, from state *s* and action *a* |
| *p*(*s*′ | *s, a*) | probability of transition to state *s*′, from state *s* taking action *a* |
| *r*(*s, a*) | expected immediate reward from state *s* after action *a* |
| *r*(*s, a, s*′) | expected immediate reward on transition from *s* to *s*′ under action *a* |
| *vπ*(*s*) | value of state *s* under policy *π* (expected return) |
| *v*\*(*s*) | value of state *s* under the optimal policy |
| *qπ*(*s, a*) | value of taking action *a* in state *s* under policy *π* |
| *q*\*(*s, a*) | value of taking action *a* in state *s* under the optimal policy |
| *V*, *V**t* | array estimates of state-value function *vπ* or *v*\* |
| *Q*, *Q**t* | array estimates of action-value function *qπ* or *q*\* |
| *V**t*(*s*) | expected approximate action value; for example, |
| *U**t* | target for estimate at time *t* |
| *δ**t* | temporal-difference (TD) error at *t* (a random variable) (Section 6.1) |
|  | state- and action-specific forms of the TD error (Section 12.9) |
| *n* | in *n*-step methods, *n* is the number of steps of bootstrapping |
|  | *μ*-weighted squared norm of value function *v*, i.e., |
| *d* | dimensionality—the number of components of **w** |
| *d*′ | alternate dimensionality—the number of components of ***θ*** |
| **w**, **w***t* | *d*-vector of weights underlying an approximate value function |
| *w**i**, w**t, i* | *i*th component of learnable weight vector |
| (*s,* **w**) | approximate value of state *s* given weight vector **w** |
| *v***w**(*s*) | alternate notation for  (*s,* **w**) |
| (*s, a,* **w**) | approximate value of state–action pair *s, a* given weight vector **w** |
| ∇ (*s,* **w**) | column vector of partial derivatives of  (*s,* **w**) with respect to **w** |
| ∇ (*s, a,* **w**) | column vector of partial derivatives of  (*s, a,* **w**) with respect to **w** |
| **x**(*s*) | vector of features visible when in state *s* |
| **x**(*s, a*) | vector of features visible when in state *s* taking action *a* |
| *x**i*(*s*)*, x**i*(*s, a*) | *i*th component of vector **x**(*s*) or **x**(*s, a*) |
| **x***t* | shorthand for **x**(*S**t*) or **x**(*S**t**, A**t*) |
| **w**⊤**x** | inner product of vectors, ; for example,  (*s,* **w**) ≐ **w**⊤**x**(*s*) |
| **v**, **v***t* | secondary *d*-vector of weights, used to learn **w** (Chapter 11) |
| **z***t* | *d*-vector of eligibility traces at time *t* (Chapter 12) |
| ***θ***, ***θ****t* | parameter vector of target policy (Chapter 13) |
| *π*(*a*|*s,* ***θ***) | probability of taking action *a* in state *s* given parameter vector ***θ*** |
| *π****θ*** | policy corresponding to parameter ***θ*** |
| ∇*π*(*a*|*s,* ***θ***) | column vector of partial derivatives of *π*(*a*|*s,* ***θ***) with respect to ***θ*** |
| *J*(***θ***) | performance measure for the policy *π****θ*** |
| ∇*J*(***θ***) | column vector of partial derivatives of *J*(***θ***) with respect to ***θ*** |
| *h*(*s, a,* ***θ***) | preference for selecting action *a* in state *s* based on ***θ*** |
| *b*(*a*|*s*) | behavior policy used to select actions while learning about target policy *π* |
| *b*(*s*) | a baseline function *b* : 𝒮 ⟼ ℝ for policy-gradient methods |
| *b* | branching factor for an MDP or search tree |
| *ρ**t*:*h* | importance sampling ratio for time *t* through time *h* (Section 5.5) |
| *ρ**t* | importance sampling ratio for time *t* alone, *ρ**t* ≐ *ρ**t*:*t* |
| *r*(*π*) | average reward (reward rate) for policy *π* (Section 10.3) |
| *R**t* | estimate of *r*(*π*) at time *t* |
| *μ*(*s*) | on-policy distribution over states (Section 9.2) |
| ***μ*** | |𝒮|-vector of the *μ*(*s*) for all *s* ∈ 𝒮 |
|  | *μ*-weighted norm of value function *v*, i.e., |
|  | (Section 11.4) |
| *η*(*s*) | expected number of visits to state *s* per episode (page 199) |
| Π | projection operator for value functions (page 268) |
| *Bπ* | Bellman operator for value functions (Section 11.4) |
| *A* | *d* × *d* matrix |
| *b* | *d*-dimensional vector *b* ≐ 𝔼[*R**t*+1**x***t*] |
| **w**TD | TD fixed point **w**TD ≐ **A**−1**b** (a *d*-vector, Section 9.4) |
| **I** | identity matrix |
| **P** | |𝒮| × |𝒮| matrix of state-transition probabilities under *π* |
| *D* | |𝒮| × |𝒮| diagonal matrix with ***μ*** on its diagonal |
| *X* | |𝒮| × *d* matrix with the **x**(*s*) as its rows |
| VE(**w**) | mean square value error  (Section 9.2) |
| *δ***w**(*s*) | Bellman error (expected TD error) for *v***w** at state *s* (Section 11.4) |
| *δ***w**, BE | Bellman error vector, with components *δ***w**(*s*) |
| BE(**w**) | mean square Bellman error |
| PBE(**w**) | mean square projected Bellman error |
| TDE(**w**) | mean square temporal-difference error  (Section 11.5) |
| RE(**w**) | mean square return error (Section 11.6) |
