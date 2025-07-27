import networkx as nx 

class Utils:
    # Restituisce tutti i path che hanno origine in 'source'
    @staticmethod
    def get_paths_from_source(graph: nx.DiGraph, node_source: str) -> list:

        paths = list()

        # Non si considerano paths di lunghezza 1
        for node in graph.nodes:
            target = node
            simple_paths = list(nx.all_simple_paths(graph, source=node_source, target=target))

            paths = paths + list(filter(lambda x: len(x) != 1, simple_paths))

        return paths
    
    # Restituisce tutti i path che partono da tutti i nodi in source_list
    @staticmethod
    def get_all_paths(graph: nx.DiGraph, source_list: list) -> list:

        paths = list()
        
        for node_source in source_list:
            paths = paths + Utils.get_paths_from_source(graph, node_source)

        return paths

    
    # Metodo per la traduzione della tabella del paper del lollo
    # node_source -> nodo dal quale esce l'arco, afr -> probabilità arco uscente
    @staticmethod
    def get_node_risk(node_source: str, afr: float) -> float:

        impact = node_source['impact']

        return round(afr * impact, 4)

    # Restituisce il rischio del path passato per parametro
    @staticmethod
    def get_path_risk(graph: nx.DiGraph, path: list) -> float:
        risk_values = list()

        for i in range(len(path)-1):
            node = path[i]
            successor = path[i+1]
            afr = graph.get_edge_data(node,successor)['weight']
            risk_values.append(Utils.get_node_risk(graph.nodes[node], afr))

        # Si restituisce il massimo dei valori in risk_values
        return max(risk_values)
    
    # Restituisce il rischio associato al grafo (massimo tra i rischi dei path)
    @staticmethod
    def get_graph_risk(graph: nx.DiGraph, source_list: list) -> int:

        paths = Utils.get_all_paths(graph, source_list)
        risk_list = list()

        for path in paths:
            risk_list.append(Utils.get_path_risk(graph, path))

        return max(risk_list)
    
    # Restituisce il path che tra tutti ha il rischio maggiore associato (scelta di un attaccante razionale)
    @staticmethod
    def get_maximum_risk_path(graph: nx.DiGraph, source_list: list) -> list:

        paths = Utils.get_all_paths(graph, source_list)
        risk_list = list()

        for path in paths:
            risk_list.append(Utils.get_path_risk(graph, path))

        index_max_risk_path = risk_list.index(max(risk_list))

        return paths[index_max_risk_path]
    

    # Restituisce un booleano che indichi il fatto, o meno, che grafo e contromisure siano state modificate,
    # il grafo modificato in seguito all'applicazione delle contromisure, la lista di contromisure aggiornata
    # e il budget rimanente dopo l'applicazione delle contromisure
    @staticmethod
    def apply_countermeasures(graph: nx.DiGraph, source_list:list, countermeasures: list, budget: int) -> tuple[bool, nx.DiGraph, list, int] :

        max_risk_path = Utils.get_maximum_risk_path(graph, source_list)

        # Viene posto a True in caso venga applicata almeno una contromisura
        modified = False

        for i in range(len(max_risk_path)-1):
            node = max_risk_path[i]
            successor = max_risk_path[i+1]
            found, countermeasure = Utils._search_countermeasure(node, successor, countermeasures)

            # Se non si trova una contromisura si passa all'arco successivo
            if not found:
                continue

            # Rischio prima dell'applicazione delle contromisure
            previous_risk = Utils.get_graph_risk(graph, source_list)

            # Modifica grafo
            new_graph = graph.copy()
            reduction = round(graph[countermeasure[2]][countermeasure[3]]['weight']*countermeasure[1], 4)
            new_graph[countermeasure[2]][countermeasure[3]]['weight'] = new_graph[countermeasure[2]][countermeasure[3]]['weight'] - reduction
            
            # Controllo cambiamento rischio
            changed_risk = Utils.get_graph_risk(new_graph, source_list)
            
            # Il rischio non è cambiato, quindi si salta all'arco successivo senza applicare nulla
            if previous_risk == changed_risk:
                continue
            
            # Se li grafo è cambiato, allora lo si aggiorna effettivamente
            # In questo modo ci si assicura che le modifiche al grafo siano significative e al prezzo minore possibile
            graph = new_graph
        
            # Modifica budget
            new_budget = budget - countermeasure[0]
            if new_budget >= 0:
                budget = new_budget
            else:
                continue
        
            # Modifica lista contromisure
            countermeasures.remove(countermeasure)
            
            modified = True

        return modified, graph, countermeasures, budget

    # Restituice costo ed effcicacia della contromisura (i nodi sono esclusi perché già noti)
    @staticmethod
    def _search_countermeasure(node_1: str, node_2: str, countermeasures: list) -> tuple[bool, int, float]:
        
        found_list = list()

        for countermeasure in countermeasures:
            if countermeasure[2] == node_1 and countermeasure[3] == node_2:
                found_list.append(countermeasure)

        if len(found_list) != 0:
            found = True
        else:
            found = False
            return found, None

        # Fra tutte le contromisure trovate si sceglie quella con costo minimo
        countermeasure_min_cost = min(found_list, key=lambda x: x[0])

        return found, countermeasure_min_cost
