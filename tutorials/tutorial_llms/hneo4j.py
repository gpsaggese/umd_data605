from neo4j import GraphDatabase
from pyvis.network import Network


def delete_all(driver):
    # Delete everything.
    driver.execute_query(
        "MATCH(n) OPTIONAL MATCH (n)-[r]-() DELETE n, r"
    )


# Define a function to fetch nodes and relationships from Neo4j
def fetch_graph_data(driver, query):
    nodes = []
    relationships = []
    
    with driver.session() as session:
        results = session.run(query)
        
        for record in results:
            n = record['n']
            m = record['m']
            r = record['r']
            
            nodes.append((n.id, dict(n)))
            nodes.append((m.id, dict(m)))
            relationships.append((n.id, m.id, r.type))
    return nodes, relationships


def plot_graph(driver):
    # Define the query to fetch nodes and relationships
    query = """
    MATCH (n)-[r]->(m)
    RETURN n, r, m
    LIMIT 100
    """

    # Fetch the graph data
    nodes, relationships = fetch_graph_data(driver, query)

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
