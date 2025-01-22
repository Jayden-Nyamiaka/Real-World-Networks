from fetcher3 import fetch_links
import networkx as nx
import pickle
from collections import deque
from urllib.error import URLError

def main():
    # Start crawling from the Caltech homepage and limit the number of pages to 100.
    start_url = "http://www.caltech.edu"
    crawl(start_url, 2000, "caltech_graph_2000.pkl")

# Crawl the web starting from the given URL and stop after visiting the given number of pages.
# Selection policy:
    # Rules:
        # - Only visit pages within the Caltech domain.
        # - Visit each page only once.
        # - Ignore pages that are not HTML (ignoring multimedia/data files as well).
        # - Ignore the parameters in dynamic URLs to visit each dynamic page only once.
        # - Removes nodes that fail to be crawled due to interruptions/errors.
        # - Use breadth-first search algorithm to prioritize between urls. 
    # Pros: 
        # - Finds pages closer to the starting URL.
        # - Keeps diameter of the graph small via BFS.
        # - Saves time by visiting each page only once.
    # Cons:
        # - Potentially skips unique content of dynamic web pages.
        # - Misses any links within multimedia/data files.
        # - Misses any links that are not in the HTML source code.
        # - Misses any new or changed links that are added after each page is visited.
def crawl(start_url, limit, save_file = None):
    # Initialize the graph, the queue of URLs to visit, and the set of already visited URLs.
    graph = nx.DiGraph()
    graph.add_node(start_url)
    url_queue = deque([start_url])
    visited = set()

    # Crawl until the queue is empty.
    while url_queue:
        # Get the next url from the queue.
        current_url = url_queue.popleft()

        # Skip if current url has already been visited, else mark it visited for next time.
        if current_url in visited:
            continue
        visited.add(current_url)

        # Try to fetch the hyperlinks in the current page.
        print("n =", graph.number_of_nodes(), "m =", graph.number_of_edges(), "visited", len(visited), "pages, visiting", current_url)
        try:
            # Ignores non-html pages and parameters in dynamic URLs 
            links = fetch_links(current_url)
        except (KeyboardInterrupt, URLError): 
            # Removes the node if there is an error during the fetch.
            print("KeyboardInterrupt or URLError on ", current_url)
            graph.remove_node(current_url)
            continue 
        
        # Continue to next url if no hyperlinks are found.
        if links is None:
            continue

        # Add the hyperlinks to the graph.
        for link in links:
            # Skip if the current url is not in the Caltech domain.
            if (link.find(".caltech.edu") == -1):
                continue
        
            if graph.number_of_nodes() < limit:
                # Make new node and add edge between existing node and new node.
                graph.add_node(link)
                graph.add_edge(current_url, link)
                # Add the hyperlink to the list of next visits if it is not visited yet.
                if link not in visited:
                    url_queue.append(link)
            else: 
                # Only add edges between existing nodes (from this point, no new nodes are added).
                if link not in graph:
                    continue
                graph.add_edge(current_url, link)
    print("Successfully crawled", len(visited), "pages, producing a graph with n =", graph.number_of_nodes(), "nodes and m =", graph.number_of_edges(), "edges.")

    # Save the graph to a file if a save file is specified.
    if save_file:
        with open(save_file, "wb") as f:
            pickle.dump(graph, f)
    print("Graph saved to ", save_file)

if __name__ == "__main__":
    main()