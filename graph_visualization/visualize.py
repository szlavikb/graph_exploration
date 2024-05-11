import networkx as nx
import matplotlib.pyplot as plt

def graph_visualization(nx_graph_object):
    position = nx.spring_layout(G=nx_graph_object)  

    nx.draw_networkx_nodes(G=nx_graph_object, 
                           pos=position)

    nx.draw_networkx_edges(G=nx_graph_object, 
                           pos=position, 
                           edgelist=nx_graph_object.edges())

    nx.draw_networkx_labels(G=nx_graph_object, 
                            pos=position)

    edge_labels = nx.get_edge_attributes(G=nx_graph_object, 
                                         name="weight")

    nx.draw_networkx_edge_labels(G=nx_graph_object, 
                                 pos=position, 
                                 edge_labels=edge_labels)

    ax = plt.gca()
    ax.margins(0.08)
    plt.axis("off")
    plt.tight_layout()
    plt.show()