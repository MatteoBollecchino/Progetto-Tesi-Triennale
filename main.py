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
    grafo.add_edge('A', 'B', 1, 3)
    grafo.add_edge('A', 'C', 2, 4)
    grafo.add_edge('B', 'C', 20, 1)
    grafo.add_edge('B', 'D', 10, 3)
    grafo.add_edge('C', 'D', 3, 4)
    
    # Stampa del grafo
    print(grafo)

    print(grafo.get_neighbours('A'))