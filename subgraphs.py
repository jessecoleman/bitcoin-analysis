import networkx as nx

with open('transactions_277198.csv', 'r') as network:
    graph = nx.Graph()
    curr_tx = []
    # track number of transactions
    tx_hash = ''
    tx_flag = True
    tx_count = 0
    for line in network.readlines():
        # skip header line
        if line.startswith('tx_hash'):
            print(line)
            continue
        attrs = line.split(',')
        curr_tx_hash = attrs[0]
        #initialize tx_hash
        if tx_hash == '':
            tx_hash = curr_tx_hash
        if attrs[1] == ' in' and curr_tx_hash == tx_hash:
            tx_flag = True
            graph.add_node(attrs[2].strip())
            for tx in curr_tx:
                graph.add_edge(tx, attrs[2])
            # add address to graph to connect
            curr_tx.append(attrs[2])
        else:
            if tx_flag:
                tx_count = tx_count + 1
            tx_flag = False
            tx_hash = curr_tx_hash
            curr_tx = []
            

print(tx_count)

graphs = list(nx.connected_component_subgraphs(graph))

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



with open('transactions_277198.csv', 'r') as network:
    user_graph = nx.MultiDiGraph()
    curr_tx = ''
    # sending user for current transaction
    curr_in_user = ''
    #curr_tx_out_users = []
    in_user_flag = True
    
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
            except:
                curr_user = args[2]
            if args[1] == ' out':
                user_graph.add_edge(curr_in_user, curr_user, args[5])    
        else:
            curr_tx = new_tx
            #in_user_flag = True
            try:
                curr_in_user = back_users[args[2]]
            except:
                curr_in_user = args[2]


            


#print(graphs[0])
#print(len(graphs))
