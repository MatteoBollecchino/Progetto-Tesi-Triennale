import numpy as np
import networkx as nx 

class Utils:
    # Metodo privato ???
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

        # si restituisce il max o la somma dei valori in risk_values?
        return max(risk_values)
    
    # Restituisce il path che tra tutti ha il rischio maggiore associato
    def get_maximum_risk_path(graph: nx.DiGraph, source_list: list) -> list:

        paths = Utils.get_all_paths(graph, source_list)
        risk_list = list()

        for path in paths:
            risk_list.append(Utils.get_path_risk(graph, path))

        index_max_risk_path = risk_list.index(max(risk_list))

        return paths[index_max_risk_path]
    

    # Restituisce un booleano che indichi il fatto, o meno, che grafo e contromisure siano state modificate,
    # il grafo modificato in seguito all'applicazione delle contromisure 
    # e la lista di contromisure aggiornata
    def apply_countermeasures(graph: nx.DiGraph, source_list:list, countermeasures: list) -> tuple[bool, nx.DiGraph, list] :

        max_risk_path = Utils.get_maximum_risk_path(graph, source_list)

        for i in range(len(max_risk_path)-1):
            node = max_risk_path[i]
            successor = max_risk_path[i+1]
            found, cost, eff = Utils.__search_countermeasure(node, successor)

            # Si ritornano gli elementi inalterati
            if not found:
                return False, graph, countermeasures
            
            

        pass

    # Restituice i valori che caratterizzano la contromisura (ad esclusione dei nodi che sono già noti)
    def __search_countermeasure(node_1: str, node_2: str) -> tuple[bool, int, float]:
        pass

    def __apply_countermeasure():
        pass
