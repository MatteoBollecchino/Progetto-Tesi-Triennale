class GrafoPesato:
    def __init__(self):
        self.nodes = {}

    def add_node(self, node):
        if node not in self.nodes:
            self.nodes[node] = {}

    def add_edge(self, from_node, to_node, cvss_score, epss_score):
        if cvss_score < 0 or cvss_score > 10 :
            print(repr("CVSS score errato"))
            return
        
        if epss_score < 0 or epss_score > 1 :
            print(repr("EPSS score errato"))
            return

        self.add_node(from_node)
        self.add_node(to_node)
        self.nodes[from_node][to_node] = self.get_unmitigated_risk(cvss_score, epss_score)

    def get_weight(self, from_node, to_node):
        if from_node in self.nodes and to_node in self.nodes[from_node]:
            return self.nodes[from_node][to_node]
        else:
            return None

    def get_neighbours(self, node):
        if node in self.nodes:
            return self.nodes[node]
        else:
            return {}
        
    def get_unmitigated_risk(self,cvss, epss):
        return cvss*epss

    def __str__(self):
        s = ""
        for node, neighbours in self.nodes.items():
            s += f"Nodo {node}: {neighbours}\n"
        return s