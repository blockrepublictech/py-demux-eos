# py-demux-eos - Python Demux for EOS
## Deterministic event-sourced state and side effect handling for blockchain applications

This library allows you the programmer to easily write applications which implement
the Demux pattern in Python

## What is the Demux Pattern?

The EOS block chain consists of blocks, transactions and actions. Each block
contains 0 or more transactions, each transaction contains 1 or more actions.
Transactions which contain more than one action the actions after the first
the additional actions are inline actions caused by the smart contract.
For example a game paying out a winner would have one action to finalise the
game and an inline transfer action to create the payout.

Programs conforming to the Demux pattern listen for these actions and update
off chain data stores from the action data.

## Why do we need Demux?

EOS permits us to store data in two different places. One is in memory and
the other is in the chain history. Storing data in memory is very expensive
compared to the RAM prices of modern computers. (Approx 20 cents per 1kb as
of time of writing). Additionally we need to obtain CPU time on a block
producer to run our application, in EOS this is done by staking for CPU.
Even then if we stake for large amounts of CPU there is still a hard limit on
the total amount of CPU a transaction can consume.

This means that storing certain kinds of information in the blockchain is not
possible because it is simply too expensive.

We could get our application to query the block chain via the block producer
API but this could require a large number of round trips in some cases.

Demux allows us to run a server that acts as a cache and allows us to perform
such queries much more cheaply than on chain.

## Updates and Effects

There are two different kinds of functions we can register as action callbacks.
Updates are functions that only change the state of your internal data stores,
Effects are functions which change the world outside our application.

Updates are functions which it is safe to call when processing old blocks (eg
during a restore from the block chain) Effects can only be called when processing
the live blockchain.

A good example would be if we have a charity smart contract. An update would
be a function that maintains a record of donor contributions in a standard
relational database. An Effect would be a function that sends a thank you email
when a contribution over a certain amount is received.

## What new features does py-demux-eos introduce?

We have added the start_block and commit_block callback functions. The original
javascript Demux library lacked these functions. These were added so that you,
the programmer using this library, can write all the data for actions you are
interested in to a database in a single database transaction. This means if you
program crashes or is unexpected closed down part way through a block your
database will not end up in a inconstitent state. The only way to recover from
such an inconsistent state would be replay the entire chain.

## How do I use py-demux-eos in my programs?

Install using pip

```
pip install git+https://github.com/blockrepublictech/py-demux-eos.git@54586e1696b52c81f8c4a3969c2844d7a65c5dee
```

Import the Demux class into your code
```
from demuxeos import Demux
```

Instantiate the Demux object
```
d = Demux()
```

Register block level function and the end point you want to call when you
instantiate the demux class.
```
d = Demux(
  client_node='https://node2.eosphere.io', # The EOS API node you wish to connect to
  start_block_fn=None, # This function is called when we start processing a block
  commit_block_fn=None, # This function is called when we complete processing a block
  rollback_fn=None # This function is called when a chain rollback situation is detected
  )
```

### The start_block function

Function prototype
```
def start_block(block):
  pass
```
Where block is a dict containing all the raw information from the block. Your
implementation of this function could do things like start a database transaction
or record block level information such as the producer, time, or block hash.  

### The commit_block function

Function prototype
```
def commit_block(block):
  pass
```
Where block is a dict containing all the raw information from the block. The
most likely thing your implementation of this function would do is commit
a database tranasction.

### The rollback function

Function prototype
```
def rollback(last_irr_block):
  pass
```
last_irr_block is the block we are rolling back to. Your program should delete
any information after this block for your application's storage.

### Action handlers

To register your action handlers call.

```
d.register_action(action, account=None, name=None, is_effect=False)
```

action is your action handler function
account and name are the account name pair to filter for on this callback. An
example would be account = 'eosio.token' and name = 'transfer'. Setting both
to None will call the action function for every action.
is_effect if true this function is an effect otherwise it is an update

Your action function should have the following prototype.

```
def handle_action(action, block, transaction):
    pass
```
action is a dict containing the information for this action. Block and
transaction are also dicts containing the relevant information.

### Start processing blocks

Process a single block
```
d.process_block(block_num, include_effects=False, irreversible_only=False)
```
block_num = block to process
include_effects = Execute callback registered as both effects and updates,
otherwise just execute updates.
irreversible_only = Only process blocks marked as irreverisble.

Process a range of blocks
```
d.process_blocks(starting_block, end_block=None, include_effects=False, irreversible_only=False)
```
starting_block = block to start processing at
end_block = block to finish processing at, if set to None we loop infintely
processing the head of the chain
include_effects = Execute callback registered as both effects and updates,
otherwise just execute updates.
irreversible_only = Only process blocks marked as irreverisble.

### Example code

A small python command line app has been created to demonstrate how to use this
library. See <https://github.com/blockrepublictech/py-demux-eos-runner>

## Running unit tests

Type the following at the console.

```
virtualenv venv -p python3

source venv/bin/activate

pip install --upgrade pip

pip install --upgrade setuptools urllib3[secure]

pip install requests==2.20.1

pip install pytest
```

Run the unit tests
```
pytest
```

## Support

Feel free to reach out if you have any questions - hello@blockrepublic.tech

Like this library? Please vote for **eosphereiobp** for block producer and we will
be able to make more like this.
