import ssg as ssg
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

    source_list = ['OWS', 'EWS']
    budget_defender = 5000
    
    # devono essere quartuple (liste di 4 elementi) ? (costo, efficacia sull'arco, nodo_origine, nodo_destinazione)
    countermeasures = [[500, 0.2,'OWS','EWS'], [100, 0.08,'OWS','S3'], [214, 0.15,'S3','SS'], [150, 0.21, 'S3', 'SS'],
                       [574, 0.38,'MHS','SS'], [710, 0.24,'F','AS'], [632, 0.17,'F','RAS'],
                       [1542, 0.41,'AS','PMS'], [2358, 0.29,'AS','SUS']]

    # Da modificare 
    env = ssg.StackelbergSecurityGameEnv(graph, source_list, budget_defender, countermeasures)

    obs, _ = env.reset()
    
    done = False

    while True:
        
        # strategy nel nostro caso corrisponderà all'applicazione delle contromisure -> strategy = grafo aggiornato
        # obs, reward, done, _, info = env.step(strategy)
        if done:
            break