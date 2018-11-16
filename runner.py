from demux import demux

# Callback start block function (OPTIONAL)
# Starts this block and stores primitive details in django database
# Actual: Start a database transaction and store block info, then return
def start_block(block): #block=None makes it an optional parameter **kwargs accepts whatever arguments given
    print("Block "+ str(block['block_num']) +" started!")

# Callback action function
# Stores the action associated with transaction ID
# Actual: Add information about particular action to DB
def action(action, block, transaction): #(action, **kwargs) would ignore the block and transaction params by the user
    print("action=", action)
    print("block=", block)
    print("transaction=", transaction)

# Callback commit block function (OPTIONAL)
# Commit block when entire process is
# Actual: Commit the FB transaction
def commit_block(block):
    print ("Block " + str(block['block_num']) + " commited.")

# Input block number to be stored
#block_num = input('Enter a block number: ')

# Tells demux there are callback functions and registers them
demux.register(action, start_block, commit_block)

# Iterates through the transactions and actions of the block number
#demux.process_block(block_num)

# Input a start and end block for multi-block processing
start_block = int(input('Enter start block number: '))
#end_block = int(input('Enter end block number: '))
#end_block = None

# Input a start and end block for multi-block processing
demux.process_blocks(start_block)
#demux.process_blocks(start_block, end_block)
