import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng(0)

# %%
# → Definir los arms (pdfs)
k = 5
q_star = np.array([1.0, 1.5, 2.0, 1.2, 0.5])  # media real de cada brazo
reward_std = 1.0  # sigma del reward, igual para todos


def pull(arm):
    """Reward de tirar `arm`: ~ N(q_star[arm], reward_std)."""
    return rng.normal(q_star[arm], reward_std)


# %%
# → Definir el agente (la policy): epsilon-greedy
epsilon = 0.1
Q = np.zeros(k)  # estimación del agente para cada brazo
N = np.zeros(k)  # cuántas veces probó cada brazo


def choose_action():
    if rng.random() < epsilon:
        return rng.integers(k)  # explorar
    return np.argmax(Q)         # explotar  ### ojo que no es truly random!


# %%
# → Tener un loop que simule la interacción Agente <-> Arms
n_steps = 1000
rewards = np.zeros(n_steps)

for t in range(n_steps):
    a = choose_action()
    r = pull(a)
    N[a] += 1
    Q[a] += (r - Q[a]) / N[a]  # actualización sample-average
    rewards[t] = r

# %%
# → Evaluar cómo salió
print("q* real:          ", np.round(q_star, 2))
print("Q estimado:        ", np.round(Q, 2))
print("mejor brazo real:  ", np.argmax(q_star))
print("mejor según agente:", np.argmax(Q))

plt.plot(np.cumsum(rewards) / np.arange(1, n_steps + 1))
plt.axhline(q_star.max(), color="k", ls="--", label="mejor q* posible")
plt.xlabel("pasos")
plt.ylabel("reward promedio acumulado")
plt.legend()
plt.show()

# %%
# → Juntar estadística (una corrida sola depende de la semilla)
n_runs = 200
regret_total = []

for _ in range(n_runs):
    Q = np.zeros(k)
    N = np.zeros(k)
    total_reward = 0.0
    for t in range(n_steps):
        a = rng.integers(k) if rng.random() < epsilon else np.argmax(Q)
        r = rng.normal(q_star[a], reward_std)
        N[a] += 1
        Q[a] += (r - Q[a]) / N[a]
        total_reward += r
    regret_total.append(n_steps * q_star.max() - total_reward)

plt.hist(regret_total, bins=20)
plt.xlabel("regret acumulado en T pasos")
plt.ylabel("frecuencia")
plt.title(f"distribución del regret sobre {n_runs} corridas")
plt.show()

# %%
# → Otra policy para los mismos arms: UCB
c = 2.0
Q_ucb = np.zeros(k)
N_ucb = np.zeros(k)


def choose_action_ucb(t):
    if 0 in N_ucb:
        return np.argmin(N_ucb)  # probar cada brazo 1 vez (evita log(t)/0)
    return np.argmax(Q_ucb + c * np.sqrt(np.log(t) / N_ucb))


# %%
# → Loop UCB (mismos arms gaussianos de arriba)
for t in range(1, n_steps + 1):
    a = choose_action_ucb(t)
    r = pull(a)
    N_ucb[a] += 1
    Q_ucb[a] += (r - Q_ucb[a]) / N_ucb[a]

print("Q estimado (UCB):", np.round(Q_ucb, 2))
print("mejor según UCB: ", np.argmax(Q_ucb))
print("mejor real:      ", np.argmax(q_star))
















# %%
# THOMPSON CON BERNOULLI
p_star = np.array([0.5, 0.55, 0.6, 0.52, 0.4])  # prob. real de éxito
alpha = np.ones(k)  # prior Beta(1,1) por brazo
beta = np.ones(k)


def choose_action_thompson():
    theta_sample = rng.beta(alpha, beta)  # sample del posterior
    return np.argmax(theta_sample)


# %%
# → Loop Thompson
for _ in range(n_steps):
    a = choose_action_thompson()
    r = rng.binomial(1, p_star[a])
    if r:
        alpha[a] += 1
    else:
        beta[a] += 1

media_posterior = alpha / (alpha + beta)
print("p* real:         ", np.round(p_star, 2))
print("media posterior: ", np.round(media_posterior, 2))
print("mejor Thompson:  ", np.argmax(media_posterior))
print("mejor real:      ", np.argmax(p_star))
