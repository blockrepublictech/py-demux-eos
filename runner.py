from demux import demux

# Callback start block function (OPTIONAL)
# Starts this block and stores primitive details in django database
# Actual: Start a database transaction and store block info, then return
def start_block(block): #block=None makes it an optional parameter **kwargs accepts whatever arguments given
    print("Block "+ str(block['block_num']) +" started!")

# Callback action functions
# Stores the action associated with transaction ID
# Actual: Add information about particular action to DB
def action(action, block, transaction): #(action, **kwargs) would ignore the block and transaction params by the user
    #print("action=", action)
    #print("block=", block)
    #print("transaction=", transaction)
    print("Action for account=eosio.unregd, name=add")

def action1(action, block, transaction):
    print("Action for (None, None)")

def action2(action, block, transaction):
    print("Action2 for account=eosio.unregd, name=add")

def action3(action, block, transaction):
    print("Action3 for random account and name")

# Callback commit block function (OPTIONAL)
# Commit block when entire process is
# Actual: Commit the FB transaction
def commit_block(block):
    print ("Block " + str(block['block_num']) + " commited.")


demux.initialise_action_dict()
# Tells demux there are callback functions and registers them
demux.register_start_commit(start_block, commit_block)
demux.register_action(action, "eosio.unregd", "add")
demux.register_action(action2, "eosio.unregd", "add")
demux.register_action(action1)
demux.register_action(action3, "randomAccount", "randomName")

# Input block number to be stored
#block_num = input('Enter a block number: ')
# Iterates through the transactions and actions of the block number
#demux.process_block(block_num)
#print("action_dict=", demux.action_dict)


# Input a start and end block for multi-block processing
start_block = int(input('Enter start block number: '))
end_block = int(input('Enter end block number: '))
#end_block = None
# Input a start and end block for multi-block processing
#demux.process_blocks(start_block)
demux.process_blocks(start_block, end_block)
