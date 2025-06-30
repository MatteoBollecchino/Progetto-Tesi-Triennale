import StackelbergSecurityGameEnv as ssg
import GrafoPesato as gp
import numpy as np
import networkx as nx

if __name__ == "__main__":
    env = ssg.StackelbergSecurityGameEnv(n_targets=3)

    obs, _ = env.reset()
    
    # esempio: proteggere i target 0,1,2 con queste probabilità
    strategy = np.array([0.5, 0.3, 0.2], dtype=np.float32)
    obs, reward, done, _, info = env.step(strategy)

    print("Reward Difensore:", reward)
    print("Target Attaccato:", info["target_attacked"])
    print("Strategia Normalizzata:", info["strategy"])

    grafo = nx.DiGraph()

    # Aggiunta di nodi e archi
    grafo.add_edge('EWS', 'OWS', weight=3)
    grafo.add_edge('OWS', 'EWS', weight=4)
    grafo.add_edge('EWS', 'S3', weight=1)
    grafo.add_edge('OWS', 'S3', weight=3)
    grafo.add_edge('S3', 'MHS', weight=4)
    grafo.add_edge('S3', 'SS', weight=4)
    grafo.add_edge('S3', 'F', weight=4)
    grafo.add_edge('MHS', 'SS', weight=4)
    grafo.add_edge('SS', 'MHS', weight=4)
    grafo.add_edge('F', 'PMS', weight=4)
    grafo.add_edge('F', 'AS', weight=4)
    grafo.add_edge('F', 'SUS', weight=4)
    grafo.add_edge('F', 'SFTPS', weight=4)
    grafo.add_edge('F', 'RAS', weight=4)
    grafo.add_edge('PMS', 'AS', weight=4)
    grafo.add_edge('AS', 'PMS', weight=4)
    grafo.add_edge('AS', 'SUS', weight=4)
    grafo.add_edge('SUS', 'AS', weight=4)
    grafo.add_edge('SFTPS', 'RAS', weight=4)
    grafo.add_edge('RAS', 'SFTPS', weight=4)
    

    print(grafo)
    # Stampa del grafo
    print(grafo.nodes)
    print(grafo.edges)

    grafo.nodes['F']['impact'] = 2

    print(f"Peso arco : {grafo.edges['F','RAS']['weight']}")
    print(f"Impatto nodo F : {grafo.nodes['F']['impact']}")