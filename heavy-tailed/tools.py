import random
import pickle
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from scipy.stats import linregress
from matplotlib.backends.backend_pdf import PdfPages

# Main function to conduct the experiment and generate the visualizations.
def main():
    # Create a PDF file for saving the plots
    pdf = PdfPages("out/heavy_tailed_graph_analysis.pdf")

    # Conduct the experiment for 3 different instances with the same parameters for better analysis
    for i in range(0, 3):
        # Generate the graphs
        pam, degrees = generate_preferential_attachment_graph(300, "out/preferential_attachment_"+str(i+1)+".pkl")
        config = generate_configuration_model_graph(degrees, "out/configuration_model_"+str(i+1)+".pkl")
        graphs = [pam, config]
        titles = ["Preferential Attachment Model "+str(i+1)+" (T=300)", "Configuration Model "+str(i+1)+" (with Same Degree Distribution)"]

        # Plot the Frequency Plot and Rank Plot of the 2 graphs
        for i in range(len(graphs)):
            plot_freq_and_rank([graphs[i].degree(node) for node in graphs[i].nodes()], titles[i], pdf)

        # Visualize the graphs in different ways
        for i in range(len(graphs)):
            variety_visualize_graph(graphs[i], "Graph Visualizations for " + titles[i], pdf, True, 14, 20)
            visualize_degree_scaled_graph(graphs[i], "Degree Scaled Graph for " + titles[i], pdf, True)

    # Close the PDF file
    pdf.close()

# Generate an undirected Preferential Attachment graph with T nodes.
# Return the graph, a list of degrees of the nodes, and optionally save it to a file if specified.
# If T < 2, print an error message and return None.
def generate_preferential_attachment_graph(T, save_file=None):
    if (T < 2):
        print("Error: T must be at least 2.")
        return None
    
    # Create a new graph with 2 nodes connected by an edge
    G = nx.Graph()
    G.add_edge(0, 1)

    while G.number_of_nodes() < T:
        # Get all the nodes and weight them by their degree
        nodes = list(G.nodes())
        degrees = [G.degree(node) for node in G.nodes()]

        # Choose a neighbor based on the degrees of all existing nodes
        neighbor = random.choices(nodes, weights=degrees, k=1)[0]

        # Add the new node and connect it to the selected neighbor
        node_n = G.number_of_nodes()
        G.add_edge(node_n, neighbor)

    # Save the graph to a file
    if (save_file is not None):
        save_graph(G, save_file)
        print("Preferential Attachment graph G, n=" +str(T)+ ", m=" +str(G.number_of_edges())+ " edges has been saved to " +save_file+ ".")
    else:
        print("Preferential Attachment graph G, n=" +str(T)+ ", m=" +str(G.number_of_edges())+ " edges has been generated.")

    # Return the graph and the list of degrees
    return (G, [G.degree(node) for node in G.nodes()])

# Generate an undirected Configuration Model graph according to the given degree sequence.
# Return the graph and optionally save it to a file if specified.
# If the degree sequence is not valid, print an error message and return None.
def generate_configuration_model_graph(deg_seq, save_file=None):
    if (sum(deg_seq) % 2 != 0):
        print("Error: The sum of the degree sequence must be even.")
        return None
    
    # Create a new graph
    G = nx.Graph()

    # Create a list of stubs for each node based on its degree
    stubs = [i for freqs in ([idx] * deg for idx, deg in enumerate(deg_seq)) for i in freqs]
    
    # Shuffle the stubs
    random.shuffle(stubs)

    # Create an edge between every pair of stubs in the shuffled order
    for i in range(0, len(stubs), 2):
        G.add_edge(stubs[i], stubs[i+1])
    
    # Save the graph to a file
    if (save_file is not None):
        save_graph(G, save_file)
        print("Configuration Model graph G, n=" +str(len(deg_seq))+ ", m=" +str(G.number_of_edges())+ " edges has been saved to " +save_file+ ".")
    else:
        print("Configuration Model graph G, n=" +str(len(deg_seq))+ ", m=" +str(G.number_of_edges())+ " edges has been generated.")

    # Return the graph
    return G

# Plot the Frequency Plot and Rank Plot of the data and save it to a PDF.
# Alternatively, outputs the plots if no PDF file is given.
def plot_freq_and_rank(data, title, pdf_pages=None):
    print("Visualizing", title)

    # Sort the data in ascending order
    data = np.sort(data)

    # Compute the empirical CDF
    ecdf = np.arange(1, len(data)+1) / len(data)

    # Compute the LOB for the frequency plot
    mf, bf, rf, _, _ = linregress(data, ecdf)

    # Compute the LOB for rank plot
    x = np.array(data)
    y = np.array(1-ecdf)
    log_x = np.log(x)
    log_y = np.log(y + 1e-12)
    mr, br, rr, _, _ = linregress(log_x, log_y)
    # Convert back to original scale
    fit_y = np.exp(br) * x**mr  # y = exp(intercept) * x^slope

    # Make the frequency plot
    plt.figure(figsize=(12,13))
    plt.plot(data, ecdf, marker='o', label="Frequency Distribution")
    plt.plot(data, mf * data + bf, label=f"Best Fit: y = {mf:.2f}x + {bf:.2f} with R^2={rf**2:.2f}")
    plt.ylim(-0.05, 1.05)
    plt.legend(loc="lower right")
    plt.xlabel("Value")
    plt.ylabel("Probability of having x or fewer")
    plt.title("Frequency Plot of " + title)
    if pdf_pages is None:
        plt.show()
    else:
        pdf_pages.savefig()
    plt.close()

    # Make the rank plot
    plt.figure(figsize=(12,13))
    plt.loglog(data, 1- ecdf, marker='o', label="Log-Log Rank Distribution")
    plt.loglog(x, fit_y, label=f"Best Fit: y = {np.exp(br):.2f}x^{mr:.2f} with R^2={rr**2:.2f}")
    plt.legend(loc="upper right")
    plt.xlabel("Value (log scale)")
    plt.ylabel("Probability of having more than x (log scale)")
    plt.title("Rank Plot of " + title)
    if pdf_pages is None:
        plt.show()
    else:
        pdf_pages.savefig()
    plt.close()

# Make a grid of 6 different visualizations of the graph and save it to a PDF.
def variety_visualize_graph(G, title, pdf_pages, with_labels=True, font_size=14, node_size=20):
    print("Visualizing", title)

    # Allocate a figure for the 6 different graph visualizations
    plt.figure(figsize=(12, 62))

    # Spring layout
    plt.subplot(6, 1, 1)
    nx.draw(G, with_labels=with_labels, font_size=font_size, node_size=node_size, font_color='r', pos=nx.spring_layout(G))
    plt.title("Spring layout")

    # Random layout
    plt.subplot(6, 1, 2)
    nx.draw(G, with_labels=with_labels, font_size=font_size, node_size=node_size, font_color='r',pos=nx.random_layout(G))
    plt.title("Random layout")

    # Circular layout
    plt.subplot(6, 1, 3)
    nx.draw(G, with_labels=with_labels, font_size=font_size, node_size=node_size, font_color='r',pos=nx.circular_layout(G))
    plt.title("Circular layout")

    # Shell layout
    plt.subplot(6, 1, 4)
    nx.draw(G, with_labels=with_labels, font_size=font_size, node_size=node_size, font_color='r',pos=nx.shell_layout(G))
    plt.title("Shell layout")

    # Planar layout
    plt.subplot(6, 1, 5)
    try:
        nx.draw(G, with_labels=with_labels, font_size=font_size, node_size=node_size, font_color='r', pos=nx.planar_layout(G))
    except: 
        plt.text(0.5, 0.5, "Layout not possible (G is not planar)", horizontalalignment='center', verticalalignment='center', transform=plt.gca().transAxes)
    plt.title("Planar layout")

    # Spectral layout
    plt.subplot(6, 1, 6)
    nx.draw(G, with_labels=with_labels, font_size=font_size, node_size=node_size, font_color='r', pos=nx.spectral_layout(G))
    plt.title("Spectral layout")

    # Give a title to the entire figure
    plt.suptitle(title, fontsize=16)

    # Leave some space for the suptitle 
    plt.tight_layout(rect=[0,0,1,0.95])
    pdf_pages.savefig()    

# Visualize a graph with the node sizes scaled by their degrees.
def visualize_degree_scaled_graph(G, title, pdf_pages, with_labels=True):
    print("Visualizing", title)

    # Get the node sizes scaled by their degrees
    node_sizes = [G.degree(node) * 100 for node in G.nodes()]

    # Generate the figure
    plt.figure(figsize=(12, 13))
    plt.title(title, fontsize=20)
    nx.draw(G, node_size=node_sizes, node_color="lightblue", edgecolors="black", linewidths=2, with_labels=with_labels, pos=nx.spring_layout(G))

    pdf_pages.savefig()  
    plt.close()  

# Simply save the graph to a file.
def save_graph(G, save_file):
    with open(save_file, "wb") as f:
        pickle.dump(G, f)
    
if __name__ == "__main__":
    main()