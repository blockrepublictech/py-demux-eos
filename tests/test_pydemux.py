import unittest
import pytest
from unittest.mock import Mock, patch, call
from demux.demux import register_start_commit, register_action, process_block, process_blocks, get_head_block, Client, initialise_action_dict, initialise_block_id_dict
from tests.utils import block_1, fake_block1, fake_block2
from collections import defaultdict

# Robust tests for pydemux

class TestPyDemux(unittest.TestCase):

    @patch.object(Client, 'get_block')
    @patch.object(Client, 'get_info')
    def test_block_with_no_transactions(self, mock_get_info_head_block, mock_get_block):
        """
        Ensure we can process a block with no transactions
        """
        mock_get_info_head_block.return_value = {'head_block_num': 99999999999}
        # get_block returns manual block_1
        mock_get_block.return_value = block_1
        # mock callback functions
        mock_start_block = Mock()
        mock_action = Mock()
        mock_commit_block = Mock()
        # register the mock callback functions
        register_start_commit(mock_start_block, mock_commit_block)
        register_action(mock_action)
        # process the mock block_1
        initialise_action_dict()
        process_block(1)
        # assertions
        mock_get_block.assert_called_once()
        mock_get_block.assert_called_with(1)
        mock_start_block.assert_called_once()
        assert mock_action.call_count == 0
        mock_commit_block.assert_called_once()

    @patch.object(Client, 'get_block')
    @patch.object(Client, 'get_info')
    def test_single_mock_block_processing(self, mock_get_info_head_block, mock_get_block): #put get_info first
        """
        Tests block processing on a mocked block
        """
        mock_get_info_head_block.return_value = {'head_block_num': 99999999999}
        # get_block returns fake_block1
        mock_get_block.return_value = fake_block1
        # mock callback functions
        mock_start_block = Mock()
        mock_action = Mock()
        mock_commit_block = Mock()

        # register the mock callback functions
        register_start_commit(mock_start_block, mock_commit_block)
        register_action(mock_action)
        # process the mock block fake_block1
        process_block(100)

        # assertions
        mock_get_block.assert_called_once()
        mock_get_block.assert_called_with(100)
        mock_start_block.assert_called_once()
        assert mock_action.call_count == 1
        mock_commit_block.assert_called_once()

    @patch.object(Client, 'get_block')
    @patch.object(Client, 'get_info')
    def test_multiple_mock_block_processing(self, mock_get_info_head_block, mock_get_block):
        """
        Ensures multiple block are processed given a start and end block
        """
        mock_get_info_head_block.return_value = {'head_block_num': 99999999999}
        # get block iterates through blocks each time it is called
        mock_get_block.side_effect = [fake_block1, fake_block2]
        # mock callback functions
        mock_start_block = Mock()
        mock_action = Mock()
        mock_commit_block = Mock()

        # register the mock callback functions
        register_start_commit(mock_start_block, mock_commit_block)
        register_action(mock_action)
        # process the mock blocks 9999 to 10000
        process_blocks(100, 102)

        # assertions
        assert mock_get_block.call_count == 2
        assert mock_get_block.call_args_list == [call(100), call(101)]
        assert mock_start_block.call_count == 2
        assert mock_action.call_count == 3
        assert mock_commit_block.call_count == 2

    @patch.object(Client, 'get_block')
    @patch.object(Client, 'get_info')
    def test_cannot_process_past_head_block(self, mock_get_info_head_block, mock_get_block):
        """
        Tests when the end block is more than one block greater than the head block, an assertion is raised and no block is processed
        """
        with pytest.raises(AssertionError) as excinfo:

            mock_get_info_head_block.return_value = {'head_block_num': 99}

            mock_start_block = Mock()
            mock_action = Mock()
            mock_commit_block = Mock()

            # register the mock callback functions
            register_start_commit(mock_start_block, mock_commit_block)
            register_action(mock_action)
            # attempts to process the mock blocks 9999998 to 10000000
            process_blocks(100, 101)

            mock_get_block.assert_not_called()
            mock_start_block.assert_not_called()
            mock_action.assert_not_called()
            mock_commit_block.assert_not_called()

        assert 'ERROR: End block is past head block.' in str(excinfo.value)

    @patch.object(Client, 'get_block')
    @patch.object(Client, 'get_info')
    def test_cannot_process_past_last_irreversible_block(self, mock_get_info_irr_block, mock_get_block):
        """
        Tests when the end block is more than one block greater than the last irreversible block, an assertion is raised and no block is processed
        """
        with pytest.raises(AssertionError) as excinfo:

            mock_get_info_irr_block.return_value = {'last_irreversible_block_num': 99}

            mock_start_block = Mock()
            mock_action = Mock()
            mock_commit_block = Mock()

            # register the mock callback functions
            register_start_commit(mock_start_block, mock_commit_block)
            register_action(mock_action)
            # attempts to process the mock blocks 9999998 to 10000000
            process_blocks(100, 101, irreversible_only=True)

            mock_get_block.assert_not_called()
            mock_start_block.assert_not_called()
            mock_action.assert_not_called()
            mock_commit_block.assert_not_called()

        assert 'ERROR: End block is past last irreversible block.' in str(excinfo.value)

    @pytest.mark.skip(reason="Failing at the moment, will fix later, added last_irreversible_block_num to get_info mock")
    @patch.object(Client, 'get_block')
    @patch.object(Client, 'get_info')
    @patch('demux.demux.time.sleep')
    def test_continuous_block_processing(self, mock_sleep,
                                         mock_get_info_head_block,
                                         mock_get_block):
        """
        Test that continuous polling the block chain for new blocks works correctly
        """
        initialise_action_dict()
        initialise_block_id_dict()
        # Internal implementation of get_info() which keeps head_block as var,
        mock_get_info_head_block.side_effect = [{'head_block_num': 9999, 'last_irreversible_block_num' : 9900},
                                                {'head_block_num': 9999, 'last_irreversible_block_num' : 9900},
                                                {'head_block_num': 9999, 'last_irreversible_block_num' : 9900},
                                                {'head_block_num': 10000, 'last_irreversible_block_num' : 9900},
                                                {'head_block_num': 10000, 'last_irreversible_block_num' : 9900}]
        # get block iterates through blocks each time it is called
        mock_get_block.side_effect = [block_9999, block_10000]

        mock_start_block = Mock()
        mock_action = Mock()
        mock_commit_block = Mock()

        # register the mock callback functions
        register_start_commit(mock_start_block, mock_commit_block)
        register_action(mock_action)
        # process the mock blocks 9999
        with pytest.raises(StopIteration) as excinfo:
            process_blocks(9999)

        # assertions
        assert mock_get_block.call_count == 2
        assert mock_get_block.call_args_list == [call(9999), call(10000)]
        assert mock_start_block.call_count == 2
        assert mock_action.call_count == 19
        assert mock_commit_block.call_count == 2
        assert mock_sleep.call_count == 1

        # NOTES FROM 22/11/18
        # Internal implementation of get_block(), test that you are never calling for block after head_block, test you sleep() if block=head_block
        # After sleep has been called once, advance the head block, sleep called again (raises exception it is expecting),
        # Never sleep unless at the head of blockchain
        # 1st time sleep, increment head block
        # 2nd time sleep, catches exception

    @pytest.mark.skip(reason="Need to fix this test it is incorrect")
    @patch.object(Client, 'get_block')
    @patch.object(Client, 'get_info')
    @patch('demux.demux.time.sleep')
    @pytest.mark.skip(reason="Failing at the moment, will fix later, added last_irreversible_block_num to get_info mock")
    def test_irreversible_blocks_only(self, mock_sleep,
                                         mock_get_info_head_block,
                                         mock_get_block):
        """
        Test that rollbacks are dealt with correctly when continously polling the block chain
        """
        initialise_action_dict()
        initialise_block_id_dict()
        mock_get_info_head_block.side_effect = [{'head_block_num': 9999, 'last_irreversible_block_num' : 9900},
                                                {'head_block_num': 9999, 'last_irreversible_block_num' : 9900},
                                                {'head_block_num': 9999, 'last_irreversible_block_num' : 9900},
                                                {'head_block_num': 10000, 'last_irreversible_block_num' : 9900},
                                                {'head_block_num': 10000, 'last_irreversible_block_num' : 9900}]
        # get block iterates through blocks each time it is called
        mock_get_block.side_effect = [block_9999, block_10000]
        # mock callback functions
        mock_start_block = Mock()
        mock_action = Mock()
        mock_commit_block = Mock()

        # register the mock callback functions
        register_start_commit(mock_start_block, mock_commit_block)
        register_action(mock_action)
        # process the mock blocks 9999
        with pytest.raises(StopIteration) as excinfo:
            process_blocks(9999)

        # assertions
        assert mock_get_block.call_count == 2
        assert mock_get_block.call_args_list == [call(9999), call(10000)]
        assert mock_start_block.call_count == 2
        assert mock_action.call_count == 19
        assert mock_commit_block.call_count == 2
        assert mock_sleep.call_count == 1

        # NOTES FROM 22/11/18
        #Fake scenario
            # same as previous test but when we get to sleep, simulate rollback
            # increment head_block,
