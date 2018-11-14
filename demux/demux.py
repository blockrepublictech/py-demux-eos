from eosapi import Client

start_block_fn = None
action_fn = None
commit_block_fn = None

# Needs c.get_block(block_num) to get all the info associated with an EOS block

# Registers callback functions start_block() and action()
def register(start_block, action, commit_block):
    global start_block_fn
    start_block_fn = start_block
    global action_fn
    action_fn = action
    global commit_block_fn
    commit_block_fn = commit_block

# Iterates through block number
def process_block(block_num):
    # Get the block
    c = Client(nodes=['https://node2.eosphere.io'])
    block = c.get_block(block_num) # block is a dictionary
    start_block_fn()


    # Get the block and iterate over transaction IDs
    transaction_list = block.get('transactions') # get the list of transactions
    for t in transaction_list: # for every dict representing a transaction
        #Get the transaction ID and iterate over actions
        if isinstance(t['trx'], str) == False:
            action_list = t['trx']['transaction']['actions'] # list of actions associated with each transaction
            for a in action_list:
                action_fn(a)


    # After iterating through transaction IDs and actions, call commit_block()
    commit_block_fn()
