from neo4j import GraphDatabase
from pyvis.network import Network


def print_neo4j_version(driver):
    with driver.session() as session:
        result = session.run("CALL dbms.components() YIELD name, versions, edition RETURN name, versions, edition;")
        for record in result:
            print(f"Name: {record['name']}, Version: {record['versions']}, Edition: {record['edition']}")


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


# Define a function to fetch nodes and relationships from Neo4j
def fetch_graph_data(session, query):
    nodes = []
    relationships = []
    
    results = session.run(query)

    for record in results:
        n = record['n']
        m = record['m']
        r = record['r']

        nodes.append((n.id, dict(n)))
        nodes.append((m.id, dict(m)))
        relationships.append((n.id, m.id, r.type))
    return nodes, relationships


def plot_graph(session):
    # Define the query to fetch nodes and relationships
    query = """
    MATCH (n)-[r]->(m)
    RETURN n, r, m
    LIMIT 100
    """

    # Fetch the graph data
    nodes, relationships = fetch_graph_data(session, query)

    # Create a Pyvis Network graph
    #net = Network(notebook=True)
    net = Network(cdn_resources = "remote", directed = True, height = '500px',width = '100%',
              notebook = True)

    # Add nodes to the Pyvis graph
    for node_id, node_data in nodes:
        net.add_node(node_id, label=node_data.get('name', str(node_id)))

    # Add edges to the Pyvis graph
    for source, target, label in relationships:
        net.add_edge(source, target, label=label)
    return net

    # Show the graph
    #net.show("graph.html")
