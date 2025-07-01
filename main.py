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
    grafo.add_edge('EWS', 'OWS', weight = 0.69)
    grafo.add_edge('OWS', 'EWS', weight = 0.77)
    grafo.add_edge('EWS', 'S3', weight = 0.92)
    grafo.add_edge('OWS', 'S3', weight = 0.57)
    grafo.add_edge('S3', 'MHS', weight = 0.93)
    grafo.add_edge('S3', 'SS', weight = 0.71)
    grafo.add_edge('S3', 'F', weight = 0.89)
    grafo.add_edge('MHS', 'SS', weight = 0.40)
    grafo.add_edge('SS', 'MHS', weight = 0.74)
    grafo.add_edge('F', 'PMS', weight = 0.90)
    grafo.add_edge('F', 'AS', weight = 0.82)
    grafo.add_edge('F', 'SUS', weight = 0.38)
    grafo.add_edge('F', 'SFTPS', weight = 0.86)
    grafo.add_edge('F', 'RAS', weight = 0.44)
    grafo.add_edge('PMS', 'AS', weight = 0.46)
    grafo.add_edge('AS', 'PMS', weight = 0.80)
    grafo.add_edge('AS', 'SUS', weight = 0.72) 
    grafo.add_edge('SUS', 'AS', weight = 0.26)
    grafo.add_edge('SFTPS', 'RAS', weight = 0.30)
    grafo.add_edge('RAS', 'SFTPS', weight = 0.24)
    

    print(f"Descrizione grafo: {grafo}")
    # Stampa del grafo
    print(grafo.nodes)
    print(grafo.edges)

    grafo.nodes['OWS']['impact'] = 1
    grafo.nodes['EWS']['impact'] = 2
    grafo.nodes['S3']['impact'] = 3
    grafo.nodes['MHS']['impact'] = 4
    grafo.nodes['SS']['impact'] = 4
    grafo.nodes['F']['impact'] = 5
    grafo.nodes['PMS']['impact'] = 9
    grafo.nodes['AS']['impact'] = 10
    grafo.nodes['SUS']['impact'] = 7
    grafo.nodes['SFTPS']['impact'] = 6
    grafo.nodes['RAS']['impact'] = 8

    print(f"Peso arco : {grafo.edges['F','RAS']['weight']}")
    print(f"Impatto nodo AS : {grafo.nodes['AS']['impact']}")