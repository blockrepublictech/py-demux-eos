import unittest
import pytest
from unittest.mock import Mock, patch, call
from demux.demux import register_start_commit, register_action, process_block, process_blocks, get_head_block, Client, initialise_action_dict
from tests.utils import block_1, block_9999, block_10000, block_9999998, block_9999999, fake_block1, fake_block2
from collections import defaultdict

class TestActionsPyDemux(unittest.TestCase):
    """
    def setup_method(self, method):
        self.mock_start_block = Mock()
        self.mock_action1 = Mock()
        self.mock_action2 = Mock()
        self.mock_action3 = Mock()
        self.mock_commit_block = Mock()
    """
    @patch.object(Client, 'get_block')
    @patch.object(Client, 'get_info')
    def test_register_multiple_action_functions(self, mock_get_info_head_block, mock_get_block):
        """
        Tests that multiple action functions are registered to a specific account and name, including actions with no account or name specified
        """
        mock_get_info_head_block.return_value = {'head_block_num': 99999999999}
        mock_get_block.return_value = fake_block2
        # mock callback functions
        mock_start_block = Mock()
        mock_action1 = Mock()
        mock_action2 = Mock()
        mock_action3 = Mock()
        mock_commit_block = Mock()
        # parent mock for checking call order
        m = Mock()
        m.mock_action1, m.mock_action2, m.mock_action3 = mock_action1, mock_action2, mock_action3
        m.mock_calls
        # set up the action_dict
        initialise_action_dict()
        # register the mock callback functions
        register_start_commit(mock_start_block, mock_commit_block)
        register_action(mock_action1, "account21", "name21")
        register_action(mock_action2, "account22", "name22")
        register_action(mock_action3)
        # process the mock fake block 2
        process_block(200)

        # assertions
        assert mock_get_block.call_count == 1
        assert mock_start_block.call_count == 1
        assert mock_action1.call_count == 1
        assert mock_action2.call_count == 1
        assert mock_action3.call_count == 2
        assert mock_commit_block.call_count == 1

        # action_dict assertions
        from demux.demux import action_dict
        assert action_dict[('account21', 'name21')] == [mock_action1]
        assert action_dict[('account22', 'name22')] == [mock_action2]
        assert action_dict[(None, None)] == [mock_action3]
        print("action_dict=", action_dict)
        # action functions call order assertions
        m.assert_has_calls([call.mock_action3(fake_block2.get('transactions')[0]['trx']['transaction'].get('actions')[0], block=fake_block2, transaction=fake_block2.get('transactions')[0]),
                            call.mock_action1(fake_block2.get('transactions')[0]['trx']['transaction'].get('actions')[0], block=fake_block2, transaction=fake_block2.get('transactions')[0]),
                            call.mock_action3(fake_block2.get('transactions')[0]['trx']['transaction'].get('actions')[1], block=fake_block2, transaction=fake_block2.get('transactions')[0]),
                            call.mock_action2(fake_block2.get('transactions')[0]['trx']['transaction'].get('actions')[1], block=fake_block2, transaction=fake_block2.get('transactions')[0])])

    @patch.object(Client, 'get_block')
    @patch.object(Client, 'get_info')
    def test_multiblock_register_multiple_action_functions(self, mock_get_info_head_block, mock_get_block):
        """
        Tests that multiple action functions are registered and called correctly when processing multiple blocks
        """
        mock_get_info_head_block.return_value = {'head_block_num': 99999999999}
        mock_get_block.side_effect = [fake_block1, fake_block2]
        # mock callback functions
        mock_start_block = Mock()
        mock_action1 = Mock()
        mock_action2 = Mock()
        mock_action3 = Mock()
        mock_action4 = Mock()
        mock_commit_block = Mock()
        # parent mock for checking call order
        m = Mock()
        m.mock_action1, m.mock_action2, m.mock_action3, m.mock_action4 = mock_action1, mock_action2, mock_action3, mock_action4
        m.mock_calls
        # set up the action_dict
        initialise_action_dict()
        # register the mock callback functions
        register_start_commit(mock_start_block, mock_commit_block)
        register_action(mock_action1, "account11", "name11")
        register_action(mock_action2, "account21", "name21")
        register_action(mock_action3)
        register_action(mock_action4, "account22", "name22")
        # process the mock fake blocks 1 and 2
        process_blocks(100,102)

        # assertions
        assert mock_get_block.call_count == 2
        assert mock_get_block.call_args_list == [call(100), call(101)]
        assert mock_start_block.call_count == 2
        assert mock_action1.call_count == 1
        assert mock_action2.call_count == 1
        assert mock_action3.call_count == 3
        assert mock_action4.call_count == 1
        assert mock_commit_block.call_count == 2

        # action_dict assertions
        from demux.demux import action_dict
        assert action_dict[('account11', 'name11')] == [mock_action1]
        assert action_dict[('account21', 'name21')] == [mock_action2]
        assert action_dict[(None, None)] == [mock_action3]
        assert action_dict['account22', 'name22'] == [mock_action4]

        # action functions call order assertions (order is: action3-account11, action1-account11, action3-account21, action2-account21, action3-account22, action4-account22
        m.assert_has_calls([call.mock_action3(fake_block1.get('transactions')[0]['trx']['transaction'].get('actions')[0], block=fake_block1, transaction=fake_block1.get('transactions')[0]),
                            call.mock_action1(fake_block1.get('transactions')[0]['trx']['transaction'].get('actions')[0], block=fake_block1, transaction=fake_block1.get('transactions')[0]),
                            call.mock_action3(fake_block2.get('transactions')[0]['trx']['transaction'].get('actions')[0], block=fake_block2, transaction=fake_block2.get('transactions')[0]),
                            call.mock_action2(fake_block2.get('transactions')[0]['trx']['transaction'].get('actions')[0], block=fake_block2, transaction=fake_block2.get('transactions')[0]),
                            call.mock_action3(fake_block2.get('transactions')[0]['trx']['transaction'].get('actions')[1], block=fake_block2, transaction=fake_block2.get('transactions')[0]),
                            call.mock_action4(fake_block2.get('transactions')[0]['trx']['transaction'].get('actions')[1], block=fake_block2, transaction=fake_block2.get('transactions')[0])])
