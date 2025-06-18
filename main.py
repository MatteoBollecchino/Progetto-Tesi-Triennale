import StackelbergSecurityGameEnv as ssg
import GrafoPesato as gp
import numpy as np

if __name__ == "__main__":
    env = ssg.StackelbergSecurityGameEnv(n_targets=3)

    obs, _ = env.reset()
    
    # esempio: proteggere i target 0,1,2 con queste probabilità
    strategy = np.array([0.5, 0.3, 0.2], dtype=np.float32)
    obs, reward, done, _, info = env.step(strategy)

    print("Reward Difensore:", reward)
    print("Target Attaccato:", info["target_attacked"])
    print("Strategia Normalizzata:", info["strategy"])
    
    grafo = gp.GrafoPesato()

    # Aggiunta di nodi e archi
    grafo.add_edge('EWS', 'OWS', 1, 3)
    grafo.add_edge('OWS', 'EWS', 2, 4)
    grafo.add_edge('EWS', 'S3', 20, 1)
    grafo.add_edge('OWS', 'S3', 10, 3)
    grafo.add_edge('S3', 'MHS', 3, 4)
    grafo.add_edge('S3', 'SS', 3, 4)
    grafo.add_edge('S3', 'F', 3, 4)
    grafo.add_edge('MHS', 'SS', 3, 4)
    grafo.add_edge('SS', 'MHS', 3, 4)
    grafo.add_edge('F', 'PMS', 3, 4)
    grafo.add_edge('F', 'AS', 3, 4)
    grafo.add_edge('F', 'SUS', 3, 4)
    grafo.add_edge('F', 'SFTPS', 3, 4)
    grafo.add_edge('F', 'RAS', 3, 4)
    grafo.add_edge('PMS', 'AS', 3, 4)
    grafo.add_edge('AS', 'PMS', 3, 4)
    grafo.add_edge('AS', 'SUS', 3, 4)
    grafo.add_edge('SUS', 'AS', 3, 4)
    grafo.add_edge('SFTPS', 'RAS', 3, 4)
    grafo.add_edge('RAS', 'SFTPS', 3, 4)
    
    # Stampa del grafo
    print(grafo)

    print(grafo.get_neighbours('A'))