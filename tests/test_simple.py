import unittest
import pytest
from unittest.mock import Mock, patch
from eosapi import Client
from demux.demux import register_start_commit, register_action, process_block, process_blocks, get_head_block


# Basic tests for pydemux

class TestSimplePyDemux(unittest.TestCase):
    #test_register call back functions
    #1. setup test with register() and make fake functions to give to it
    #2. setup a block and assert that something was called
    #def setUp():
    def test_register_all_callback_functions(self):
        """
        Ensure that all callback functions are registered by demux
        """
        def start():
            print('Block started.')
        def action():
            print('Block action=')
        def commit():
            print('Block committed.')

        register_start_commit(start, commit)
        register_action(action)
        from demux.demux import start_block_fn, commit_block_fn

        assert start_block_fn == start
#        assert action_fn == action
        assert commit_block_fn == commit

#    def test_start_and_commit_callback_functions_called(self):
        """
        Ensure the start_block and commit_block functions are called when processing a block
        """
        """
        mock_start_block = Mock()
        mock_action = Mock()
        mock_commit_block = Mock()

        register_start_commit(mock_start_block, mock_commit_block)
        register_action(mock_action)
        process_block(9999)
        mock_start_block.assert_called_once()
        mock_action.assert_called()
        mock_commit_block.assert_called_once()
        """

    def test_no_start_block_function(self):
        """
        When users do not want to use the start_block function
        """
        mock_start_block = Mock()
        mock_action = Mock()
        mock_commit_block = Mock()

        register_start_commit(mock_commit_block)
        register_action(mock_action)
        process_block(9999)

        mock_start_block.assert_not_called()
        mock_action.assert_called()
        mock_commit_block.assert_called_once()

    def test_no_commit_block_function(self):
        """
        When users do not want to use the commit_block function
        """
        mock_start_block = Mock()
        mock_action = Mock()
        mock_commit_block = Mock()

        register_start_commit(mock_start_block)
        register_action(mock_action)
        process_block(9999)

        mock_start_block.assert_called_once()
        mock_action.assert_called()
        mock_commit_block.assert_not_called()

    def test_only_action_function(self):
        """
        When users only want to use the action function
        """
        mock_start_block = Mock()
        mock_action = Mock()
        mock_commit_block = Mock()

        register_action(mock_action)
        process_block(9999)

        mock_start_block.assert_not_called()
        mock_action.assert_called()
        mock_commit_block.assert_not_called()


    def test_multiple_block_processing_with_start_and_end_block(self):
        """
        Ensure we can process multiple blocks with a start and end block
        """
        # mock callback functions
        mock_start_block = Mock()
        mock_action = Mock()
        mock_commit_block = Mock()

        # register mock callback functions
        register_start_commit(mock_start_block, mock_commit_block)
        register_action(mock_action)
        # process multiple blocks (in this case there are 9)
        process_blocks(9990,9999)

        # assert the callback functions were called for each block only
        assert mock_start_block.call_count == 9
        assert mock_commit_block.call_count == 9
        # NEED: assert that process_block was called for each block
        #assert mock_process_block.call_count == 9

#    def test_multiple_block_processing_with_no_end_block(self):
#        """
#        Ensure that multiple blocks are processed from a starting block to the head block
#        """
#        # mock callback functions
#        mock_start_block = Mock()
#        mock_action = Mock()
#        mock_commit_block = Mock()
#
#        # register mock callback functions
#        register(mock_action, mock_start_block, mock_commit_block)
#        # process multiple blocks (in this case there are 9)
#        process_blocks(9990)

        # assert start_block is called for block 9990

        # assert start_block is not called for block after head block



#    def test_cannot_process_block_after_head_block(self)
#        """
#        Ensure exception is raised when start_block, current_block, end_block exceeds head_block, it shouldn't run anything if end block > head_block
#        """
#        #mock get_info and get_block using patch
#        mock_get_info = Mock()


#    def test_start_and_commit_block_receives_block_param(self):
#        """
#        Ensure start_block_fn and commit_block_fn successfully receives block as param
#        """

#    def test_action_fn_receives_correct_param(self):
#        """
#        Ensures action_fn receives correct block, transaction, action params
#        """
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
