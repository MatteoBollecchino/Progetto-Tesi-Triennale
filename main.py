import ssg as ssg
import networkx as nx
from utils import Utils as ut
from networkx.drawing.nx_pydot import to_pydot

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
    graph.add_edge('MHS', 'SS', weight = 0.60)
    graph.add_edge('SS', 'MHS', weight = 0.74)
    graph.add_edge('F', 'PMS', weight = 0.92)
    graph.add_edge('F', 'AS', weight = 0.82)
    graph.add_edge('F', 'SUS', weight = 0.58)
    graph.add_edge('F', 'SFTPS', weight = 0.86)
    graph.add_edge('F', 'RAS', weight = 0.74)
    graph.add_edge('PMS', 'AS', weight = 0.46)
    graph.add_edge('AS', 'PMS', weight = 0.80)
    graph.add_edge('AS', 'SUS', weight = 0.72) 
    graph.add_edge('SUS', 'AS', weight = 0.56)
    graph.add_edge('SFTPS', 'RAS', weight = 0.60)
    graph.add_edge('RAS', 'SFTPS', weight = 0.47)



    # Nodi più esterni -> impatto minore

    graph.nodes['OWS']['impact'] = 1
    graph.nodes['EWS']['impact'] = 2
    graph.nodes['S3']['impact'] = 3
    graph.nodes['MHS']['impact'] = 4
    graph.nodes['SS']['impact'] = 4
    graph.nodes['F']['impact'] = 9
    graph.nodes['PMS']['impact'] = 9
    graph.nodes['AS']['impact'] = 10
    graph.nodes['SUS']['impact'] = 7
    graph.nodes['SFTPS']['impact'] = 9
    graph.nodes['RAS']['impact'] = 8

    source_list = ['OWS', 'EWS']
    budget_defender = 6000
    
    # liste di 5 elementi : [costo, efficacia sull'arco, nodo_origine, nodo_destinazione, minaccia STRIDE]

    # le liste sono da modificare
    """
    # Caso in cui NON si raggiunge un rischio accettabile
    countermeasures = [[500, 0.2,'OWS','EWS'], [100, 0.08,'EWS','S3'], [356, 0.31,'S3','F'],[214, 0.15,'S3','SS'], 
                       [150, 0.21, 'S3', 'SS'],[574, 0.38,'MHS','SS'], [710, 0.24,'F','AS'], [632, 0.17,'F','RAS'], 
                       [759, 0.26,'F','PMS'], [542, 0.36,'F','SFTPS'], [1542, 0.41,'AS','PMS'], [2358, 0.29,'AS','SUS']]
    """
    
    # Caso in cui si raggiunge un rischio accettabile
    countermeasures = [[500, 0.25,'OWS','EWS'], [100, 0.08,'EWS','S3'], [356, 0.31,'S3','F'], [214, 0.15,'S3','SS'], 
                       [150, 0.21,'S3','SS'], [574, 0.38,'MHS','SS'], [710, 0.24,'F','AS'], [1110, 0.64,'F','AS'],
                       [632, 0.17,'F','RAS'], [369, 0.38,'F','RAS'], [759, 0.26,'F','PMS'], [100, 0.19,'F','PMS'], 
                       [542, 0.36,'F','SFTPS'], [142, 0.49,'F','SFTPS'], [852, 0.45,'F','SUS'], [600, 0.32,'PMS','AS'],
                       [154, 0.61,'AS','PMS'], [235, 0.29,'AS','SUS'], [441, 0.76,'AS','SUS'], [535, 0.27,'SFTPS','RAS']]
    
    risk_threshold = 4
    env = ssg.StackelbergSecurityGameEnv(graph, source_list, budget_defender, countermeasures, risk_threshold)

    obs, _ = env.reset()

    ut.print_graph_png(graph, 0)

    done = False

    print(f"\nRischio iniziale: {ut.get_graph_risk(graph,source_list)} \n")

    # Contatore Iterazioni Gioco
    i = 1

    while True:

        # strategy nel nostro caso corrisponderà all'applicazione delle contromisure
        # strategy = modified, new_graph, remaining_countermeasures, remaining_budget
        strategy = ut.apply_countermeasures(graph, source_list, countermeasures, budget_defender)

        graph = strategy[1]

        """
        # Stampa del grafo modificato
        for u, v, d in graph.edges(data=True):
                d["label"] = str(round(d["weight"],4))

        pydot_graph = to_pydot(graph)
        
        pydot_graph.write_png(f"Grafi\grafo{i}.png")
        """

        # attacker_strategy = path con maggior rischio (corrisponde alla strategia finale dell'attaccante) 
        done, new_graph_risk, remaining_budget, applied_countermeasures, attacker_strategy = env.step(strategy)

        budget_defender = remaining_budget

        print(f"Iterazione {i} del gioco")
        print(f"Terminato: {done}")
        print(f"Rischio grafo: {new_graph_risk}")
        print(f"Budget rimanente: {remaining_budget}")
        print(f"Contromisure applicate: {applied_countermeasures} \n \n")

        if done:

            print(f"Strategia finale attaccante: {attacker_strategy} \n")

            ut.print_graph_png(graph, i)

            if new_graph_risk <= env.get_risk_threshold():
                print(f"Il rischio {new_graph_risk} ottenuto è accettabile \n")
            else:
                print(f"Il rischio {new_graph_risk} ottenuto NON è accettabile \n")

            break

        i = i + 1

    # Aggiungere chiusura dell'enviroment
    env.close()