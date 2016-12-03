import time
import datetime
from blockchain import blockexplorer
import re
import pandas as pd
import networkx as nx

def get_transactions(height, end):
    begin_height = height
    block = blockexplorer.get_block_height(height)[0]
    curr_date = time.strftime('%Y-%m-%d', time.localtime(block.received_time))
    new_date = curr_date
    date_transactions = []
    #while curr_date == new_date:
    while height < end:
        try:
            print(end - height)
            height = height + 1
            for block in blockexplorer.get_block_height(height):
                new_date = time.strftime('%Y-%m-%d', time.localtime(block.received_time))
                print(new_date)
                #dt = "%d-%02d-%02d-%02d-%02d-%02d"%(block_datetime.year, block_datetime.month, block_datetime.day, block_datetime.hour, block_datetime.minute, block_datetime.second)
                #field specification: ["in", transaction_key, referent_transaction_key, index, public_key, date]   
                date_transactions = date_transactions + block.transactions
        except:
            time.sleep(30)
            #height = height - 1


    input_nodes = nx.Graph()   
    print(date_transactions[0:5])
    lines = []
    lines.append('tx_hash,in_out,address,tx_index,time,value')
    for trns in date_transactions:
        # if block doesn't have any inputs, skip
        curr_nodes = []
        for inpt in trns.inputs:
            try:
                input_nodes.add_node(inpt.address)
                #add edges between all nodes in transaction
                input_nodes.add_edges_from([(inpt.address, out_addr) for out_addr in curr_nodes])
                curr_nodes.append(inpt.address)
                #print('input' + str(inpt.address))
                row = str(trns.hash) + ', ' + 'in, ' + str(inpt.address) + ', ' + str(inpt.tx_index) + ', ' + str(trns.time) + ', ' + str(inpt.value)
                #print(row)
                lines.append(row)
            except AttributeError:
                pass
            
        for outpt in trns.outputs:
            try:
                #print('output' + str(outpt.address))
                #edge = (outpt.address, outpt.value)
                #src.append(edge)
                row = str(trns.hash) + ', ' + 'out, ' + str(outpt.address) + ', ' + str(outpt.tx_index) + ', ' + str(trns.time) + ', ' + str(outpt.value)
                #print(row)
                lines.append(row)
            except AttributeError:
                pass
    with open('transactions_' + str(begin_height) + '.csv', 'w') as file_out:
        file_out.write('\n'.join(lines))



with open("dates_blocks.txt") as f:
    first = int(re.split(',|\\n', f.readline())[1])
    index = 0
    for line in f.readlines():
        
        row = re.split(',|\\n', line)
        if index > 6:
            print(first)
            get_transactions(first, int(row[1]))
        first = int(row[1])
        index = index + 1
        #block = blockexplorer.get_block_height(int(line[1].split('\n')[0]))
        #print(block[0].transactions)
    
