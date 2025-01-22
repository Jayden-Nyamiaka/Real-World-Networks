
import os
import pickle
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from PyPDF2 import PdfMerger
from math import comb

temp_dir = "temp"
temp_plots_pdf = "temp/plots.pdf"
temp_text_pdf = "temp/text.pdf"

def main():
    analyze_graph('out/gr_qc_coauthorships.pkl', 'out/gr_qc_coauthorships_analysis.pdf')

def analyze_graph(graph_pkl_file, analysis_pdf_save_file):
    # Create the temp dir if it doesn't exist
    os.makedirs(temp_dir, exist_ok=True)

    # Create a PDF file for saving the plots
    pdf = PdfPages(temp_plots_pdf)

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
    
    n = G.number_of_nodes()
    m = G.number_of_edges()
    print("Loaded undirected graph with n =", n, "nodes and m =", G.number_of_edges(), "edges from", graph_pkl_file)

    
    # Generate degree distribution histogram
    degree_counts = [G.degree(node) for node in G.nodes()]
    plt.figure(figsize=(8, 4))
    plt.hist(degree_counts, bins=range(0, max(degree_counts)+1), alpha=1, color='purple', label='degrees')
    plt.title("Degree distribution")
    plt.xlabel("Number of edges")
    plt.ylabel("Number of nodes")
    pdf.savefig()
    plt.close()


    # Generate out-degree and in-degree CDFs
    degree_cdf = generate_cdf_func(degree_counts)

    # Visualize the out-degree CDF
    plot_cdf(degree_cdf, 0, max(degree_counts))
    plt.title("CDF of node degrees")
    plt.xlabel("Number of edges")
    plt.ylabel("Probability of having x or fewer edges")
    pdf.savefig()
    plt.close()

    # Close the graph PDF
    pdf.close() 

    # Open the PDF file for writing text
    c = canvas.Canvas(temp_text_pdf, pagesize=letter)
    c.setFont("Times-Roman", 10)

    y = 10 * 72 # 10 inches in points (top of the page)
    x = 1 * 72 # 1 inch in points (left margin)

    # Restate the graph. 
    c.drawString(x, y, "The undirected Co-authorship graph has n = " + str(n) + " nodes and m = " + str(G.number_of_edges()) + " edges.")
    y -= 40

    # Output clustering and diameter analysis.
    c.drawString(x, y, "Clustering and Diameter analysis")
    y -= 25

    # Calculate the global and average clustering coefficients of the undirected graph
    global_CC = nx.transitivity(G)
    avg_CC = nx.average_clustering(G)
    c.drawString(x, y, "Global clustering coefficient: " + str(global_CC))
    y -= 20
    c.drawString(x, y, "Average clustering coefficient: " + str(avg_CC))
    y -= 20

    # Calculate the maximum and average diameters of the undirected graph
    max_diameter = nx.diameter(G)
    avg_diameter = nx.average_shortest_path_length(G)
    c.drawString(x, y, "Maximum diameter: " + str(max_diameter))
    y -= 20
    c.drawString(x, y, "Average diameter: " + str(avg_diameter))
    y -= 40

    # Output the Erdos-Renyi comparison. 
    c.drawString(x, y, "Erdos-Renyi comparison")
    y -= 25

    # Calculate the number of triangles in the undirected graph
    T = sum(nx.triangles(G).values()) // 3
    c.drawString(x, y, "Total number of triangles: " + str(T))
    y -= 20

    # Calculate the expected probability parameter p for an equivalent Erdos-Renyi graph
    expected_p = (T / comb(n, 3)) ** (1/3)
    c.drawString(x, y, "An equivalent Erdos-Renyi graph with n=" + str(n) + " nodes would have parameter p=" + str(expected_p) + ".")
    y -= 15
    c.drawString(x, y, "This is because the expected number of triangles in an Erdos-Renyi graph is given by E[T] = (n choose 3) * p^3")
    y -= 15
    c.drawString(x, y, "     where (n choose 3) is the number of possible triangles in the graph")
    y -= 15
    c.drawString(x, y, "     and p^3 is the probability that each of the 3 nodes exist independently")
    y -= 20

    # Reason about the degree distribution of the graph.
    c.drawString(x, y, "The degree distribution for an Erdos-Renyi graph should be binomial.")
    y -= 15
    c.drawString(x, y, "We can conclude this mathematically without a histogram.")
    y -= 15
    c.drawString(x, y, "This is because every edge has probability p of existing such that each node has the same probability of having degree k,")
    y -= 15
    c.drawString(x, y, "     specifically Pr(d = k) = Bin(n-1, k).")
    y -= 20

    c.drawString(x, y, "Real-world networks like this one of co-authorship are known to have a heavy-tail degree distribution, ")
    y -= 15
    c.drawString(x, y, "described by the Pareto distribution, so we know an Erdos-Renyi model would be a poor model for this graph.")
    y -= 15

    # Save text PDF
    c.save()

    # Combine the plots and text into a single PDF
    with open(analysis_pdf_save_file, "wb") as f:
        pdfs = [temp_text_pdf, temp_plots_pdf]
        merger = PdfMerger()
        for pdf in pdfs:
            merger.append(pdf)
        merger.write(f)
        merger.close()

    os.remove(temp_plots_pdf)
    os.remove(temp_text_pdf)
    try:
        os.rmdir(temp_dir)
    except:
        pass


# Generates a CDF function from a list of counts.
def generate_cdf_func(counts):
    counts = sorted(counts)
    max_val = counts[-1]
    n = len(counts)
    set_cdf = []
    count = 0
    for i in range(max_val):
        while counts[count] <= i and count < n:
            count += 1
        set_cdf.append(count/n)
    def cdf(x):
        if (x < 0):
            return 0.0
        if (x >= max_val):
            return 1.0
        return set_cdf[x]
    return cdf

# Plots the CDF of a function given the domain range of the CDF.
def plot_cdf(cdf, min, max):
    x = range(min, max + 1)
    y = [cdf(i) for i in x]
    plt.plot(x, y)

if __name__ == '__main__':
    main()