
import os
import pickle
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from PyPDF2 import PdfMerger

temp_dir = "temp"
temp_plots_pdf = "temp/plots.pdf"
temp_text_pdf = "temp/text.pdf"

def main():
    analyze_graph('out/caltech_graph_2000.pkl', 'out/caltech_graph_2000_analysis.pdf')

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
    print("Loaded graph with n =", G.number_of_nodes(), "nodes and m =", G.number_of_edges(), "edges from", graph_pkl_file)

    # Generate out-degree histogram
    out_degree_counts = [G.out_degree(node) for node in G.nodes()]
    plt.figure(figsize=(8, 4))
    plt.hist(out_degree_counts, bins=range(0, max(out_degree_counts)+1), alpha=1, color='b', label='Out-degrees')
    plt.title("Distribution of hyperlinks pointing from a page (out-degrees)")
    plt.xlabel("Number of out hyperlinks")
    plt.ylabel("Number of pages")
    pdf.savefig()
    plt.close()

    # Generate in-degree histogram
    in_degree_counts = [G.in_degree(node) for node in G.nodes()]
    plt.figure(figsize=(8, 4))
    plt.hist(in_degree_counts, bins=range(0, max(in_degree_counts)+1), alpha=1, color='r', label='In-degrees')
    plt.title("Distribution of hyperlinks pointing to a page (in-degrees)")
    plt.xlabel("Number of in hyperlinks")
    plt.ylabel("Number of pages")
    pdf.savefig()
    plt.close()

    # Generate overlayed out-degree and in-degree histogram
    plt.figure(figsize=(8, 4))
    plt.hist(out_degree_counts, bins=range(0, max(out_degree_counts)+1), alpha=0.5, color='b', label='Out-degrees')
    plt.hist(in_degree_counts, bins=range(0, max(in_degree_counts)+1), alpha=0.5, color='r', label='In-degrees')
    plt.title("Distribution of hyperlinks pointing to and from a page")
    plt.xlabel("Number of hyperlinks")
    plt.ylabel("Number of pages")
    plt.legend()
    pdf.savefig()
    plt.close()

    # Generate out-degree and in-degree CDFs
    out_degree_cdf = generate_cdf_func(out_degree_counts)
    in_degree_cdf = generate_cdf_func(in_degree_counts)

    # Visualize the out-degree CDF
    plot_cdf(out_degree_cdf, 0, max(out_degree_counts))
    plt.title("CDF of hyperlinks pointing from a page (out-degrees)")
    plt.xlabel("Number of out hyperlinks")
    plt.ylabel("Probability of having x or fewer out hyperlinks")
    pdf.savefig()
    plt.close()

    # Visualize the in-degree CDF
    plot_cdf(in_degree_cdf, 0, max(in_degree_counts))
    plt.title("CDF of hyperlinks pointing to a page (in-degrees)")
    plt.xlabel("Number of in hyperlinks")
    plt.ylabel("Probability of having x or fewer in hyperlinks")
    pdf.savefig()
    plt.close()

    # Close the graph PDF
    pdf.close() 

    # Open the PDF file for writing text
    c = canvas.Canvas(temp_text_pdf, pagesize=letter)
    y = 10 * 72 # 10 inches in points (top of the page)

    # Add the selection policy to the PDF
    c.drawString(100, y, "The Caltech Graph has n = " + str(G.number_of_nodes()) + " nodes and m = " + str(G.number_of_edges()) + " edges.")
    y -= 15
    c.drawString(100, y, "It was generated using the following selection policy:")
    y -= 30
    for line in selection_policy:
        c.drawString(100, y, line)
        y -= 15
    y -= 50

    # Treat the graph as undirected for clustering and diameter calculations
    G_undirected = G.to_undirected()
    c.drawString(100, y, "Clustering and Diameter analysis (treating the graph as undirected)")
    y -= 30

    # Calculate the global and average clustering coefficients of the undirected graph
    global_CC = nx.transitivity(G_undirected)
    avg_CC = nx.average_clustering(G_undirected)
    c.drawString(100, y, "Global clustering coefficient: " + str(global_CC))
    y -= 20
    c.drawString(100, y, "Average clustering coefficient: " + str(avg_CC))
    y -= 30

    # Calculate the maximum and average diameters of the undirected graph
    max_diameter = nx.diameter(G_undirected)
    avg_diameter = nx.average_shortest_path_length(G_undirected)
    c.drawString(100, y, "Maximum diameter: " + str(max_diameter))
    y -= 20
    c.drawString(100, y, "Average diameter: " + str(avg_diameter))
    y -= 30

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
    
# Description of selection policy
selection_policy = [
    "Rules:",
    " - Only visit pages within the Caltech domain.",
    " - Visit each page only once.",
    " - Ignore pages that are not HTML (ignoring multimedia/data files as well).",
    " - Ignore the parameters in dynamic URLs to visit each dynamic page only once.",
    " - Removes nodes that fail to be crawled due to interruptions/errors.",
    " - Use breadth-first search algorithm to prioritize between urls.",
    "Pros:",
    " - Finds pages closer to the starting URL.",
    " - Keeps diameter of the graph small via BFS.",
    " - Saves time by visiting each page only once.",
    "Cons:",
    " - Potentially skips unique content of dynamic web pages.",
    " - Misses any links within multimedia/data files.",
    " - Misses any links that are not in the HTML source code.",
    " - Misses any new or changed links that are added after each page is visited."
]


if __name__ == '__main__':
    main()