# Web Crawling and Network Analysis of Caltech Domain

This project crawls the **Caltech domain** starting from `http://www.caltech.edu`, generates a **directed web graph** with up to 2000 nodes, and then analyzes the graph, producing visualizations and textual reports. It also builds tooling for generating and visualizing networks.

## Project Overview

1. **Crawl** the Caltech homepage and follow links to build a directed graph (up to 2000 nodes).
2. **Analyze** the resulting graph to produce histograms, CDFs, clustering coefficients, and diameters.
3. **Build** a set of tools to generate and visualize common graphs to develop intuition for working with networks.

## Prerequisites

Install the following Python packages via `pip`:

```bash
pip install networkx matplotlib reportlab PyPDF2
```

## How to Run the Code

### Step 1. **Crawl the Caltech Domain**

Run the **crawl.py** script to start crawling from `http://www.caltech.edu`. This will collect up to 2000 nodes and store the directed graph in a pickle file.

```bash
python3 crawl.py
```

- The script uses **fetcher3.py** to handle fetching and parsing of URLs.
- The final graph is saved as `out/caltech_graph_2000.pkl`.

### Step 2. **Analyze the Graph**

Run the **graph_analysis.py** script to:

1. Load the graph from `out/caltech_graph_2000.pkl`.
2. Generate histograms (in-degree, out-degree).
3. Generate CDF functions and plots for in-degree and out-degree.
4. Calculate the overall and average clustering coefficients for the equivalent undirected graph.
5. Calculate the maximum and average diameters for the equivalent undirected graph.
6. Merge graphs and texts into a single resulting PDF.

```bash
python3 graph_analysis.py
```

- The PDF file containing the analysis is saved to `out/caltech_graph_2000_analysis.pdf`.

### Step 3. **Tooling**

Run the **tools.py** script to generate a variety of visualizations for 4 different graphs.

```bash
python3 tools.py
```

- The methods in the script are made to be used as helpers in future projects.
- The pdf of visualizations is saved to `out/varying_visualizations.pdf`.
- The four graphs the visualizations are based on are also saved to the `out` directory.

## Crawling Selection Policy

### Rules

- Only visit pages within the Caltech domain.
- Visit each page only once.
- Ignore pages that are not HTML (ignoring multimedia/data files as well).
- Ignore the parameters in dynamic URLs to visit each dynamic page only once.
- Removes nodes that fail to be crawled due to interruptions/errors.
- Use breadth-first search algorithm to prioritize between urls.

### Pros

- Finds pages closer to the starting URL.
- Keeps diameter of the graph small via BFS.
- Saves time by visiting each page only once.

### Cons

- Potentially skips unique content of dynamic web pages.
- Misses any links within multimedia/data files.
- Misses any links that are not in the HTML source code.
- Misses any new or changed links that are added after each page is visited.

*A comparison of the Caltech and Co-authorship Networks can be found at `coauthor-comparison.md`.*
*A comparison of the Visualizations for different graphs can be found at `visualization-comparison.md`.*
