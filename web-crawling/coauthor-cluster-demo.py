import tools
import networkx as nx

# Generates an Erdos-Renyi graph equivalent to co-authorship network and outputs its clustering coefficients.
G = tools.generate_erdos_renyi_graph(4158,0.015861688593415416)
print("Global clustering coefficient:", nx.transitivity(G))
print("Average clustering coefficient:", nx.average_clustering(G))