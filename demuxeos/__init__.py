# py-demux-eos - Deterministic event-sourced state and side effect handling for blockchain applications
# Copyright (C) 2018 BlockRepublic Pty Ltd
# Licenced under the Apache 2.0 Licence

import time
from collections import defaultdict
from operator import xor
import requests
from .exceptions import UnknownBlockError


class Demux(object):
    def __init__(self, client_node='https://node2.eosphere.io',
                 start_block_fn=None, commit_block_fn=None,
                 rollback_fn=None):
        self._start_block_fn = start_block_fn
        self._commit_block_fn = commit_block_fn
        self._rollback_fn = rollback_fn
        self._action_dict = defaultdict(list)
        self._head_block = None
        self._last_irr_block = None
        self._block_id_dict = {}
        self._block = None
        self._client_node = client_node

    # Function to get a 'block' object given a specified block number
    def _get_block(self, block_num):
        r = requests.post('{}/v1/chain/get_block'.format(self._client_node),
            json={'block_num_or_id': block_num})
        if not (r.status_code >= 200 and r.status_code <= 299):
            raise UnknownBlockError('Error attempting to get block. Statuse code = {}', r.status_code)
        return r.json()

    def _get_info(self):
        return requests.get('{}/v1/chain/get_info'.format(self._client_node)
            ).json()

    # Function to get the current head block in the chain
    def get_head_block(self):
        return self._get_info()['head_block_num']

    # Function to get the number of the last irreverisble block on the chain
    def get_last_irr_block_num(self):
        return self._get_info()['last_irreversible_block_num']

    # Function to register action functions: can specify an account and name, or None
    def register_action(self, action, account=None, name=None, is_effect=False):
        assert not xor(bool(account), bool(name)), "Account and name must both be valid or both be none"
        self._action_dict[(account,name, 'effects' if is_effect else 'updates')].append(action)

    # Function to process a block given a specified block number
    def process_block(self, block_num, include_effects=False, irreversible_only=False): #head_block=some head block that may or may not be supplied
        # Only process up to the last irreversible block if irreversible only
        if irreversible_only:
            self._head_block = self.get_last_irr_block_num()
        else:
            # Get the current head block number in the chain
            self._head_block = self.get_head_block()
        # Cannot process past one greater than the head block
        if int(block_num) > self._head_block + 1:
            if irreversible_only:
                assert False, "ERROR: Block number is past last irreversible block."
            else:
                assert False, "ERROR: Block number is past head block."
        # Get the current block if it is valid
        self._block = self._get_block(block_num)
        # Start of block processing
        if self._start_block_fn is not None:
            self._start_block_fn(block=self._block)
        # Get the block and iterate over transaction IDs
        transaction_list = self._block.get('transactions')
        for t in transaction_list:
            #Get the transaction ID and iterate over actions
            if isinstance(t['trx'], str) == False: # ignore if 'trx' is a string (these are strange transactions)
                block_action_list = t['trx']['transaction']['actions'] # block_action_list = list of actions associated with each block
                for a in block_action_list:
                    #Running all the functions that want to get that action, in order they're registered
                    # and depending upon if they are effects or updates
                    for action_fn in self._action_dict[(None, None, 'effects' if include_effects else 'updates')]:
                        action_fn(a, block=self._block, transaction=t)
                    #Look up from dict, everything that matches the account and name for that action and run it
                    for action_fn in self._action_dict[(a['account'], a['name'], 'effects' if include_effects else 'updates')]:
                        action_fn(a, block=self._block, transaction=t)
        # After iterating through transaction IDs and actions, commit block processing
        if self._commit_block_fn is not None:
            self._commit_block_fn(block=self._block)

    def _post_rollback_process(self):
        # Verify the irreversible blocks still matches and clean up the now defunction block history
        if self._last_irr_block in self._block_id_dict:
            self._block_id_dict = {self._last_irr_block:
                                   self._block_id_dict[self._last_irr_block]}
            block = self._get_block(self._last_irr_block)
            assert block['id'] == self._block_id_dict[self._last_irr_block], 'Irreversible block mismatch halting'
        else:
            self._block_id_dict = {}

    # Function to process multiple blocks
    # Param: starting_block = block to start processing from
    # Param: end_block = stops processing at this block (OPTIONAL)
    def process_blocks(self, starting_block, end_block=None, include_effects=False, irreversible_only=False):
        if irreversible_only:
            # Only read up to the last irreversible block if irreversible only
            self._head_block = self.get_last_irr_block_num()
        else:
            # Get the current head block number and block number does not exceed it
            self._head_block = self.get_head_block()
        # Start processing from given starting_block
        block_num = starting_block
        # Check that Starting blocks cannot be more than 1 greater than head block
        if starting_block > self._head_block + 1:
            if irreversible_only:
                assert False, "ERROR: Starting block is past last irreversible block."
            else:
                assert False, "ERROR: Starting block is past head block."
        # If an end_block is specified, process blocks from starting to end block
        if end_block is not None:
            # Check that End blocks cannot be more than 1 greater than head block
            if end_block > self._head_block + 1:
                if irreversible_only:
                    assert False, "ERROR: End block is past last irreversible block."
                else:
                    assert False, "ERROR: End block is past head block." #test will look for assertion error
            # Iterate through blocks and process them
            while block_num < end_block:
                self.process_block(block_num, include_effects, irreversible_only)
                block_num += 1
        # If no end_block is specified, continuosly process blocks until the end of the chain
        if end_block is None:
             while True:
                    # Only process blocks that are before or at the head of the chain
                    if block_num <= self._head_block:
                        # If irreversible block only: the last irreverisble block is the 'head' of the chain
                        if irreversible_only:
                            self.process_block(block_num, include_effects, irreversible_only=True)
                            block_num += 1
                        # If considering ALL blocks
                        elif not irreversible_only:
                            try:
                                self.process_block(block_num, include_effects, irreversible_only=False)
                            except UnknownBlockError as ex:
                                # Call the rollback function if it exists, else silenty continue
                                if self._rollback_fn is not None:
                                    self._rollback_fn(last_irr_block)
                                self._post_rollback_process()
                                # Continue processing from the next block after the last irreversible block
                                block_num = self._last_irr_block + 1
                            else:
                                this_block = self._block
                                self._last_irr_block = self.get_last_irr_block_num()
                                # Update block_id dict to only store blocks > last irreversible block
                                self._block_id_dict = {k : v for (k, v) in self._block_id_dict.items()
                                                 if k >= self._last_irr_block}
                                # Add the current block to the dictionary of block ids
                                self._block_id_dict[block_num] = this_block['id']
                                # If a rollback has occurred (AKA this block does not point to the last processed block in block_id_dict)
                                if block_num-1 in self._block_id_dict and this_block['previous'] != self._block_id_dict[(block_num-1)]:
                                    # Call the rollback function if it exists, else silenty continue
                                    if self._rollback_fn is not None:
                                        self._rollback_fn(self._last_irr_block)
                                    self._post_rollback_process()
                                    # Continue processing from the next block after the last irreversible block
                                    block_num = self._last_irr_block + 1
                                # Increment to the next block if no rollback has occurred
                                else:
                                    block_num += 1
                    # If we have processed the head block and have now incremented to the block after: sleep() until head_block is updated
                    if block_num > self._head_block:
                        old_head_block = self._head_block
                        if irreversible_only:
                            self._head_block = self.get_last_irr_block_num()
                        else:
                            self._head_block = self.get_head_block()
                            if self._head_block < old_head_block:
                                # Call the rollback function if it exists, else silenty continue
                                if self._rollback_fn is not None:
                                    self._rollback_fn(self._last_irr_block)
                                self._post_rollback_process()
                                # Continue processing from the next block after the last irreversible block
                                block_num = self._last_irr_block + 1
                        # Sleep for 100ms if head block has not changed
                        if old_head_block == self._head_block:
                            time.sleep(0.1)
