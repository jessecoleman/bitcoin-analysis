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

users = {}
back_users = {}
index = 0
for g in graphs:
    users[index] = g.nodes()
for user in users.keys():
    for hsh in users[user]:
        backusers[hsh] = user

with open('transactions_277198.csv', 'r') as network:
    user_graph = nx.Graph()
    curr_tx = ''
    for line in network.readlines():
        args = line.split(',')
        new_tx = args[0]
        if curr_tx[]

#print(graphs[0])
print(len(graphs))
