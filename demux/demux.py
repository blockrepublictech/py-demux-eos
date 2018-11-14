start_block_fn = None
action_fn = None

# Needs c.get_block(block_num) to get all the info associated with an EOS block

# Registers callback functions start_block() and action()
def register(start_block, action):
    global start_block_fn
    start_block_fn = start_block
    global action_fn
    action_fn = action

# Iterates through block number
def process_block(block_num, commit_block):
    # Get the block and iterate over transaction IDs
    for transaction in block_num:
        print('transaction')
    #Get the transaction ID and iterate over actions
    for action in transaction:
        action_fn(action)
    # After iterating through transaction IDs and actions, call commit_block()
    #commit_block = True
