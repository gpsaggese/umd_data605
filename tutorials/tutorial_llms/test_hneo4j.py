import unittest
import sys; sys.path.append("/data")
import helpers.hunit_test as hunit_test

import neo4j
import hneo4j

# !pip install --quiet neo4j

class Test_to_str1(hunit_test.TestCase):

    def connect_to_neo4j(self):
        URI = "neo4j://neo4j:7687"
        # URI = "bolt://neo4j:7687"
        AUTH = ("neo4j", "testtest")
        driver = neo4j.GraphDatabase.driver(URI, auth=AUTH)
        return driver

    def create_graph(self, driver):
        hneo4j.print_graph_stats(driver)
        print("Deleting ...")
        hneo4j.delete_all(driver)
        hneo4j.print_graph_stats(driver)
        # `w` has `Wine` label and then various properties.
        query = 'CREATE (w:Wine {name:"Prancing Wolf", style: "ice wine", vintage: 2015})'
        _ = driver.execute_query(query)
        # Create a node representing a publication.
        query = 'CREATE (p:Publication {name: "Wine Expert Monthly"})'
        _ = driver.execute_query(query)
        # Since the publication reports on the wine, we can create an edge.
        query = '''
            MATCH (p:Publication {name: "Wine Expert Monthly"}),
              (w:Wine {name: "Prancing Wolf", vintage: 2015})
              CREATE (p)-[r:reported_on]->(w)
            '''
        _ = driver.execute_query(query)

    def test1(self) -> None:
        driver = self.connect_to_neo4j()
        self.create_graph(driver)
        # Run.
        query = "MATCH(n) RETURN COUNT(n) AS node_count"
        result = driver.execute_query(query)
        # Check.
        self.assertEqual(type(result[0]), list)
        #
        self.assertEqual(type(result[0][0]), neo4j.Record)
        act = hneo4j.to_str(result[0][0])
        exp = """
        record=<int> 2
        """
        self.assert_equal(act, exp, fuzzy_match=True)
        #
        act = hneo4j.to_str(result)
        exp = """
        records:
            1 [
                    record=<int> 2
            ]
        keys:
            1 [
                    <str> node_count
            ]
            """
        self.assert_equal(act, exp, fuzzy_match=True)
        #
        self.assertEqual(result[0][0]["node_count"], 2)
        driver.close()

    def test2(self) -> None:
        driver = self.connect_to_neo4j()
        self.create_graph(driver)
        # Return a node.
        query = "MATCH(n:Wine) RETURN n"
        result = driver.execute_query(query)
        # Check.
        self.assertEqual(type(result[0]), list)
        #
        record = result[0][0]
        self.assertEqual(type(record), neo4j.Record)
        act = hneo4j.to_str(record)
        exp = """
        record=label=Wine
        properties=
        {'name': 'Prancing Wolf', 'style': 'ice wine', 'vintage': 2015}
        """
        self.assert_equal(act, exp, fuzzy_match=True)
        #
        act = hneo4j.to_str(result)
        exp = r"""
        records:
            1 [
                    record=label=Wine
                    properties=
                    {'name': 'Prancing Wolf', 'style': 'ice wine', 'vintage': 2015}

            ]
        keys:
            1 [
                    <str> n
            ]
        """
        self.assert_equal(act, exp, fuzzy_match=True)
        driver.close()
