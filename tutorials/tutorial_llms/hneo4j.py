from neo4j import GraphDatabase
from pyvis.network import Network

import re
import helpers.hdbg as hdbg
import helpers.hprint as hprint

from pprint import pformat
from typing import Any

from pygments import highlight
from pygments.formatters import Terminal256Formatter
from pygments.lexers import PythonLexer

import neo4j


def to_bold(text):
    return "\033[1m" + text + "\033[0m"


def pformat_(obj: Any) -> str:
    """
    Pretty-print in color.
    """
    if hasattr(obj, "to_dict"):
        obj = obj.to_dict()
    res = highlight(pformat(obj), PythonLexer(), Terminal256Formatter())
    res = res.rstrip("\n")
    return res


def to_str_(obj, name=""):
    if name:
        txt = "%s= %s %s" % (to_bold(name), type(obj), pformat_(obj))
    else:
        txt = "%s %s" % (type(obj), pformat_(obj))
    return txt


def print_(obj, name=""):
    print(to_str_(obj, name))


def print_result(result):
    # The result contains information about the query results and summary of the query.
    records, summary, keys = result
    # `result.records` is the list of records returned by the query.
    print_(records, "records")
    print_(summary, "summary")
    # `result.keys` is the list of keys returned by the query.
    print_(keys, "keys")


def type_to_str(obj):
    type_str = str(type(obj))
    # <class 'int'>
    m = re.search("(.*)<class '(.*)'>(.*)", type_str)
    if m:
        return "%s<%s>%s" % (m.group(1), m.group(2), m.group(3))
    return type_str


def to_str(obj, depth=0):
    num_spaces = 2
    txt = ""
    if isinstance(obj, neo4j.EagerResult):
        # EagerResult(
        #   records=[
        #       <Record node_count=2>
        #       ],
        #   summary=<neo4j._work.summary.ResultSummary object at 0xffff5eb048e0>,
        #   keys=['node_count'])
        #
        # EagerResult(
        #   records=[
        #       <Record n=<
        #           Node element_id='4:907b90c5-77b7-40ee-bd2b-900a55534cf9:31'
        #               labels=frozenset({'Wine'})
        #               properties={'vintage': 2015, 'name': 'Prancing Wolf', 'style': 'ice wine'}
        #           >>
        #           ],
        #   summary=<neo4j._work.summary.ResultSummary object at 0xffff5eb95930>,
        #   keys=['n'])
        #
        # EagerResult(
        #   records=[
        #       <Record name='Prancing Wolf' style='ice wine'>],
        #   summary=<neo4j._work.summary.ResultSummary object at 0xffff5eaa0eb0>,
        #   keys=['name', 'style'])
        txt = ""
        # The result contains information about the query results and summary of the query.
        records, summary, keys = obj
        # `result.records` is the list of records returned by the query.
        txt += "records:\n" + to_str(records, depth=depth + 1)
        # txt += to_str_(summary, "summary") + "\n"
        # `result.keys` is the list of keys returned by the query.
        txt += "keys:\n" + to_str(keys, depth=depth + 1)
    if isinstance(obj, neo4j.Record):
        # <Record n=<Node element_id='4:907b90c5-77b7-40ee-bd2b-900a55534cf9:31'
        #   labels=frozenset({'Wine'})
        #   properties={'vintage': 2015, 'name': 'Prancing Wolf', 'style': 'ice wine'}>>
        #
        # <Record name='Prancing Wolf' style='ice wine'>
        record = obj
        txt = []
        txt.append("%s [" % len(obj))
        for key in record.keys():
            value = record[key]
            txt.append(
                "%s ->\n%s" % (to_str(key), to_str(value, depth=depth + 1)))
        txt.append("]\n")
        txt = "\n".join(txt)
    if isinstance(obj, neo4j.graph.Node):
        # <Node element_id='4:907b90c5-77b7-40ee-bd2b-900a55534cf9:31'
        #   labels=frozenset({'Wine'})
        #   properties={'vintage': 2015, 'name': 'Prancing Wolf', 'style': 'ice wine'}>
        txt = ""
        txt += " " * num_spaces + "label=%s\n" % (str(list(obj.labels)))
        txt += " " * num_spaces + "properties=%s\n" % (to_str(dict(
            obj.items())))
    if isinstance(obj, neo4j.graph.Relationship):
        # <Relationship element_id='5:907b90c5-77b7-40ee-bd2b-900a55534cf9:48286'
        #   nodes=(
        #       <Node element_id='4:907b90c5-77b7-40ee-bd2b-900a55534cf9:38'
        #           labels=frozenset() properties={}>,
        #       <Node element_id='4:907b90c5-77b7-40ee-bd2b-900a55534cf9:37'
        #           labels=frozenset() properties={}>)
        #   type='reported_on' properties={}>
        txt = ""
        txt += " " * num_spaces + "start_node=%s" % (to_str(obj.start_node))
        txt += " " * num_spaces + "end_node=%s" % (to_str(obj.start_node))
        txt += " " * num_spaces + "type=%s" % (to_str(obj.type))
        txt += " " * num_spaces + "properties=%s\n" % (to_str(dict(
            obj.items())))
    if isinstance(obj, list):
        txt = []
        txt.append("%s [" % len(obj))
        for obj_tmp in obj:
            txt.append(to_str(obj_tmp, depth=depth + 1))
        txt.append("]\n")
        txt = "\n".join(txt)
    if isinstance(obj, dict):
        import pprint
        txt = pprint.pformat(obj)
    if isinstance(obj, (str, int, float, bool)):
        txt = "%s %s" % (type_to_str(obj), str(obj))
    if txt:
        txt = hprint.indent(txt, num_spaces=depth * num_spaces)
        return txt
    raise ValueError("Invalid obj=%s of type=%s" % (obj, type(obj)))


def print_neo4j_version(driver):
    with driver.session() as session:
        result = session.run(
            "CALL dbms.components() YIELD name, versions, edition RETURN name, versions, edition;")
        for record in result:
            print(
                f"Name: {record['name']}, Version: {record['versions']}, Edition: {record['edition']}")


def print_graph_stats(driver):
    # Get node count.
    node_query = "MATCH (n) RETURN COUNT(n) AS node_count"
    node_result = driver.execute_query(node_query)
    # Note that `node_result.single()` doesn't work.
    node_count = node_result[0][0]["node_count"]
    print(f"Number of nodes: {node_count}")
    # Get edge count.
    edge_query = "MATCH ()--() RETURN COUNT(*) / 2 AS edge_count"
    edge_result = driver.execute_query(edge_query)
    edge_count = edge_result[0][0]["edge_count"]
    print(f"Number of edges: {edge_count}")


def delete_all(driver):
    # Delete everything.
    driver.execute_query(
        "MATCH(n) OPTIONAL MATCH (n)-[r]-() DELETE n, r"
    )


def count_nodes(session):
    # Count the number of nodes.
    query = "MATCH(n) RETURN COUNT(n) AS node_count"
    node_count_result = session.run(query)
    node_count = node_count_result.single()["node_count"]
    return node_count


def count_nodes(session):
    # Count the number of nodes.
    query = "MATCH(n) RETURN COUNT(n) AS node_count"
    node_count_result = session.run(query)
    node_count = node_count_result.single()["node_count"]
    return node_count


import re


def extract_chunks(text):
    # The regular expression matches any substring starting with a $ and
    # continues until the next $ followed by a whitespace or the end of the
    # string.
    pattern = r'\$(?:[^\$]*?)(?=\$\s|\Z)'
    # Find all matching chunks.
    # The re.DOTALL flag is used to make the dot . match all characters,
    # including newline characters.
    chunks = re.findall(pattern, text, re.DOTALL)
    # Strip leading $ and whitespace characters.
    chunks = [chunk.strip().replace("$ ", "") for chunk in chunks]
    return chunks


def execute_query(driver, query):
    if isinstance(query, str):
        driver.execute_query(query)
    else:
        for q in query:
            driver.execute_query(q)


def get_id(element_id):
    # 4:907b90c5-77b7-40ee-bd2b-900a55534cf9:44
    vals = element_id.split(":")
    return vals[2]


def fetch_graph_data(driver):
    # Define the query to fetch nodes and relationships
    query = "MATCH (n)-[r]->(m) RETURN n, r, m"
    # LIMIT 100
    results, _, _ = driver.execute_query(query)
    # Parse the results.
    nodes = {}
    relationships = []
    for record in results:
        n = record['n']
        m = record['m']
        r = record['r']
        # Extract info.
        n_id = get_id(n.element_id)
        m_id = get_id(m.element_id)
        # Add nodes.
        if n_id not in nodes:
            nodes[n_id] = dict(n)
        if m_id not in nodes:
            nodes[m_id] = dict(m)
        relationships.append((n_id, m_id, r.type))
    return nodes, relationships


def plot_graph(driver):
    # Fetch the graph data.
    nodes, relationships = fetch_graph_data(driver)
    # Create a Pyvis Network graph.
    # net = Network(notebook=True)
    net = Network(cdn_resources="remote", directed=True, height='500px',
                  width='100%', notebook=True)
    # Add nodes to the Pyvis graph.
    for node_id, node_data in nodes.items():
        net.add_node(node_id, label=node_data.get('name', str(node_id)),
                     color="#00ff1e")
    # Add edges to the Pyvis graph.
    for source, target, label in relationships:
        net.add_edge(source, target, label=label, color="#162347")
    return net

