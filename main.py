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
    grafo.aggiungi_arco('A', 'B', 4)
    grafo.aggiungi_arco('A', 'C', 2)
    grafo.aggiungi_arco('B', 'C', 5)
    grafo.aggiungi_arco('B', 'D', 10)
    grafo.aggiungi_arco('C', 'D', 3)
    
    # Stampa del grafo
    print(grafo)