import ssg as ssg
import networkx as nx
from utils import Utils as ut

def main():

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
    graph.nodes['SS']['impact'] = 5
    graph.nodes['F']['impact'] = 9
    graph.nodes['PMS']['impact'] = 6
    graph.nodes['AS']['impact'] = 10
    graph.nodes['SUS']['impact'] = 7
    graph.nodes['SFTPS']['impact'] = 9
    graph.nodes['RAS']['impact'] = 8

    source_list = ['OWS', 'EWS']
    budget_defender = 6000

    # liste di 5 elementi : [costo, efficacia sull'arco, nodo_origine, nodo_destinazione, minaccia STRIDE]

    # le liste sono da modificare
    
    # Caso in cui NON si raggiunge un rischio accettabile al primo SSG
    countermeasures = [[500, 0.2,'OWS','EWS','S'], 
                       [100, 0.08,'EWS','S3','D'], 
                       [356, 0.31,'S3','F','T'],
                       [214, 0.15,'S3','SS','I'], 
                       [150, 0.21, 'S3', 'SS','T'],
                       [574, 0.38,'MHS','SS','S'], 
                       [710, 0.24,'F','AS','D'], 
                       [632, 0.17,'F','RAS','E'],
                       [3632, 0.17,'F','RAS','S'],
                       [1275, 0.21,'F','RAS','I'], 
                       [759, 0.46,'F','PMS','I'],
                       [691, 0.61,'F','SUS','D'], 
                       [542, 0.36,'F','SFTPS','S'],
                       [1890, 0.46,'F','SFTPS','I'],
                       [1542, 0.41,'AS','PMS','E'],
                       [623, 0.19,'AS','PMS','T'],
                       [2358, 0.29,'AS','SUS','I'],
                       [358, 0.48,'AS','SUS','S'],
                       [857, 0.63,'PMS','AS','D'], 
                       [3260, 0.19,'RAS','SFTPS','E'],
                       [2260, 0.49,'SFTPS','RAS','T'],

                       [711, 0.25,'F','AS','E'], 
                       [631, 0.18,'F','RAS','D'],
                       [3631, 0.16,'F','RAS','D'],
                       [1271, 0.20,'F','RAS','T'], 
                       [751, 0.45,'F','PMS','S'],
                       [692, 0.64,'F','SUS','I'], 
                       [541, 0.35,'F','SFTPS','E'],
                       [1891, 0.47,'F','SFTPS','S'],
                       [1541, 0.40,'AS','PMS','D'],
                       [621, 0.18,'AS','PMS','I'],
                       [2351, 0.27,'AS','SUS','T'],
                       [351, 0.48,'AS','SUS','E'],
                       [851, 0.62,'PMS','AS','S'], 
                       [3321, 0.22,'RAS','SFTPS','T'],
                       [2261, 0.48,'SFTPS','RAS','E']]
    
    """
    # Caso in cui si raggiunge un rischio accettabile al primo SSG
    countermeasures = [[500, 0.25,'OWS','EWS','S'], 
                       [100, 0.08,'EWS','S3','E'],
                       [356, 0.31,'S3','F','T'], 
                       [214, 0.15,'S3','SS','I'], 
                       [150, 0.21,'S3','SS','S'], 
                       [574, 0.38,'MHS','SS','D'], 
                       [710, 0.24,'F','AS','D'], 
                       [1110, 0.64,'F','AS','S'],
                       [632, 0.17,'F','RAS','I'], 
                       [369, 0.38,'F','RAS','E'], 
                       [759, 0.26,'F','PMS','T'], 
                       [100, 0.19,'F','PMS','S'], 
                       [542, 0.36,'F','SFTPS','D'], 
                       [142, 0.49,'F','SFTPS','D'], 
                       [852, 0.45,'F','SUS','T'], 
                       [600, 0.32,'PMS','AS','E'],
                       [154, 0.61,'AS','PMS','E'], 
                       [235, 0.29,'AS','SUS','S'], 
                       [441, 0.76,'AS','SUS','I'], 
                       [535, 0.27,'SFTPS','RAS','T']]
    """  
                
    risk_threshold = 4

    # Controllo rischio grafo senza contromisure
    unmitigated_risk = ut.get_graph_risk(graph,source_list)
    print(f"\nRischio iniziale: {unmitigated_risk} \n")

    # Se il rischio è tollerabile termina tutto
    if unmitigated_risk < risk_threshold:
        print(f"Il rischio {unmitigated_risk} ottenuto è accettabile \n")
        return
    
    # Lista di contromisure già implementate, fornite dall'owner (hanno costo nullo)
    implemented_countermeasures = [[0, 0.14,'OWS','EWS','S'], 
                                [0, 0.06,'EWS','S3','D'], 
                                [0, 0.28,'S3','F','T'],
                                [0, 0.34,'S3','SS','I'], 
                                [0, 0.16,'MHS','SS','S'], 
                                [0, 0.12,'F','AS','D'], 
                                [0, 0.26,'F','PMS','I'], 
                                [0, 0.09,'AS','PMS','E']]

    # Si applicano al grafo la lista di contromisure già implementate
    graph = ut.apply_implemented_countermeasures(graph, source_list, implemented_countermeasures)

    # Controllo rischio grafo con contromisure iniziali
    mitigated_risk = ut.get_graph_risk(graph,source_list)
    print(f"\nRischio dopo le contromisure già implementate: {mitigated_risk} \n")

    # Se il rischio è tollerabile termina tutto
    if mitigated_risk < risk_threshold:
        print(f"Il rischio {mitigated_risk} ottenuto è accettabile \n")
        return
    
    G1 = graph.copy()

    previous_graph = graph.copy()
    previous_budget = budget_defender
    previous_countermeasures = countermeasures.copy()
    budget_increment = 1000

    # Contatore Giochi
    j = 1

    while True:

        # Inizio SSG

        env = ssg.StackelbergSecurityGameEnv(graph, source_list, budget_defender, countermeasures, risk_threshold)

        obs, _ = env.reset()

        ut.print_graph_png(graph, 0)

        print(f"Budget Iniziale: {budget_defender}")

        done = False

        # Contatore Iterazioni Gioco
        i = 1

        while True:

            # strategy nel nostro caso corrisponderà all'applicazione delle contromisure
            # strategy = modified, new_graph, remaining_countermeasures, remaining_budget
            strategy = ut.apply_countermeasures(graph, source_list, countermeasures, budget_defender)

            graph = strategy[1]

            # attacker_strategy = path con maggior rischio (corrisponde alla strategia finale dell'attaccante) 
            done, new_graph_risk, remaining_budget, applied_countermeasures, attacker_strategy = env.step(strategy)

            budget_defender = remaining_budget

            if done:

                print(f"Strategia finale attaccante: {attacker_strategy} \n")
                print(f"Budget rimanente: {remaining_budget}")
                print(f"Contromisure applicate: {applied_countermeasures} \n \n")

                ut.print_graph_png(graph, i)
                G2 = graph.copy()

                if new_graph_risk < risk_threshold:

                    print(f"Il rischio {new_graph_risk} ottenuto è accettabile \n")
                    ut.export_graph_diff_png(G1, G2)

                    return
                else:

                    print(f"Il rischio {new_graph_risk} ottenuto NON è accettabile \n")
                    graph = previous_graph.copy()
                    budget_defender = previous_budget + j * budget_increment
                    countermeasures = previous_countermeasures.copy()

                break

            i = i + 1

        # Chiusura dell'environment
        env.close()

        if j == 10 :
            print("Contromisure Insufficienti")
            break

        j = j + 1



if __name__ == "__main__":
    main()