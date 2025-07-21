import numpy as np
import networkx as nx 
import random

class Utils:
    # Restituisce tutti i path che hanno origine in 'source'
    def get_paths_from_source(graph: nx.DiGraph, node_source: str) -> list:

        paths = list()

        for node in graph.nodes:
            target = node
            paths = paths + list(nx.all_simple_paths(graph, source=node_source, target=target))

        return paths
    
    # Restituisce tutti i path che partono da tutti i nodi in source_list
    def get_all_paths(graph: nx.DiGraph, source_list: list) -> list:

        paths = list()
        
        for node_source in source_list:
            paths = paths + Utils.get_paths_from_source(graph, node_source)

        return paths

    
    # Metodo per la traduzione della tabella del paper del lollo
    # node_source -> nodo dal quale esce l'arco, afr -> probabilità arco uscente
    def get_node_risk(node_source: str, afr: float) -> float:
        impact_norm = (node_source['impact'] - 1) / 9

        # oppure (impact/10 + afr)/2
        return round(afr * 0.6 + impact_norm * 0.4, 4)

    # Restituisce il rischio del path passato per parametro
    def get_path_risk(graph: nx.DiGraph, path: list) -> float:
        risk_values = list()

        # Path di lunghezza 1 = loop
        if len(path) == 1:
            return 0

        for i in range(len(path)-1):
            node = path[i]
            successor = path[i+1]
            afr = graph.get_edge_data(node,successor)['weight']
            risk_values.append(Utils.get_node_risk(graph.nodes[node], afr))

        return max(risk_values)
    
    # Restituisce il path che tra tutti ha il rischio maggiore associato
    def get_maximum_risk_path(graph: nx.DiGraph, node_source: str) -> list:
        paths = Utils.get_paths_from_source(graph, node_source)
        risk_paths = list()

        for path in paths:
            risk_paths.append(Utils.get_path_risk(graph, path))

        index_max_risk_path = risk_paths.index(max(risk_paths))

        return paths[index_max_risk_path]
    
