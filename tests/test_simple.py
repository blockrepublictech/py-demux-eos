import unittest
import pytest
from mock import Mock
from eosapi import Client
from demux.demux import register, process_block

# Basic tests for pydemux

#def test_assert_false():
#    assert False

class TestSimplePyDemux(unittest.TestCase):
    #test_register call back functions
    #1. setup test with register() and make fake functions to give to it
    #2. setup a block and assert that something was called
    #def setUp():
    #    a

    def test_manual_block_with_no_transactions(self):
        """
        Ensure we can get a block with no transactions
        """
        c = Client(nodes=['https://node2.eosphere.io'])
        block = c.get_block(1)
        assert block.get("transactions") == []

    def test_register_callback_functions(self):
        """
        Ensure that all callback functions are registered by demux
        """
        def start():
            print('Block started.')
        def action():
            print('Block action=')
        def commit():
            print('Block committed.')

        register(start, action, commit)
        from demux.demux import start_block_fn, action_fn, commit_block_fn

        assert start_block_fn == start
        assert action_fn == action
        assert commit_block_fn == commit

    def test_callback_functions_called(self):
        """
        Ensure the start_block function is called when processing a block
        """
        mock_start_block = Mock()
        mock_action = Mock()
        mock_commit_block = Mock()

        register(mock_start_block, mock_action, mock_commit_block)
        process_block(9999)

        mock_start_block.assert_called()
        #mock_action.assert_called()
        mock_commit_block.assert_called()


#def test_smartcontract_filter_actions #in the future
# def test_get_block
    # we want to mock get_block function with mock return value = a manual block
    # the manual block contains transactions and actions and test that relevant functions work with it
#def test_multiple_actions_called(self):
#    """
#    Ensure that action functions are called when there are multiple actions
#    """
#    demux.register(start, action, commit)
#    demux.process_block(1)
#    assert action_fn1 called
#    assert action_fn2 called
#    assert action_fn3 called
#def test_smartcontract_filter_actions(self): #in the future
#    """
#    In the future we want to filter actions for different smart contracts
#    """
#def test_start_block(self):
#    """
#    Ensure that start block is called
#    """
#    def start_block1:
#        return True
#    demux.register(start_block1, action1, commit_block1)
#    demux.process_block(1)
    # Call process_block() on a certian
    #register the star blcok function
    # process_block()
    # assert start_block was called (using a mock)
        #mock = standard part of unit testing
        #called with () for callables
        # callables keep track that it has been called
