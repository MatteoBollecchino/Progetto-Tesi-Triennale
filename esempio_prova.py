import gymnasium as gym
from gymnasium import spaces
import numpy as np

class StackelbergSecurityGameEnv(gym.Env):
    def __init__(self, n_targets=3):
        super(StackelbergSecurityGameEnv, self).__init__()
        self.n_targets = n_targets
        
        # Difensore: distribuzione di probabilità sulla protezione dei target
        self.action_space = spaces.Box(low=0, high=1, shape=(n_targets,), dtype=np.float32)
        
        # Osservazione fittizia (non è rilevante in SSG statico)
        self.observation_space = spaces.Box(low=0, high=1, shape=(n_targets,), dtype=np.float32)
        
        # Reward matrix: righe = target, colonne = [reward if defended, reward if attacked]
        self.defender_rewards = np.array([[1, -10], [1, -5], [1, -1]])  # esempio
        self.attacker_rewards = np.array([[-1, 10], [-1, 5], [-1, 1]])

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        return np.zeros(self.n_targets, dtype=np.float32), {}

    def step(self, action):
        # Normalizza la strategia del difensore (probabilità)
        strategy = action / np.sum(action)

        # L'attaccante osserva la strategia e sceglie il miglior target
        expected_utilities = []
        for i in range(self.n_targets):
            prob_defended = strategy[i]
            u = prob_defended * self.attacker_rewards[i][0] + (1 - prob_defended) * self.attacker_rewards[i][1]
            expected_utilities.append(u)
        
        # Attaccante sceglie il target con reward massimo
        target_attacked = np.argmax(expected_utilities)
        prob_defended = strategy[target_attacked]

        # Calcolo del reward per il difensore
        defender_reward = prob_defended * self.defender_rewards[target_attacked][0] + \
                          (1 - prob_defended) * self.defender_rewards[target_attacked][1]
        
        done = True  # gioco a un passo
        return np.zeros(self.n_targets, dtype=np.float32), defender_reward, done, False, {
            "target_attacked": target_attacked,
            "strategy": strategy
        }

if __name__ == "__main__":
    env = StackelbergSecurityGameEnv(n_targets=3)

    obs, _ = env.reset()
    strategy = np.array([0.5, 0.3, 0.2], dtype=np.float32)  # esempio: proteggere i target 0,1,2 con queste probabilità
    obs, reward, done, _, info = env.step(strategy)

    print("Reward Difensore:", reward)
    print("Target Attaccato:", info["target_attacked"])
    print("Strategia Normalizzata:", info["strategy"])

