import unittest
import utils as ut
import networkx as nx

# DA VALUTARE SE TENERE O MENO
class TestUtils(unittest.TestCase):

    def setUp(self):

        # Aggiunta di nodi e archi
        self.graph = nx.DiGraph()

        # Aggiunta di nodi e archi
        self.graph.add_edge('EWS', 'OWS', weight = 0.69)
        self.graph.add_edge('OWS', 'EWS', weight = 0.77)
        self.graph.add_edge('EWS', 'S3', weight = 0.92)
        self.graph.add_edge('OWS', 'S3', weight = 0.57)
        self.graph.add_edge('S3', 'MHS', weight = 0.93)
        self.graph.add_edge('S3', 'SS', weight = 0.71)
        self.graph.add_edge('S3', 'F', weight = 0.89)
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
                        [574, 0.38,'MHS','SS'], [710, 0.24,'F','AS'], [632, 0.17,'F','RAS'],
                        [1542, 0.41,'AS','PMS'], [2358, 0.29,'AS','SUS']]

    def test_somma(self):
        self.assertEqual(self.calc.somma(2, 3), 5)

    def test_sottrai(self):
        self.assertEqual(self.calc.sottrai(5, 2), 3)

    def test_dividi(self):
        self.assertAlmostEqual(self.calc.dividi(10, 2), 5.0)

    def test_dividi_per_zero(self):
        with self.assertRaises(ValueError):
            self.calc.dividi(10, 0)

if __name__ == "__main__":
    unittest.main()