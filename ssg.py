import gymnasium as gym
from gymnasium import spaces
import numpy as np
import networkx as nx
from utils import Utils as ut

class StackelbergSecurityGameEnv(gym.Env):
    def __init__(self, graph: nx.DiGraph, source_list: list, budget_defender : int, countermeasures: list):
        super(StackelbergSecurityGameEnv, self).__init__()
        self.graph = graph # DiGraph
        self.source_list = source_list # Lista nodi sorgente
        self.budget_defender = budget_defender # intero
        self.countermeasures = countermeasures # liste di coppie (costo, efficacia sull'arco)
        self.n_targets = graph.number_of_nodes()
        
        # Difensore: distribuzione di probabilità sulla protezione dei target
        self.action_space = spaces.Box(low=0, high=1, shape=(self.n_targets,), dtype=np.float32)
        
        # Osservazione fittizia (non è rilevante in SSG statico)
        self.observation_space = spaces.Box(low=0, high=1, shape=(self.n_targets,), dtype=np.float32)

        # tutti i path che hanno origine da OWS e da EWS -> tutti i possibili path di attacco
        # all_paths ha tipo: lista di liste
        all_paths = ut.get_all_paths(self.graph, self.source_list)

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
        
        done = False  # gioco in più passi
        return np.zeros(self.n_targets, dtype=np.float32), defender_reward, done, False, {
            "target_attacked": target_attacked,
            "strategy": strategy
        }