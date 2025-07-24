import unittest
import utils as ut
import networkx as nx

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
        test_paths = [['S3'], ['S3', 'MHS'], ['S3', 'SS'], ['S3', 'MHS', 'SS'], ['S3', 'SS', 'MHS']]
        self.assertCountEqual(all_paths, test_paths)

    def test_get_all_paths(self):

        all_paths = self.ut.get_all_paths(self.graph, self.source_list)
        test_paths = [['OWS', 'EWS'], ['OWS'], ['OWS', 'EWS', 'S3'], ['OWS', 'S3'], ['OWS', 'EWS', 'S3', 'MHS'], 
                      ['OWS', 'EWS', 'S3', 'SS', 'MHS'], ['OWS', 'S3', 'MHS'], ['OWS', 'S3', 'SS', 'MHS'], 
                      ['OWS', 'EWS', 'S3', 'MHS', 'SS'], ['OWS', 'EWS', 'S3', 'SS'], ['OWS', 'S3', 'MHS', 'SS'], 
                      ['OWS', 'S3', 'SS'],['EWS'], ['EWS', 'OWS'], ['EWS', 'OWS', 'S3'], ['EWS', 'S3'], 
                      ['EWS', 'OWS', 'S3', 'MHS'], ['EWS', 'OWS', 'S3', 'SS', 'MHS'], ['EWS', 'S3', 'MHS'], 
                      ['EWS', 'S3', 'SS', 'MHS'], ['EWS', 'OWS', 'S3', 'MHS', 'SS'], ['EWS', 'OWS', 'S3', 'SS'], 
                      ['EWS', 'S3', 'MHS', 'SS'], ['EWS', 'S3', 'SS']]
        self.assertCountEqual(all_paths, test_paths)
    
    def test_get_node_risk(self):

        risk = self.ut.get_node_risk(self.graph.nodes['MHS'], 0.40)
        expected_risk = 1.60

        self.assertEqual(risk, expected_risk)

    def test_get_path_node_risk(self):

        path = ['EWS', 'OWS', 'S3', 'SS', 'MHS']
        risk = self.ut.get_path_risk(self.graph, path)
        expected_risk = 2.96

        self.assertEqual(risk, expected_risk)

    def test_get_maximum_risk_path(self):
        
        max_risk_path = self.ut.get_maximum_risk_path(self.graph, self.source_list)
        expected_max_risk_path = ['OWS', 'EWS', 'S3', 'SS', 'MHS']

        self.assertEqual(max_risk_path, expected_max_risk_path)

    def test__search_countermeasure(self):
        
        found, cost, efficiency = self.ut._search_countermeasure('OWS', 'S3', self.countermeasures)

        self.assertTrue(found)
        self.assertEqual(cost, 100)
        self.assertEqual(efficiency, 0.08)

        found, cost, efficiency = self.ut._search_countermeasure('EWS', 'OWS', self.countermeasures)

        self.assertFalse(found)
        self.assertEqual(cost, 0)
        self.assertEqual(efficiency, 0)

    def test__apply_countermeasure(self):
        pass

    def test_apply_countermeasure(self):
        pass

if __name__ == "__main__":
    unittest.main()