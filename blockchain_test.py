import time
import datetime
from blockchain import blockexplorer

curr_block_height = 277197

def get_transactions(height):
    block = blockexplorer.get_block_height(height)[0]
    curr_date = time.strftime('%Y-%m-%d', time.localtime(block.received_time))
    new_date = curr_date
    date_transactions = []
    #while curr_date == new_date:
    while True:
        height = height + 1
        for block in blockexplorer.get_block_height(height):
            new_date = time.strftime('%Y-%m-%d-%H-%m-%s', time.localtime(block.received_time))
            print(block.received_time)
            #dt = "%d-%02d-%02d-%02d-%02d-%02d"%(block_datetime.year, block_datetime.month, block_datetime.day, block_datetime.hour, block_datetime.minute, block_datetime.second)
            #field specification: ["in", transaction_key, referent_transaction_key, index, public_key, date]   
            date_transactions = date_transactions + block.transactions
    #print(len(date_transactions))
    return
    adjacent = {}
    for trns in date_transactions:
        for inpt in trns.inputs:
            # if block doesn't have any inputs, skip
            try:
                print('input' + str(inpt.address))
                in_addr = inpt.address
            except AttributeError:
                print('none')
                continue
            for outpt in trns.outputs:
                print('output' + str(outpt.address))
                src = adjacent.get(in_addr, [])
                edge = (outpt.address, outpt.value)
                src.append(edge)
                adjacent[in_addr] = src
            print(inpt.address)
            print(inpt.value)

def find_date_height(date, curr_block_height):
    unix_time = int(time.mktime(datetime.datetime.strptime(date, '%Y-%m-%d').timetuple()))
    #print(date)
    #print(unix_time)
    block_time = get_time(curr_block_height)
    #print(block_time)
    while unix_time > block_time:
        curr_block_height = curr_block_height + 1000
        block_time = get_time(curr_block_height)
        #print(unix_time - block_time)
    while unix_time < block_time:
        curr_block_height = curr_block_height - 100
        block_time = get_time(curr_block_height)
        #print(unix_time - block_time)
    while unix_time > block_time:
        curr_block_height = curr_block_height + 50
        block_time = get_time(curr_block_height)
        #print(unix_time - block_time)
    while unix_time < block_time:
        curr_block_height = curr_block_height - 10
        block_time = get_time(curr_block_height)
        #print(unix_time - block_time)
    while unix_time > block_time:
        curr_block_height = curr_block_height + 1
        block_time = get_time(curr_block_height)
        #print(unix_time - block_time)
    return curr_block_height

def get_time(height):
    try:
        return blockexplorer.get_block_height(height)[0].received_time
    except KeyError:
        print('error')
        return get_time(height + 1)

def print_block(block):
    try:
        print(block.value)
        print(block.tx_index)
        print(block.address)
        print(block.n)
    except AttributeError:
        pass

def find_start_blocks():
    dates = [
    '2013-12-27',
    '2014-01-20',
    '2014-02-17',
    '2014-03-03',
    '2014-04-07',
    '2014-04-28',
    '2014-05-17',
    '2014-06-04',
    '2014-06-19',
    '2014-07-05',
    '2014-07-30',
    '2014-08-14',
    '2014-08-31',
    '2014-09-15',
    '2014-09-30',
    '2014-10-11',
    '2014-10-24',
    '2014-11-01',
    '2014-01-07',
    '2014-01-28',
    '2014-02-21',
    '2014-03-07',
    '2014-04-16',
    '2014-05-03',
    '2014-05-24',
    '2014-06-07',
    '2014-06-24',
    '2014-07-20',
    '2014-08-03',
    '2014-08-22',
    '2014-09-05',
    '2014-09-24',
    '2014-10-04',
    '2014-10-15',
    '2014-10-27',
    '2014-11-04',
    '2014-01-11',
    '2014-02-08',
    '2014-02-24',
    '2014-03-10',
    '2014-04-21',
    '2014-05-10',
    '2014-05-29',
    '2014-06-11',
    '2014-06-30',
    '2014-07-26',
    '2014-08-09',
    '2014-08-27',
    '2014-09-11',
    '2014-09-26',
    '2014-10-08',
    '2014-10-17',
    '2014-10-31',
    '2014-11-06']

    dates.sort()
    #t = time.strftime('%Y-%m-%d', time.localtime(blockexplorer.get_block_height(277198)[0].received_time))
    #print(t)
    idx = 0
    for date in dates:
        if idx > 23:
            #print(idx)
            curr_block_height = find_date_height(date, curr_block_height)
            print(str(date) + '\t' + str(curr_block_height))#file='date_heights.txt')
            #print_block(blockexplorer.get_block_height(curr_block_height)[0].transactions[0].inputs[0])
        idx = idx + 1



def generate_edges():
    with open('dates_blocks.txt', mode='r') as blocks:
        for line in blocks.readlines():
            row = line.split(',')
            #print(row[1])
            block = blockexplorer.get_block_height(int(row[1]))[0]
            print(len(block.transactions))
            #print(dir(block.transactions[0].outputs[0]))
            #print(block.transactions[0].inputs[0])
            print(len(block.transactions[0].outputs))
            for outpt in block.transactions[0].outputs:
                #print('output')
                #print(str(outpt.address) + " " + str(outpt.value))
                #print(outpt.value)
                pass
            for inpt in block.transactions[0].inputs:
                print('input')
                #print(inpt.address)
                print(inpt.script)
            #print_block(block.transactions[0].inputs[0])
            break
           

#generate_edges()
get_transactions(curr_block_height)

def do_shit():
    i = 277190
    #get_transactions(i)

    t1 = '2013-12-27'

    t2 = '2014-11-6'
    time1 = int(time.mktime(datetime.datetime.strptime(t1, '%Y-%m-%d').timetuple()))
    time2 = int(time.mktime(datetime.datetime.strptime(t2, '%Y-%m-%d').timetuple()))

    end = 328783
    while i < end:
        block = blockexplorer.get_block_height(i)[0]
        block_time = time.localtime(block.received_time)
        block_transactions = block.transactions
        #print(len(block_transactions))
        #print(block_transactions[0].relayed_by)
        #print(block.size)
        t = time.strftime('%Y-%m-%d', block_time)
        #print(i)
        print(t)
        
        
        unix_time = int(time.mktime(datetime.datetime.strptime(t, '%Y-%m-%d').timetuple()))
        if(time2 > unix_time):
            i = i + 1
        else:
            i = i + 1