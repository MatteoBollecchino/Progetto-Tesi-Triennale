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
        test_paths = [['S3', 'MHS'], ['S3', 'SS'], ['S3', 'MHS', 'SS'], ['S3', 'SS', 'MHS']]
        self.assertCountEqual(all_paths, test_paths)

    def test_get_all_paths(self):

        all_paths = self.ut.get_all_paths(self.graph, self.source_list)
        test_paths = [['OWS', 'EWS'], ['OWS', 'EWS', 'S3'], ['OWS', 'S3'], ['OWS', 'EWS', 'S3', 'MHS'], 
                      ['OWS', 'EWS', 'S3', 'SS', 'MHS'], ['OWS', 'S3', 'MHS'], ['OWS', 'S3', 'SS', 'MHS'], 
                      ['OWS', 'EWS', 'S3', 'MHS', 'SS'], ['OWS', 'EWS', 'S3', 'SS'], ['OWS', 'S3', 'MHS', 'SS'], 
                      ['OWS', 'S3', 'SS'], ['EWS', 'OWS'], ['EWS', 'OWS', 'S3'], ['EWS', 'S3'], 
                      ['EWS', 'OWS', 'S3', 'MHS'], ['EWS', 'OWS', 'S3', 'SS', 'MHS'], ['EWS', 'S3', 'MHS'], 
                      ['EWS', 'S3', 'SS', 'MHS'], ['EWS', 'OWS', 'S3', 'MHS', 'SS'], ['EWS', 'OWS', 'S3', 'SS'], 
                      ['EWS', 'S3', 'MHS', 'SS'], ['EWS', 'S3', 'SS']]
        self.assertCountEqual(all_paths, test_paths)
    
    def test_get_node_risk(self):

        risk = self.ut.get_node_risk(self.graph.nodes['MHS'], 0.40)
        expected_risk = 1.60

        self.assertEqual(risk, expected_risk)

    def test_get_path_risk(self):

        path = ['EWS', 'OWS', 'S3', 'SS', 'MHS']
        risk = self.ut.get_path_risk(self.graph, path)
        expected_risk = 2.96

        self.assertEqual(risk, expected_risk)

    def test_get_graph_risk(self):

        risk = self.ut.get_graph_risk(self.graph, self.source_list)
        expected_risk = 2.96

        self.assertEqual(risk, expected_risk)

    def test_get_maximum_risk_path(self):
        
        max_risk_path = self.ut.get_maximum_risk_path(self.graph, self.source_list)
        expected_max_risk_path = ['OWS', 'EWS', 'S3', 'SS', 'MHS']

        self.assertEqual(max_risk_path, expected_max_risk_path)

    def test__search_countermeasure(self):
        
        found, countermeasure = self.ut._search_countermeasure('OWS', 'S3', self.countermeasures)

        self.assertTrue(found)
        self.assertEqual(countermeasure, [100, 0.08,'OWS','S3'])

        found, countermeasure = self.ut._search_countermeasure('EWS', 'OWS', self.countermeasures)

        self.assertFalse(found)
        self.assertEqual(countermeasure, None)

    def test_apply_countermeasure_True(self):

        graph1 = self.graph.copy()
        modified, graph, countermeasures, budget = self.ut.apply_countermeasures(self.graph, self.source_list,
                                                                                 self.countermeasures, self.budget_defender)
        
        self.assertTrue(modified)
        self.assertCountEqual(countermeasures, [[100, 0.08,'OWS','S3'], [574, 0.38,'MHS','SS']])
        self.assertEqual(budget, 4286)
        
        # Con i seguenti controlli si verifica che il grafo venga effettivamente modificato dal metodo
        matcher = nx.is_isomorphic(graph, self.graph,
            edge_match=nx.algorithms.isomorphism.categorical_edge_match('weight', None))
        self.assertTrue(matcher)

        matcher = nx.is_isomorphic(graph, graph1,
            edge_match=nx.algorithms.isomorphism.categorical_edge_match('weight', None))
        self.assertFalse(matcher)

    def test_apply_countermeasure_False(self):

        graph1 = self.graph.copy()
        countermeasures1 = [[710, 0.24,'F','AS'], [632, 0.17,'F','RAS'], [1542, 0.41,'AS','PMS'], [2358, 0.29,'AS','SUS']]
        modified, graph, countermeasures, budget = self.ut.apply_countermeasures(self.graph, self.source_list,
                                                                                 countermeasures1, self.budget_defender)
        
        self.assertFalse(modified)
        self.assertCountEqual(countermeasures, countermeasures1)
        self.assertEqual(budget, 5000)
        
        # Date queste contromisure, mi aspetto che il grafo non abbia variazioni
        matcher = nx.is_isomorphic(graph, graph1,
            edge_match=nx.algorithms.isomorphism.categorical_edge_match('weight', None))
        self.assertTrue(matcher)


if __name__ == "__main__":
    unittest.main()