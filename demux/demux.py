from eosapi import Client
import time
from collections import defaultdict

# Global variables
start_block_fn = None
commit_block_fn = None
rollback_fn = None
action_dict = None
head_block = None
last_irr_block = None
block_id_dict = None #key=block_num, value=block_id

# Function to initialise an empty dictionary of accounts per account-name
def initialise_action_dict():
    global action_dict
    action_dict = defaultdict(list)

def initialise_block_id_dict():
    global block_id_dict
    block_id_dict = {}

#*HEAD BLOCK SHOULD IT BE CONSTANTLY UPDATED??***
# Function to get the current head block in the chain
def get_head_block():
    c = Client(nodes=['https://node2.eosphere.io'])
    head_block = c.get_info().get('head_block_num')
    return head_block

def get_last_irr_block_num():
    c = Client(nodes=['https://node2.eosphere.io'])
    irr_block = c.get_info().get('last_irreversible_block_num')
    return irr_block

# Function to register callback functions
def register_start_commit(start_block=None, commit_block=None):
    global start_block_fn
    start_block_fn = start_block
    global commit_block_fn
    commit_block_fn = commit_block

# Function to register a rollback function
def register_rollback(rollback=None):
    global rollback_fn
    rollback_fn = rollback

# Function to register action functions: can specify an account and name, or None
def register_action(action, account=None, name=None, is_effect=False):
    global action_dict
    if is_effect:
        if account is None and name is None:
            action_dict[(None, None, 'effects')].append(action)
        if account is not None and name is not None:
                action_dict[(account,name, 'effects')].append(action)
    elif not is_effect:
        if account is None and name is None:
            action_dict[(None, None, 'updates')].append(action)
        if account is not None and name is not None:
                action_dict[(account, name, 'updates')].append(action)

# Function to process one particular block number
def process_block(block_num, include_effects=False, irreversible_only=False):  #irreversible_only=True, only process up to the last irreversible block, not the head block #head_block=some head block that may or may not be supplied
    global action_dict
    global head_block
    # Only process up to the last irreversible block if irreversible only
    if irreversible_only:
        head_block = get_last_irr_block_num()
    else:
        # Get the current head block number and block number does not exceed it
        head_block = get_head_block()
        #print("head_block=", head_block)

    if int(block_num) > head_block + 1:
        if irreversible_only:
            assert False, "ERROR: Block number is past last irreversible block."
        else:
            assert False, "ERROR: Block number is past head block."
    # Get the current block if it is valid
    c = Client(nodes=['https://node2.eosphere.io'])
    block = c.get_block(block_num) # block is a dictionary
    #print("get_block=", block)
    print("get_info=", c.get_info())
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
                # Only fire Effects if asked
                if include_effects:
                    #Running all the functions that want to get that action, in order registered
                    for action_fn in action_dict[(None, None, 'effects')]:
                        action_fn(a, block=block, transaction=t)
                    #Look up from dict, everything that matches the account and name for that action
                    for action_fn in action_dict[(a['account'], a['name'], 'effects')]:
                        action_fn(a, block=block, transaction=t)
                elif not include_effects:
                    for action_fn in action_dict[(None, None, 'updates')]:
                        action_fn(a, block=block, transaction=t)
                    for action_fn in action_dict[(a['account'], a['name'], 'updates')]:
                        action_fn(a, block=block, transaction=t)
    # After iterating through transaction IDs and actions, commit block processing
    if commit_block_fn is not None:
        commit_block_fn(block=block)

# Function to process multiple blocks
    # start_block = block to start processing from
    # end_block = stops processing at this block (OPTIONAL)
def process_blocks(starting_block, end_block=None, include_effects=False, irreversible_only=False): #irreversible_only=True, only process up to the last irreversible block, not the head block
    global head_block
    if irreversible_only:
        # Only read up to the last irreversible block if irreversible only
        head_block = get_last_irr_block_num()
    else:
        # Get the current head block number and block number does not exceed it
        head_block = get_head_block()
        #print("head_block=", head_block)

    # Start processing from given starting_block
    block_num = starting_block
    # Start and End blocks cannot be more than 1 greater than head block
    if starting_block > head_block + 1:
        if irreversible_only:
            assert False, "ERROR: Starting block is past last irreversible block."
        else:
            assert False, "ERROR: Starting block is past head block."
    # Iterate block processing from start to end block
    if end_block is not None:
        if end_block > head_block + 1:
            if irreversible_only:
                assert False, "ERROR: End block is past last irreversible block."
            else:
                assert False, "ERROR: End block is past head block." #test will look for assertion error
        while block_num < end_block:
            process_block(block_num, include_effects, irreversible_only)
            block_num += 1
    # Iterate block processing from start block to end of chain
    if end_block is None:
         while True:
                if block_num <= head_block:
                    """
                    print("head_block=", head_block)
                    print("block_num=", block_num)
                    if not irreversible_only: #if there rollback_fn is None, just don't say anything
                        initialise_block_id_dict()
                        global block_id_dict #key=block_num, value=block_id
                        # get the current block
                        c = Client(nodes=['https://node2.eosphere.io'])
                        block = c.get_block(block_num)
                        process_block(block_num, include_effects, irreversible_only)
                        block_id_dict[block_num] = block.get('id')
                        # If a rollback has occurred (current block does not point back to the last processed block)
                        if block_num > 1:
                            if block.get('previous') != block_id_dict[(block_num-1)]:
                                print("first_block_id_dict=", block_id_dict)
                                rollback_fn(get_last_irr_block_num()) # call the rollback function with last irr block num
                                block_id_dict.clear() # clear the block id dict
                                global last_irr_block # access the global var last_irr_block
                                block_num = last_irr_block # block_num is set to last_irr_block
                                block_id_dict[block_num] = c.get_block(block_num).get('id') # start block id dict with last irr block name/id
                                block_num += 1 # re-commence from the next block
                                print("second_block_id_dict=", block_id_dict)
                        block_num += 1
                    else:
                        """
                    process_block(block_num, include_effects, irreversible_only)
                    block_num += 1
                if block_num > head_block:
                    old_head_block = head_block
                    if not irreversible_only:
                        head_block = get_last_irr_block_num()
                    else:
                        head_block = get_head_block()
                    if old_head_block == head_block:
                        time.sleep(0.1)
