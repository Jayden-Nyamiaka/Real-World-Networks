# Comparing the Caltech Domain and Co-authorship Networks

Let us compare the Caltech Domain Network and the General Relativity and Quantum Cosmology Network, from the `coauthor-network` project, to each other and from the perspective of our 4 Universal Properties of Real-World Networks.

- It is worth noting that all algorithms used for diameter and clustering coefficients are consistent between projects.

As these are both seemingly typical real-world networks, we can expect them to be relatively similar and possess all of our 4 Universal Properties.

## Property 1: Connectivity -> One Giant Connected Component

**Both graphs are highly connected with a huge strongly connected component.**

The Caltech graph is strongly connected when considered as an undirected graph, and even as a directed graph, it has 1 giant strongly connected component dominating it. The Co-authorship graph we work is actually a subset of the largest connected component in the network, with the original dataset containing 5242 nodes, showing the majority 4158 of 5242 nodes are within the strongly connected component.

## Property 2: Diameter -> Small Diameter

**Both graphs have a small diameter.**

For graph of their sizes, both their maximum and average diameters are relatively small. For n = 200 nodes and n = 4158 nodes respectively, the farthest nodes being only 4 and 17 edges away is disproportionately small compared (compared to Erdos-Renyi).

## Propery 3: Degree -> Heavy-tailed Degree Distribution

**Both graphs possess a heavy-tailed degree distribution.**

Looking at their histogram distributions, we see the heavy-tail of high-degree nodes at the far end and a high low-degree concentration toward the beginning, reflecting the Pareto distribution typical of real-world networks.

## Property 4: Clustering -> High Clustering Coefficient

**Both graphs are highly clustered with high clustering coefficients.**

From our experience with real-world graphs, we know equivalent random Erdos-Renyi graphs would have expected clustering coefficients around 0.01 or much less. However, the clustering coefficients for these graphs are much bigger and at least a magnitude higher. Using Erdos-Renyi as our benchmark, it tells us these graphs are highly clustered.
