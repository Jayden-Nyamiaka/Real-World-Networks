import random
import pickle
import itertools
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

caltech_graph_pkl_file = "out/caltech_graph_2000.pkl"

def main():
    # Create a PDF file for saving the plots
    pdf = PdfPages("out/varying_visualizations.pdf")

    # Generate the graphs
    gnp = generate_erdos_renyi_graph(40, 0.3, "out/erdos_renyi.pkl")
    ssbm, ssbm_community_map = generate_ssbm_graph(30, 4, 0.75, 0.15, "out/ssbm.pkl")
    caltech150 = generate_first_n_subgraph(caltech_graph_pkl_file, 150, "out/caltech_graph_150.pkl")
    caltech400 = generate_first_n_subgraph(caltech_graph_pkl_file, 400, "out/caltech_graph_400.pkl")
    graphs = [gnp, ssbm, caltech150, caltech400]
    titles = ["Erdos-Renyi G(n=40, p=0.3)", "SSBM G(n=30, k=4, A=0.75, B=0.15)", "Caltech 150 nodes", "Caltech 400 nodes"]
    labels_on = [True, True, False, False]

    # Visualize the graphs in different ways
    for i in range(len(graphs)):
        variety_visualize_graph(graphs[i], "Varying Visualizations for " + titles[i], pdf, labels_on[i])
        visualize_degree_scaled_graph(graphs[i], "Degree Scaled Graph for " + titles[i], pdf, labels_on[i])
        if i == 1:
            visualize_colored_ssbm(graphs[i], ssbm_community_map, "Colored Communities for " + titles[i], pdf, labels_on[i])

    # Close the PDF file
    pdf.close()


# Generate an Erdos-Renyi graph with n nodes and probability p of each edge existing.
# Return the graph and optionally save it to a file if specified.
def generate_erdos_renyi_graph(n, p, save_file=None):
    # Create a new graph
    G = nx.Graph()

    # Each node is connected to every other node with probability p
    nodes = list(range(n))
    for i, j in itertools.combinations(nodes, 2):
        if (random.random() < p):
            G.add_edge(i, j)

    # Save the graph to a file
    if (save_file is not None):
        save_graph(G, save_file)
        print("Erdos-Renyi graph G(n=" +str(n)+ ", p="+str(p)+") and m=" +str(G.number_of_edges())+ " edges has been saved to " +save_file+ ".")
    else:
        print("Erdos-Renyi graph G(n=" +str(n)+ ", p="+str(p)+") and m=" +str(G.number_of_edges())+ " edges has been generated.")

    # Return the graph
    return G

# Generate a Symmetric Stochastic Block Model graph with n nodes, k evenly distributed 
# communities, and probability matrix with A on the diagonal and B outside the diagonal.
# Return the graph and a list mapping each node to its community
# and optionally save it to a file if specified.
def generate_ssbm_graph(n, k, A, B, save_file=None):
    # Initialize undirected graph
    G = nx.Graph()

    # Create the communities
    communities = np.array_split(np.arange(n), k)

    # Map each node to its community and add all nodes to the graph
    node_to_community = np.zeros(n)
    for community_count in range(len(communities)):
        community = communities[community_count]
        for node in community:
            node_to_community[node] = community_count
            G.add_node(node)

    # Connect nodes within and between communities with prob A and B respectively
    for node_i in range(n):
        for node_j in range(node_i+1, n):
            if node_i == node_j:
                continue
            if node_to_community[node_i] == node_to_community[node_j]:
                if random.random() < A:
                    G.add_edge(node_i, node_j)
            else:
                if random.random() < B:
                    G.add_edge(node_i, node_j)

    # Save the graph to a file
    if (save_file is not None):
        save_graph(G, save_file)
        print("SSBM graph G(n=" +str(n)+ ", k="+str(k)+", A="+str(A)+", B="+str(B)+") and m=" +str(G.number_of_edges())+ " edges has been saved to " +save_file+ ".")
    else:
        print("SSBM graph G(n=" +str(n)+ ", k="+str(k)+", A="+str(A)+", B="+str(B)+") and m=" +str(G.number_of_edges())+ " edges has been generated.")

    # Return the graph
    return G, node_to_community
                
# Generate a subgraph of the first n nodes in the graph.
# Return the graph and optionally save it to a file if specified.
def generate_first_n_subgraph(graph_pkl_file, n, save_file=None):
    # Load the graph from the pickle file
    G = None
    try:
        with open(graph_pkl_file, 'rb') as f:
            G = pickle.load(f)
    except:
        pass
    if (G is None):
        print("Error: Graph could not be loaded from", graph_pkl_file)
        return
    if n > G.number_of_nodes():
        print("Error: n is greater than the number of nodes in the graph.")
        return
    
    # Get the first n nodes
    first_n_nodes = list(G.nodes())[:n]

    # Create the subgraph
    G_sub = G.subgraph(first_n_nodes)

    # Save the graph to a file
    if (save_file is not None):
        save_graph(G, save_file)
        print("Subgraph of first " +str(n)+ " nodes has been saved to " +save_file+ ".")
    else:
        print("Subgraph of first " +str(n)+ " nodes has been generated.")

    # Return the graph
    return G_sub

# Make a grid of 6 different visualizations of the graph and save it to a PDF.
def variety_visualize_graph(G, title, pdf_pages=None, with_labels=True):
    print("Visualizing", title)

    # Allocate a figure for the 6 different graph visualizations
    plt.figure(figsize=(12, 20))

    # Spring layout
    plt.subplot(3, 2, 1)
    nx.draw(G, with_labels=with_labels, font_weight='bold', pos=nx.spring_layout(G))
    plt.title("Spring layout")

    # Random layout
    plt.subplot(3, 2, 2)
    nx.draw(G, with_labels=with_labels, pos=nx.random_layout(G))
    plt.title("Random layout")

    # Circular layout
    plt.subplot(3, 2, 3)
    nx.draw(G, with_labels=with_labels, pos=nx.circular_layout(G))
    plt.title("Circular layout")

    # Shell layout
    plt.subplot(3, 2, 4)
    nx.draw(G, with_labels=with_labels, pos=nx.shell_layout(G))
    plt.title("Shell layout")

    # Planar layout
    plt.subplot(3, 2, 5)
    try:
        nx.draw(G, with_labels=with_labels, pos=nx.planar_layout(G))
    except: 
        plt.text(0.5, 0.5, "Layout not possible (G is not planar)", horizontalalignment='center', verticalalignment='center', transform=plt.gca().transAxes)
    plt.title("Planar layout")

    # Spectral layout
    plt.subplot(3, 2, 6)
    nx.draw(G, with_labels=with_labels, pos=nx.spectral_layout(G))
    plt.title("Spectral layout")

    # Give a title to the entire figure
    plt.suptitle(title, fontsize=16)

    # Leave some space for the suptitle 
    plt.tight_layout(rect=[0,0,1,0.95])

    if pdf_pages is not None:
        pdf_pages.savefig()  
        plt.close()  
    else:
        plt.show()   

# Visualize a graph with the node sizes scaled by their degrees.
def visualize_degree_scaled_graph(G, title, pdf_pages=None, with_labels=True):
    print("Visualizing", title)

    # Get the node sizes scaled by their degrees
    node_sizes = [G.degree(node) * 100 for node in G.nodes()]

    # Generate the figure
    plt.figure(figsize=(12, 13))
    plt.title(title, fontsize=20)
    nx.draw(G, node_size=node_sizes, node_color="lightblue", edgecolors="black", linewidths=2, with_labels=with_labels, pos=nx.spring_layout(G))

    if pdf_pages is not None:
        pdf_pages.savefig()  
        plt.close()  
    else:
        plt.show()

# Make a grid of 2 visualizations for the ssbm graph with the communities colored differently.
def visualize_colored_ssbm(G, node_to_community, title, pdf_pages=None, with_labels=True):
    print("Visualizing", title)

    # Allocate a figure for the 2 different graph visualizations
    plt.figure(figsize=(12, 7))

    # Spring layout with colored communities
    plt.subplot(1, 2, 1)
    pos = nx.spring_layout(G)
    colors = [node_to_community[node] for node in G.nodes()]
    nx.draw(G, with_labels=with_labels, font_weight='bold', pos=pos, node_color=colors, cmap=plt.cm.tab20)
    plt.title("Spring layout with colored communities")

    # Circular layout with colored communities
    plt.subplot(1, 2, 2)
    pos = nx.circular_layout(G)
    colors = [node_to_community[node] for node in G.nodes()]
    nx.draw(G, with_labels=with_labels, pos=pos, node_color=colors, cmap=plt.cm.tab20)
    plt.title("Circular layout with colored communities")

    # Give a title to the entire figure
    plt.suptitle(title, fontsize=16)

    # Leave some space for the suptitle 
    plt.tight_layout(rect=[0,0,1,0.95])
    
    if pdf_pages is not None:
        pdf_pages.savefig()  
        plt.close()  
    else:
        plt.show()

# Simply save the graph to a file.
def save_graph(G, save_file):
    with open(save_file, "wb") as f:
        pickle.dump(G, f)
    
if __name__ == "__main__":
    main()