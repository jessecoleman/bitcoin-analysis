import networkx as nx
import igraph as ig
import pandas as pd

file_path = 'transactions_289335.csv'
with open(file_path, 'r') as network:

    length = 2892195
    graph = nx.Graph()
    curr_tx = []
    # track number of transactions
    tx_hash = ''
    tx_flag = False
    tx_count = 0
    pos_count = 0
    curr_address = ''
    for line in network.readlines():
        # skip header line
        if line.startswith('tx_hash'):
            continue
        attrs = line.split(',')
        print(attrs)
        curr_tx_hash = attrs[0].strip()
        tx_address = attrs[2].strip()
        #initialize tx_hash
        if tx_hash == '':
            tx_hash = curr_tx_hash
            in_address = tx_address
        if attrs[1] == ' in' and curr_tx_hash == tx_hash:
            pos_count = pos_count + 1
            #print(str(pos_count) + '/' + str(length))
            #print(tx_address)
            graph.add_node(tx_address)
            #connect all public addresses from the same transaction
            #print('tx_address: ' + tx_address + ' in_address: ' + in_address)
            graph.add_edge(tx_address, in_address)
        else:
            if tx_flag:
                tx_count = tx_count + 1
            tx_flag = False
            tx_hash = curr_tx_hash
            in_address = tx_address
            graph.add_node(in_address)
            

print(tx_count)

graphs = list(nx.connected_component_subgraphs(graph))
#graphs = list(ig.components(graph, mode="weak"))

print(len(graphs))

users = {}
back_users = {}
index = 0
# create forward reference of users
for g in graphs:
    users[index] = g.nodes()
# create back reference of users
for user in users.keys():
    for hsh in users[user]:
        back_users[hsh] = user


user_graph = nx.MultiDiGraph()
with open(file_path, 'r') as network:
    curr_tx = ''
    # sending user for current transaction
    curr_in_user = ''
    #curr_tx_out_users = []
    in_user_flag = True
    num_found = 0
    num_not_found = 0
    user_graph.add_nodes_from(users)
    for line in network.readlines():
        args = line.split(',')
        if args[1] == ' in' and in_user_flag:
            in_user_flag = False
            try:
                curr_in_user = back_users[args[2]]
            except:
                print('couldn\'t find user')
                curr_in_user = args[2]
        new_tx = args[0]
        if curr_tx == '':
            curr_tx = new_tx
            # if line is part of curr_tx
        if curr_tx == new_tx:
            # try and get user from inputs list, else default to input address
            try:
                curr_user = back_users[args[2]]
                print(curr_user)
                num_found = num_found + 1
            except:
                print('couldn\'t find user')
                curr_user = args[2]
                num_not_found = num_not_found + 1
            if args[1] == ' out':
                user_graph.add_edge(curr_in_user, curr_user, weight=args[5])    
        else:
            curr_tx = new_tx
            #in_user_flag = True
            try:
                curr_in_user = back_users[args[2]]
            except:
                curr_in_user = args[2]
print(num_found)
print(num_not_found)


print(nx.density(user_graph))
print(nx.info(user_graph))
print(nx.number_of_edges(user_graph))
print(nx.number_of_nodes(user_graph))
pagerank = nx.in_degree_centrality(user_graph)
print(pagerank[0])
#pagerank = nx.pagerank_numpy(user_graph, alpha=0.85, weight='weight')
results = pd.DataFrame(pagerank)
print(results.head())

#print(graphs[0])
#print(len(graphs))
