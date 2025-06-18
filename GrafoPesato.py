class GrafoPesato:
    def __init__(self):
        self.nodi = {}

    def aggiungi_nodo(self, nodo):
        if nodo not in self.nodi:
            self.nodi[nodo] = {}

    def aggiungi_arco(self, da_nodo, a_nodo, peso):
        self.aggiungi_nodo(da_nodo)
        self.aggiungi_nodo(a_nodo)
        self.nodi[da_nodo][a_nodo] = peso

    def ottieni_peso(self, da_nodo, a_nodo):
        if da_nodo in self.nodi and a_nodo in self.nodi[da_nodo]:
            return self.nodi[da_nodo][a_nodo]
        else:
            return None

    def ottieni_vicini(self, nodo):
        if nodo in self.nodi:
            return self.nodi[nodo]
        else:
            return {}

    def __str__(self):
        s = ""
        for nodo, vicini in self.nodi.items():
            s += f"Nodo {nodo}: {vicini}\n"
        return s