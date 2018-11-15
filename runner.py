from demux import demux

# Callback start block function (OPTIONAL)
# Starts this block and stores primitive details in django database
# Actual: Start a database transaction and store block info, then return
def start_block():
    print("Block started!")

# Callback action function
# Stores the action associated with transaction ID
# Actual: Add information about particular action to DB
def action(action):
    print("action=", action) # later add function other than printing

# Callback commit block function (OPTIONAL)
# Commit block when entire process is
# Actual: Commit the FB transaction
def commit_block():
    print ("Block commited.")

# Input block number to be stored
block_num = input('Enter a block number: ')

# Tells demux there are callback functions and registers them
demux.register(action, start_block, commit_block)

# Iterates through the transactions and actions of the block number
demux.process_block(block_num)
