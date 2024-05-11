import networkx as nx 

def create_nx_object(input_graph: list[dict]): 

    graph  = nx.Graph()

    for edge in input_graph: 

        graph.add_edge(u_of_edge=edge["node_1"], 
                       v_of_edge=edge["node_2"], 
                       weight=edge["weight"])
        
    return graph