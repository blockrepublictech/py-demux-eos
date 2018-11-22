import unittest
import pytest
from unittest.mock import Mock, patch
from eosapi import Client
from demux.demux import register_start_commit, register_action, process_block, process_blocks, get_head_block, initialise_action_dict

# Basic tests for pydemux, run the process_block() functions and connect to the Client

@pytest.mark.skip(reason="Takes too long to execute, connects to Client each time")
class TestSimplePyDemux(unittest.TestCase):

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

#    @pytest.mark.skip(reason="Not sure why this test is failing, says action() gets unexpected kwarg block")
    def test_start_and_commit_callback_functions_called(self):
        """
        Ensure the start_block and commit_block functions are called when processing a block
        """
        # set up the action_dict
        initialise_action_dict()
        # mock callback functions
        mock_start_block = Mock()
        mock_action = Mock()
        mock_commit_block = Mock()

        register_start_commit(mock_start_block, mock_commit_block)
        register_action(mock_action)
        process_block(9999)
        mock_start_block.assert_called_once()
        mock_action.assert_called()
        mock_commit_block.assert_called_once()


    def test_no_start_block_function(self):
        """
        When users do not want to use the start_block function
        """
        # set up the action_dict
        initialise_action_dict()
        # mock callback functions
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
        # set up the action_dict
        initialise_action_dict()
        # mock callback functions
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
        # set up the action_dict
        initialise_action_dict()
        # mock callback functions
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
        # set up the action_dict
        initialise_action_dict()
        # mock callback functions
        mock_start_block = Mock()
        mock_action = Mock()
        mock_commit_block = Mock()

        register_start_commit(mock_start_block, mock_commit_block)
        register_action(mock_action)
        # process multiple blocks (in this case there are 9)
        process_blocks(9990,9999)

        # assert the callback functions were called for each block only
        assert mock_start_block.call_count == 9
        assert mock_commit_block.call_count == 9
        # NEED: assert that process_block was called for each block
        #assert mock_process_block.call_count == 9
