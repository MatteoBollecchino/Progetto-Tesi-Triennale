import gymnasium as gym
import networkx as nx
from utils import Utils as ut

class StackelbergSecurityGameEnv(gym.Env):
    def __init__(self, graph: nx.DiGraph, source_list: list, budget_defender : int, countermeasures: list):

        super(StackelbergSecurityGameEnv, self).__init__()
        self.graph = graph # DiGraph
        self.source_list = source_list # Lista nodi sorgente
        self.budget_defender = budget_defender # Intero

        # Liste di quartuple (costo, efficacia sull'arco, nodo_origine, nodo_destinazione)
        self.remaining_countermeasures = countermeasures # Lista delle contromisure rimanenti alla fine del gioco

        self.risk_threshold = 3 # Soglia di rischio tollerabile
        self.applied_countermeasures = list() # Lista delle contromisure applicate durante i vari passi

        # Cambia dopo che il difensore applica delle contromisure
        self.maximum_risk_path = ut.get_maximum_risk_path(self.graph, self.source_list)

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        return 0, {}

    # DA MODIFICARE
    def step(self, action) -> tuple[bool, int, int, list]:

        done = False  # Gioco in più passi
        
        # Strategia difensore = action
        self.graph = action[1] # si aggiorna il grafo

        self.applied_countermeasures = self.remaining_countermeasures + [x for x in self.countermeasures if x not in action[2]]
        
        print(self.applied_countermeasures)
        self.remaining_countermeasures = action[2] # si aggiorna le contromisure disponibili
        self.budget_defender = action[3] # si aggiorna il budget del difensore

        # L'attaccante osserva la strategia e sceglie il miglior path target possibile
        self.maximum_risk_path = ut.get_maximum_risk_path(self.graph, self.source_list)

        new_graph_risk = ut.get_graph_risk(self.graph, self.source_list)

        # Terminazione gioco: la lista delle contromisure è vuota, il rischio del grafo è sotto una soglia tollerabile 
        if (len(self.countermeasures) == 0) or (new_graph_risk <= self.risk_threshold):
            done = True

        return done, new_graph_risk, self.budget_defender, self.applied_countermeasures
    
    # Serve all'utente per ripulire l'enviroment e chiuderlo
    def close(self):
        self.graph = None
        self.source_list = None
        self.budget_defender = 0
        self.countermeasures = list()
        self.remaining_countermeasures = list()
        self.maximum_risk_path = list()