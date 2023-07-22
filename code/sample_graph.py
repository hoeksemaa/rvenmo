import networkx as nx
G = nx.path_graph(10)
nx.write_gexf(G, "geeksforgeeks.gexf")
