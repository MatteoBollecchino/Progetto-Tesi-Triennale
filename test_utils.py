import unittest
import utils as ut
import networkx as nx

# DA VALUTARE SE TENERE O MENO
class TestUtils(unittest.TestCase):

    def setUp(self):

        self.ut = ut.Utils()

        # Aggiunta di nodi e archi
        self.graph = nx.DiGraph()

        # Aggiunta di nodi e archi
        self.graph.add_edge('EWS', 'OWS', weight = 0.69)
        self.graph.add_edge('OWS', 'EWS', weight = 0.77)
        self.graph.add_edge('EWS', 'S3', weight = 0.92)
        self.graph.add_edge('OWS', 'S3', weight = 0.57)
        self.graph.add_edge('S3', 'MHS', weight = 0.93)
        self.graph.add_edge('S3', 'SS', weight = 0.71)
        self.graph.add_edge('MHS', 'SS', weight = 0.40)
        self.graph.add_edge('SS', 'MHS', weight = 0.74)
        
        # Nodi più esterni -> impatto minore
        self.graph.nodes['OWS']['impact'] = 1
        self.graph.nodes['EWS']['impact'] = 2
        self.graph.nodes['S3']['impact'] = 3
        self.graph.nodes['MHS']['impact'] = 4
        self.graph.nodes['SS']['impact'] = 4

        self.source_list = ['OWS', 'EWS']
        self.budget_defender = 5000
        
        # devono essere quartuple (liste di 4 elementi) ? (costo, efficacia sull'arco, nodo_origine, nodo_destinazione)
        self.countermeasures = [[500, 0.2,'OWS','EWS'], [100, 0.08,'OWS','S3'], [214, 0.15,'S3','SS'], 
                                [574, 0.38,'MHS','SS']]

    def test_get_paths_from_source(self):

        all_paths = self.ut.get_paths_from_source(self.graph, 'S3')
        self.assertCountEqual(all_paths, [['S3'], ['S3', 'MHS'], ['S3', 'SS'], ['S3', 'MHS', 'SS'], ['S3', 'SS', 'MHS']])

if __name__ == "__main__":
    unittest.main()