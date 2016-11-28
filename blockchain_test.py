import time
import datetime
from blockchain import blockexplorer

def get_transactions(height):
    block = blockexplorer.get_block_height(height)[0]
    curr_date = time.strftime('%Y-%m-%d', time.localtime(block.received_time))
    new_date = curr_date
    date_transactions = []
    while curr_date == new_date:
        height = height + 1
        block = blockexplorer.get_block_height(height)[0]
        new_date = time.strftime('%Y-%m-%d', time.localtime(block.received_time))
        print(curr_date)
        date_transactions = date_transactions + block.transactions
        print(len(block.transactions))
    print(len(date_transactions))

    adjacent = {}
    for trns in date_transactions:
        print('value')
        print(trns.inputs)
        for inpt in trns.inputs:
            # if block doesn't have any inputs, skip
            try:
                print('input' + str(inpt.address))
                in_addr = inpt.address
            except AttributeError:
                print('none')
                continue
            print(len(trns.outputs))
            print(trns.outputs)
            for outpt in trns.outputs:
                print('output' + str(outpt.address))
                src = adjacent.get(in_addr, [])# if adjacent[inpt.address].get())
                edge = (outpt.address, outpt.value)
                src.append(edge)
                adjacent[in_addr] = src
            print(inpt.address)
            print(inpt.value)



i = 277190
get_transactions(i)

t1 = '2013-12-27'
t2 = '2014-11-6'
time1 = int(time.mktime(datetime.datetime.strptime(t1, '%Y-%m-%d').timetuple()))
time2 = int(time.mktime(datetime.datetime.strptime(t2, '%Y-%m-%d').timetuple()))

end = 328783
while i < end:
    block = blockexplorer.get_block_height(i)[0]
    block_time = time.localtime(block.received_time)
    block_transactions = block.transactions
    print(len(block_transactions))
    print(block_transactions[0].relayed_by)
    print(block.size)
    t = time.strftime('%Y-%m-%d', block_time)
    #print(i)
    print(t)
    
    
    unix_time = int(time.mktime(datetime.datetime.strptime(t, '%Y-%m-%d').timetuple()))
    if(time2 > unix_time):
        i = i + 1
    else:
       i = i + 1