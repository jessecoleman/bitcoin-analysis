import networkx as nx
#import igraph as ig
import pandas as pd
import glob

def calc_centrality(file_path):
    print(file_path)
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
            #print(attrs)
            curr_tx_hash = attrs[0].strip()
            tx_address = attrs[2].strip()
            #initialize tx_hash
            if tx_hash == '':
                tx_hash = curr_tx_hash
                in_address = tx_address
            if attrs[1] == ' in' and curr_tx_hash == tx_hash:
                tx_flag = True
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
    print(len(graph.nodes()))
    graphs = list(nx.connected_component_subgraphs(graph))
    #graphs = list(ig.components(graph, mode="weak"))


    #print(graphs[8].nodes())

    users = {}
    back_users = {}
    index = 0
    # create forward reference of users
    for g in graphs:
        users[index] = g.nodes()
        index = index + 1
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
                    curr_in_user = back_users[args[2].strip()]
                except:
                    print('couldn\'t find user')
                    curr_in_user = args[2].strip()
            new_tx = args[0]
            #print(curr_in_user)
            if curr_tx == '':
                curr_tx = new_tx
                # if line is part of curr_tx
            if curr_tx == new_tx:
                # try and get user from inputs list, else default to input address
                try:
                    curr_user = back_users[args[2].strip()]
                    #print(curr_user)
                    num_found = num_found + 1
                except:
                    #print('couldn\'t find user')
                    curr_user = args[2].strip()
                    num_not_found = num_not_found + 1
                if args[1] == ' out':
                    #print('out')
                    if curr_in_user != curr_user:
                        user_graph.add_edge(curr_in_user, curr_user, weight=args[5])
                    if curr_in_user == '19shhoca4GWsTxDbWPad2MyDXbZWwA6c2M':
                        print('connected')
            else:
                curr_tx = new_tx
                in_user_flag = True
                try:
                    curr_in_user = back_users[args[2].strip()]
                except:
                    curr_in_user = args[2].strip
    print('found: ' + str(num_found))
    print(num_not_found)


    print(nx.info(user_graph))
    in_degree = nx.in_degree_centrality(user_graph)
    out_degree = nx.out_degree_centrality(user_graph)

    #pagerank = nx.pagerank_numpy(user_graph, alpha=0.85, weight='weight')
    results1 = pd.DataFrame.from_dict(in_degree, orient='index')
    #results2 = pd.DataFrame.from_dict(out_degree, orient='index')
    #results = pd.merge(results1, results2, left_index=True, right_index=True)

    results = results.sort_values(by='0_x', ascending=False)
    print(results.head(10))
    # return sorted by in degree
    return (users, results.head(10))

    for i in range(0,10):
        top_in_user = results.head(10).index[i]
        print(len(users[top_in_user]))

    results = results.sort_values(by='0_y', ascending=False)
    print(results.head(20))
    top_out_user = results.head(1).index[0]

    for i in range(0,10):
        top_out_user = results.head(10).index[i]
        print(len(users[top_out_user]))
    #print(graphs[0])
    #print(len(graphs))
    

#file_path = 'transactions_277198.csv'
paths = glob.glob('*.csv')

prev_users = ''
prev_results = ''
for path in paths:
    users, results = calc_centrality(path)
    if prev_users != '':
        for i in range(0, 10):
            print(results[i])
            for i in range(0, 10):
                pass



