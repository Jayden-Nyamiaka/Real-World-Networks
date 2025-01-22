# Comparing Visualizations

For the **Erdos-Renyi Graph**, spring layout, circular, and shell all seem to be equivalently useful. There is no significant difference in degree or clustering for the nodes of G(n, p), so the parameters of visualization don't really affect much.

For the **Symmetric Stochastic Block Model**, by far the most helpful technique was coloring nodes by their community. Coloring nodes by their community combined with either spring or circular distinguished between the connectivity within the same communities and between different communities.

For the **Caltech Domain graphs**, the most helpful technique was scaling nodes by their relative degrees. Since they were many nodes and edges for these graphs compared to the others, the other basic visuals were basically useless, telling us nothing about the graph. However, when scaling by size, the number of high degree to low degree nodes became more apparent and actually gave us information about the graph. Specifically, adding borders around each node also helped so that smaller nodes could still be distinguished over larger nodes.

With respect to labeling, it was very helpful for simple integer node values, but it became incomprehensible for the string url node values. It seems advantageous to only add node labels if the values are short and simple.
