import numpy as np
import networkx as nx 

class Utils:
    def get_paths(grafo: nx.DiGraph, origine):

        paths = list()
        
        for node in grafo.nodes:
            target = node
            paths = paths + list(nx.all_simple_paths(grafo, source=origine, target=target))

        return paths