import unittest
import pytest
from unittest.mock import Mock, patch, call
from demux.demux import register_start_commit, register_action, process_block, process_blocks, get_head_block, Client, initialise_action_dict
from tests.utils import block_1, block_9999, block_10000, block_9999998, block_9999999, fake_block1, fake_block2
from collections import defaultdict

# Robust tests for pydemux

class TestPyDemux(unittest.TestCase):
    #test_register call back functions
    #1. setup test with register() and make fake functions to give to it
    #2. setup a block and assert that something was called
    #def setUp():
    """
    def tearDown(self):
        self.addCleanup(mock.stoall)
    """
    @patch.object(Client, 'get_block')
    @patch.object(Client, 'get_info')
    def test_block_with_no_transactions(self, mock_get_info_head_block, mock_get_block):
        """
        Ensure we can process a block with no transactions
        """
        mock_get_info_head_block.return_value = {'head_block_num': 99999999999}
        # return block 1
        mock_get_block.return_value = block_1
        # mock callback functions
        mock_start_block = Mock()
        mock_action = Mock()
        mock_commit_block = Mock()

        # register the mock callback functions
        register_start_commit(mock_start_block, mock_commit_block)
        register_action(mock_action)
        # process the mock blocks 9999
        initialise_action_dict()
        process_block(1)

        # assertions
        mock_get_block.assert_called_once()
        mock_get_block.assert_called_with(1)
        mock_start_block.assert_called_once()
        assert mock_action.call_count == 0
        mock_commit_block.assert_called_once()

    #Patch should be used like: @patch('package.module.ClassName')
    #@patch('demux.demux.process_block')
    #patch.object passes the thing you want to attach to
    @patch.object(Client, 'get_block') #Client is a class, get_block() is replaced at the class level
    #parameters are in the reverse order
    #@patch.object(Client, 'get_info')
    @patch.object(Client, 'get_info')
    def test_single_mock_block_processing(self, mock_get_info_head_block, mock_get_block): #put get_info first
        """
        Tests block processing on a mocked block
        """
        mock_get_info_head_block.return_value = {'head_block_num': 99999999999}
        # set the patched get_block function to return a manual block 9999
        mock_get_block.return_value = block_9999
        # mock callback functions
        mock_start_block = Mock()
        mock_action = Mock()
        mock_commit_block = Mock()

        # register the mock callback functions
        register_start_commit(mock_start_block, mock_commit_block)
        register_action(mock_action)
        # process the mock blocks 9999
        process_block(9999)
        # assertions
        mock_get_block.assert_called_once()
        mock_get_block.assert_called_with(9999)
        mock_start_block.assert_called_once()
        assert mock_action.call_count == 14
        mock_commit_block.assert_called_once()

    @patch.object(Client, 'get_block')
    @patch.object(Client, 'get_info')
    def test_multiple_mock_block_processing(self, mock_get_info_head_block, mock_get_block):
        """
        Ensures multiple block are processed given a start and end block
        """
        mock_get_info_head_block.return_value = {'head_block_num': 99999999999}
        # get block iterates through blocks each time it is called
        mock_get_block.side_effect = [block_9999998, block_9999999]

        mock_start_block = Mock()
        mock_action = Mock()
        mock_commit_block = Mock()

        # register the mock callback functions
        register_start_commit(mock_start_block, mock_commit_block)
        register_action(mock_action)
        # process the mock blocks 9999
        process_blocks(9999998, 10000000)

        # assertions
        assert mock_get_block.call_count == 2
        assert mock_get_block.call_args_list == [call(9999998), call(9999999)]
        assert mock_start_block.call_count == 2
        assert mock_action.call_count == 132
        assert mock_commit_block.call_count == 2

    @patch.object(Client, 'get_block')
    @patch.object(Client, 'get_info')
    def test_cannot_process_past_head_block(self, mock_get_info_head_block, mock_get_block):
        """
        Tests when the end block is more than one block greater than the head
        block, an assertion is raised and no block is processed
        """
        with pytest.raises(AssertionError) as excinfo:

            mock_get_info_head_block.return_value = {'head_block_num': 9999998}

            mock_start_block = Mock()
            mock_action = Mock()
            mock_commit_block = Mock()

            # register the mock callback functions
            register_start_commit(mock_start_block, mock_commit_block)
            register_action(mock_action)
            # attempts to process the mock blocks 9999998 to 10000000
            process_blocks(9999998, 10000000)

            mock_get_block.assert_not_called()
            mock_start_block.assert_not_called()
            mock_action.assert_not_called()
            mock_commit_block.assert_not_called()

        assert 'ERROR: End block is past head block.' in str(excinfo.value)

    @patch.object(Client, 'get_block')
    @patch.object(Client, 'get_info')
    @patch('demux.demux.time.sleep')
    def test_continuous_block_processing(self, mock_sleep,
                                         mock_get_info_head_block,
                                         mock_get_block):
        """
        Test that continuous polling the block chain for new blocks works correctly
        """
        mock_get_info_head_block.side_effect = [{'head_block_num': 9999998},
                                                {'head_block_num': 9999998},
                                                {'head_block_num': 9999998},
                                                {'head_block_num': 9999999},
                                                {'head_block_num': 9999999}]
        # get block iterates through blocks each time it is called
        mock_get_block.side_effect = [block_9999998, block_9999999]

        mock_start_block = Mock()
        mock_action = Mock()
        mock_commit_block = Mock()

        # register the mock callback functions
        register(mock_action, mock_start_block, mock_commit_block)
        # process the mock blocks 9999
        with pytest.raises(StopIteration) as excinfo:
            process_blocks(9999998)

        # assertions
        assert mock_get_block.call_count == 2
        assert mock_get_block.call_args_list == [call(9999998), call(9999999)]
        assert mock_start_block.call_count == 2
        assert mock_action.call_count == 132
        assert mock_commit_block.call_count == 2
        assert mock_sleep.call_count == 1
