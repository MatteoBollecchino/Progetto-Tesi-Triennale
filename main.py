import ssg as ssg
import GrafoPesato as gp
import numpy as np
import networkx as nx
from utils import Utils as ut

if __name__ == "__main__":

    # Creazione grafo SUC
    graph = nx.DiGraph()

    # Aggiunta di nodi e archi
    graph.add_edge('EWS', 'OWS', weight = 0.69)
    graph.add_edge('OWS', 'EWS', weight = 0.77)
    graph.add_edge('EWS', 'S3', weight = 0.92)
    graph.add_edge('OWS', 'S3', weight = 0.57)
    graph.add_edge('S3', 'MHS', weight = 0.93)
    graph.add_edge('S3', 'SS', weight = 0.71)
    graph.add_edge('S3', 'F', weight = 0.89)
    graph.add_edge('MHS', 'SS', weight = 0.40)
    graph.add_edge('SS', 'MHS', weight = 0.74)
    graph.add_edge('F', 'PMS', weight = 0.90)
    graph.add_edge('F', 'AS', weight = 0.82)
    graph.add_edge('F', 'SUS', weight = 0.38)
    graph.add_edge('F', 'SFTPS', weight = 0.86)
    graph.add_edge('F', 'RAS', weight = 0.44)
    graph.add_edge('PMS', 'AS', weight = 0.46)
    graph.add_edge('AS', 'PMS', weight = 0.80)
    graph.add_edge('AS', 'SUS', weight = 0.72) 
    graph.add_edge('SUS', 'AS', weight = 0.26)
    graph.add_edge('SFTPS', 'RAS', weight = 0.30)
    graph.add_edge('RAS', 'SFTPS', weight = 0.24)



    # Nodi più esterni -> impatto minore

    graph.nodes['OWS']['impact'] = 1
    graph.nodes['EWS']['impact'] = 2
    graph.nodes['S3']['impact'] = 3
    graph.nodes['MHS']['impact'] = 4
    graph.nodes['SS']['impact'] = 4
    graph.nodes['F']['impact'] = 5
    graph.nodes['PMS']['impact'] = 9
    graph.nodes['AS']['impact'] = 10
    graph.nodes['SUS']['impact'] = 7
    graph.nodes['SFTPS']['impact'] = 6
    graph.nodes['RAS']['impact'] = 8

    budget_difensore = 10000
    contromisure = [(500,0.2)]

    print(ut.get_paths(graph, 'OWS'))
    print(ut.get_maximum_risk_path(graph, 'OWS'))

    # Da modificare 
    """
    env = ssg.StackelbergSecurityGameEnv(n_targets=3)

    obs, _ = env.reset()
    
    # esempio: proteggere i target 0,1,2 con queste probabilità
    strategy = np.array([0.5, 0.3, 0.2], dtype=np.float32)
    obs, reward, done, _, info = env.step(strategy)

    print("Reward Difensore:", reward)
    print("Target Attaccato:", info["target_attacked"])
    print("Strategia Normalizzata:", info["strategy"])
    """