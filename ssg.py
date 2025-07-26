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
        self.countermeasures = countermeasures # liste di quartuple (costo, efficacia sull'arco, nodo_origine, nodo_destinazione)
        self.n_targets = graph.number_of_nodes() # da eliminare nella versione finale
        self.remaining_countermeasures = list() # lista delle contromisure rimanenti alla fine del gioco

        # tutti i path che hanno origine da OWS e da EWS -> tutti i possibili path di attacco
        # all_paths ha tipo: lista di liste
        all_paths = ut.get_all_paths(self.graph, self.source_list)

        # cambia dopo che il difensore applica delle contromisure
        self.maximum_risk_path = ut.get_maximum_risk_path(self.graph, source_list)

        # Si mantiene solo il reward dell'attaccante poiché il gioco è a somma zero

        # lista di liste (formate da 2 elementi: path + rischio del path)
        self.attacker_rewards = list()

        for path in all_paths:
            self.attacker_rewards.append([path, ut.get_path_risk(graph, path)])


    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        return np.zeros(self.n_targets, dtype=np.float32), {}

    # DA MODIFICARE
    def step(self, action):

        """
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
        """
        # Strategia difensore

        # L'attaccante osserva la strategia e sceglie il miglior target

        # Calcolo del reward dell'attaccante

        # Terminazione gioco: la lista delle contromisure è vuota, il rischio del grafo è sotto una soglia tollerabile 
        done = False  # gioco in più passi
    
    # Serve all'utente per ripulire l'enviroment e chiuderlo
    def close(self):
        pass