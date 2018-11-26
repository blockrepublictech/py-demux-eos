from eosapi import Client
import time
from collections import defaultdict
from eosapi.exceptions import HttpAPIError


# Global variables
start_block_fn = None
commit_block_fn = None
rollback_fn = None
action_dict = None
head_block = None
last_irr_block = None
block_id_dict = None
block = None

# Function to get a 'block' object given a specified block number
def get_a_block(block_num):
    c = Client(nodes=['https://node2.eosphere.io'])
    return c.get_block(block_num)

# Function to initialise an empty dictionary of accounts per account-name
def initialise_action_dict():
    global action_dict
    action_dict = defaultdict(list)

# Function to initialise an empty dictionary containing a block's number and id
def initialise_block_id_dict():
    global block_id_dict
    block_id_dict = {}

# Function to get the current head block in the chain
def get_head_block():
    c = Client(nodes=['https://node2.eosphere.io'])
    head_block = c.get_info()['head_block_num']
    return head_block

# Function to get the number of the last irreverisble block on the chain
def get_last_irr_block_num():
    c = Client(nodes=['https://node2.eosphere.io'])
    irr_block = c.get_info()['last_irreversible_block_num']
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

# Function to process a block given a specified block number
def process_block(block_num, include_effects=False, irreversible_only=False): #head_block=some head block that may or may not be supplied
    global action_dict
    global head_block
    # Only process up to the last irreversible block if irreversible only
    if irreversible_only:
        head_block = get_last_irr_block_num()
    else:
        # Get the current head block number in the chain
        head_block = get_head_block()
    # Cannot process past one greater than the head block
    if int(block_num) > head_block + 1:
        if irreversible_only:
            assert False, "ERROR: Block number is past last irreversible block."
        else:
            assert False, "ERROR: Block number is past head block."
    # Get the current block if it is valid
    global block
    block = get_a_block(block_num)
    # Start of block processing
    if start_block_fn is not None:
        start_block_fn(block=block)
    # Get the block and iterate over transaction IDs
    transaction_list = block.get('transactions')
    for t in transaction_list:
        #Get the transaction ID and iterate over actions
        if isinstance(t['trx'], str) == False: # ignore if 'trx' is a string (these are strange transactions)
            block_action_list = t['trx']['transaction']['actions'] # block_action_list = list of actions associated with each block
            for a in block_action_list:
                # Only fire Effects if asked
                if include_effects:
                    #Running all the functions that want to get that action, in order they're registered
                    for action_fn in action_dict[(None, None, 'effects')]:
                        action_fn(a, block=block, transaction=t)
                    #Look up from dict, everything that matches the account and name for that action and run it
                    for action_fn in action_dict[(a['account'], a['name'], 'effects')]:
                        action_fn(a, block=block, transaction=t)
                # Run Update functions if include_effects not specified
                elif not include_effects:
                    for action_fn in action_dict[(None, None, 'updates')]:
                        action_fn(a, block=block, transaction=t)
                    for action_fn in action_dict[(a['account'], a['name'], 'updates')]:
                        action_fn(a, block=block, transaction=t)
    # After iterating through transaction IDs and actions, commit block processing
    if commit_block_fn is not None:
        commit_block_fn(block=block)

# Function to process multiple blocks
# Param: starting_block = block to start processing from
# Param: end_block = stops processing at this block (OPTIONAL)
def process_blocks(starting_block, end_block=None, include_effects=False, irreversible_only=False):
    global head_block
    if irreversible_only:
        # Only read up to the last irreversible block if irreversible only
        head_block = get_last_irr_block_num()
    else:
        # Get the current head block number and block number does not exceed it
        head_block = get_head_block()
    # Start processing from given starting_block
    block_num = starting_block
    # Check that Starting blocks cannot be more than 1 greater than head block
    if starting_block > head_block + 1:
        if irreversible_only:
            assert False, "ERROR: Starting block is past last irreversible block."
        else:
            assert False, "ERROR: Starting block is past head block."
    # If an end_block is specified, process blocks from starting to end block
    if end_block is not None:
        # Check that End blocks cannot be more than 1 greater than head block
        if end_block > head_block + 1:
            if irreversible_only:
                assert False, "ERROR: End block is past last irreversible block."
            else:
                assert False, "ERROR: End block is past head block." #test will look for assertion error
        # Iterate through blocks and process them
        while block_num < end_block:
            process_block(block_num, include_effects, irreversible_only)
            block_num += 1
    # If no end_block is specified, continuosly process blocks until the end of the chain
    if end_block is None:
         while True:
                # Only process blocks that are before or at the head of the chain
                if block_num <= head_block:
                    # If irreversible block only: the last irreverisble block is the 'head' of the chain
                    if irreversible_only:
                        process_block(block_num, include_effects, irreversible_only=True)
                        block_num += 1
                    # If considering ALL blocks
                    elif not irreversible_only:
                        try:
                            process_block(block_num, include_effects, irreversible_only=False)
                        except HttpAPIError as ex:
                            # Call the rollback function if it exists, else silenty continue
                            if rollback_fn is not None:
                                rollback_fn(last_irr_block)
                            # Continue processing from the next block after the last irreversible block
                            block_num = last_irr_block + 1
                        else:
                            global block
                            this_block = block
                            global last_irr_block
                            last_irr_block = get_last_irr_block_num()
                            global block_id_dict
                            # Update block_id dict to only store blocks > last irreversible block
                            block_id_dict = {k : v for (k, v) in block_id_dict if k >= last_irr_block}
                            # Add the current block to the dictionary of block ids
                            block_id_dict[block_num] = this_block['id']
                            # If a rollback has occurred (AKA this block does not point to the last processed block in block_id_dict)
                            if block_num-1 in block_id_dict and this_block['previous'] != block_id_dict[(block_num-1)]:
                                # Call the rollback function if it exists, else silenty continue
                                if rollback_fn is not None:
                                    rollback_fn(last_irr_block)
                                # Continue processing from the next block after the last irreversible block
                                block_num = last_irr_block + 1
                            # Increment to the next block if no rollback has occurred
                            else:
                                block_num += 1
                # If we have processed the head block and have now incremented to the block after: sleep() until head_block is updated
                if block_num > head_block:
                    old_head_block = head_block
                    if irreversible_only:
                        head_block = get_last_irr_block_num()
                    else:
                        head_block = get_head_block()
                    # Sleep for 100ms if head block has not changed
                    if old_head_block == head_block:
                        time.sleep(0.1)
