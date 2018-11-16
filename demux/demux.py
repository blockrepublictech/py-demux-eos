from eosapi import Client

start_block_fn = None
action_fn = None
commit_block_fn = None

def get_head_block():
    c = Client(nodes=['https://node2.eosphere.io'])
    head_block = c.get_info().get('head_block_num')
    return head_block

# Function to register callback functions
#def register(start_block, action, commit_block):
def register(action, start_block=None, commit_block=None):
    global start_block_fn
    start_block_fn = start_block
    global action_fn
    action_fn = action
    global commit_block_fn
    commit_block_fn = commit_block

# Function to process a particular block
def process_block(block_num):
    # Get the current head block number and block number does not exceed it
    head_block = get_head_block()
    if int(block_num) > head_block + 1:
        raise Exception("ERROR: Block number is past head block.")
    # Get the current block if it is valid
    c = Client(nodes=['https://node2.eosphere.io'])
    block = c.get_block(block_num) # block is a dictionary
    # Start of block processing
    if start_block_fn is not None:
        start_block_fn(block=block) #find a named argument 'block' and assign it block when it's parsed in
    # Get the block and iterate over transaction IDs
    transaction_list = block.get('transactions') # get the list of transactions
    for t in transaction_list: # for every dict representing a transaction
        #Get the transaction ID and iterate over actions
        if isinstance(t['trx'], str) == False: # if 'trx' is not a string (these are strange transactions)
            action_list = t['trx']['transaction']['actions'] # list of actions associated with each transaction
            for a in action_list:
                action_fn(a, block=block, transaction=t) #block, transactions and actions
    # After iterating through transaction IDs and actions, commit block processing
    if commit_block_fn is not None:
        commit_block_fn(block=block) #block

# Function to process multiple blocks
    # start_block = block to start processing from
    # end_block = stops processing at this block (OPTIONAL)
def process_blocks(start_block, end_block=None):
    # Get the current head block number
    head_block = get_head_block()

    block_num = start_block

    # Start and End blocks cannot be more than 1 greater than head block
    if start_block > head_block + 1:
        raise Exception("ERROR: Start block is past head block.")

    # Iterate block processing from start to end block
    if end_block is not None:
        if end_block > head_block + 1:
            assert False, "ERROR:End block is past head block." #test will look for assertion error
        while block_num < end_block:
            process_block(block_num)
            block_num += 1

    # Iterate block processing from start block to end of chain
    if end_block is None:
        while block_num < head_block:
            process_block(block_num)
            block_num += 1
