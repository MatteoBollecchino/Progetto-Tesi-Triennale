import numpy as np
import networkx as nx 
import random

class Utils:
    def get_paths(grafo: nx.DiGraph, origine):

        paths = list()

        for node in grafo.nodes:
            target = node
            paths = paths + list(nx.all_simple_paths(grafo, source=origine, target=target))

        return paths
    
    # Metodo per la traduzione della tabella del paper del lollo
    # node_source -> nodo dal quale esce l'arco, afr -> probabilità arco uscente
    def get_node_risk(node_source, afr):
        impact_norm = (node_source['impact'] - 1) / 9

        # oppure (impact/10 + afr)/2
        return round(afr * 0.6 + impact_norm * 0.4, 4)

    def get_path_risk(graph: nx.DiGraph, path: list):
        risk_values = list()

        for i in range(len(path)-1):
            node = path[i]
            successor = path[i+1]
            afr = graph.get_edge_data(node,successor)['weight']
            risk_values = risk_values + Utils.get_node_risk(graph.nodes[node], afr)

        return max(risk_values)

    def get_maximum_risk_path():
        pass