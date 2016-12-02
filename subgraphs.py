import networkx as nx

with open('transactions_277198.csv', 'r') as network:
    graph = nx.Graph()
    curr_tx = []
    for line in network.readlines():
        if line.startswith('tx_hash'):
            print(line)
            continue
        attrs = line.split(',')
        #print(attrs)
        if attrs[1] == ' in':
            graph.add_node(attrs[2])
            for tx in curr_tx:
                graph.add_edge(tx, attrs[2])
            # add address to graph to connect
            curr_tx.append(attrs[2])
        else:
            curr_tx = []
graphs = list(nx.connected_component_subgraphs(graph))
#print(graphs[0])
print(len(graphs))
