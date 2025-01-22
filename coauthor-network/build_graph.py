import networkx as nx
import pickle

def main():
    process_graph("data/gr_qc_coauthorships.txt", "out/gr_qc_coauthorships.pkl")

def process_graph(graph_text_file, save_file):
    # Create a new undirected graph
    G = nx.Graph()

    # Open the file in read mode
    with open(graph_text_file, "r") as f:
        print("Reading graph from", graph_text_file)

        # Read each line in the file
        for line in f:
            # Split the line by space and convert strings to ints
            nodes = list(map(int, line.split()))
            # Add an edge between the two nodes (adding nodes if necessary)
            G.add_edge(nodes[0], nodes[1])
    
    # Check if the graph is empty
    if (len(G.nodes()) == 0):
        print("No nodes found in the graph")
        return

    # Save the graph to a file
    with open(save_file, "wb") as f:
        pickle.dump(G, f)

    # Print end message.
    print("Undirected graph with n =", len(G.nodes()), "nodes and m =", len(G.edges()), "edges has been saved to", save_file)
    
if __name__ == "__main__":
    main()