from eosapi import Client
import time
from collections import defaultdict

# Global variables
start_block_fn = None
commit_block_fn = None
action_dict = None #action_list = {('account', 'name') : [action_fn1, action_fn2], (None, None) : [action_fn3, action_fn4]
# default dict --> key is the name of account, value is list of actions
    # must be able to apply actions that match and all actions that don't match
#[account, name] : list of actions
# list of actions
#function to register aciton, if it is called with no account or name, it should be called on every action
def initialise_action_dict():
    global action_dict
    action_dict = defaultdict(list)

def get_head_block():
    c = Client(nodes=['https://node2.eosphere.io'])
    head_block = c.get_info().get('head_block_num')
    return head_block

# Function to register callback functions
def register_start_commit(start_block=None, commit_block=None):
    global start_block_fn
    start_block_fn = start_block
    global commit_block_fn
    commit_block_fn = commit_block

# Function to register action functions, can specify an account and name, or None
def register_action(action, account=None, name=None, isEffect=True):
    global action_dict
    if account is None and name is None:
        action_dict[(None, None)].append(action)
    if account is not None and name is not None:
            action_dict[(account,name)].append(action)

# Function to process a particular block
def process_block(block_num):
    global action_dict
    # Get the current head block number and block number does not exceed it
    global head_block
    head_block = get_head_block()
    #print("head_block=", head_block)
    if int(block_num) > head_block + 1:
        raise Exception("ERROR: Block number is past head block.")
    # Get the current block if it is valid
    c = Client(nodes=['https://node2.eosphere.io'])
    block = c.get_block(block_num) # block is a dictionary
    #print("get_block=", block)
    #print("get_info=", c.get_info())
    # Start of block processing
    if start_block_fn is not None:
        start_block_fn(block=block) #find a named argument 'block' and assign it block when it's parsed in
    # Get the block and iterate over transaction IDs
    #print("block_num=", block_num)
    transaction_list = block.get('transactions') # get the list of transactions
    for t in transaction_list: # for every dict representing a transaction
        #Get the transaction ID and iterate over actions
        if isinstance(t['trx'], str) == False: # if 'trx' is not a string (these are strange transactions)
            block_action_list = t['trx']['transaction']['actions'] # list of actions associated with each transaction
            for a in block_action_list:
#                print('')
#                print("Action: account=", a['account'])
#                print("action_balance=", a['data']['balance'])
                #Running all the functions that want to get that action, in order registered
                for action_fn in action_dict[(None, None)]:
                    action_fn(a, block=block, transaction=t)
                #Look up from dict, everything that matches the account and name for that action
                for action_fn in action_dict[(a['account'], a['name'])]:
                    action_fn(a, block=block, transaction=t)
    # After iterating through transaction IDs and actions, commit block processing
    if commit_block_fn is not None:
        commit_block_fn(block=block)

# Function to process multiple blocks
    # start_block = block to start processing from
    # end_block = stops processing at this block (OPTIONAL)
def process_blocks(starting_block, end_block=None):
    # Get the current head block number
    global head_block
    head_block = get_head_block()
    block_num = starting_block
    # Start and End blocks cannot be more than 1 greater than head block
    if starting_block > head_block + 1:
        assert False, "ERROR: Starting block is past head block."
    # Iterate block processing from start to end block
    if end_block is not None:
        if end_block > head_block + 1:
            assert False, "ERROR: End block is past head block." #test will look for assertion error
        while block_num < end_block:
            process_block(block_num)
            block_num += 1
    # Iterate block processing from start block to end of chain
    if end_block is None:
         while True:
                if block_num < head_block:
                    process_block(block_num)
                    block_num += 1
                if block_num == head_block:
                    time.sleep(0.1)
                    head_block = get_head_block()
            #instead call get_info all the time, and go to sleep if it is at the head  (100ms)
            # test that the infinite loop works -->
                #mock get_block and get_info, and sleep() and test that things are called in the right way
                #do the mocking so you raise a side_effect (exception), catch the exception and test all the test conditions worked
                # test if i get a block, if start from block < head : it will keep calling get_block for every block
                # if it matches the head --> it will call sleep
                # get out of infinite loop by using side effect from a mock to get an exception (this exits the function), assert it is raised
                # check that all the mocks were called correctly
