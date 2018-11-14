from demux import demux

# Callback function
# Starts this block and stores primitive details in django database
# Actual: Start a database transaction and store block info, then return
def start_block():
    print("block started=")

# Callback function
# Stores the action associated with transaction ID
# Actual: Add information about particular action to DB
def action(action):
    print("action=", action)

# Commit block when entire process is
# Actual: Commit the FB transaction
def commit_block():
    print ("block commited=")

# Input block number to be stored
block_num = input('Enter a block number: ')

# Tells demux there are callback functions
demux.register(start_block, action, commit_block)

# Iterates through the transactions and actions in the block number
demux.process_block(block_num)
