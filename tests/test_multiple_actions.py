# py-demux-eos - Deterministic event-sourced state and side effect handling for blockchain applications
# Copyright (C) 2018 BlockRepublic Pty Ltd
# Licenced under the Apache 2.0 Licence

import unittest
import pytest
from unittest.mock import Mock, patch, call
from demux import Demux
from tests.utils import block_1, fake_block1, fake_block2
from collections import defaultdict

# Tests for py-demux with multiple registered action functions

class TestActionsPyDemux(unittest.TestCase):

    @patch.object(Demux, '_get_block')
    @patch.object(Demux, '_get_info')
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
        # register the mock callback functions
        d = Demux(start_block_fn=mock_start_block,
                  commit_block_fn=mock_commit_block)
        d.register_action(mock_action1, "account21", "name21")
        d.register_action(mock_action2, "account22", "name22")
        d.register_action(mock_action3)
        # process the mock fake block 2
        d.process_block(200)
        # assertions
        assert mock_get_block.call_count == 1
        assert mock_start_block.call_count == 1
        assert mock_action1.call_count == 1
        assert mock_action2.call_count == 1
        assert mock_action3.call_count == 2
        assert mock_commit_block.call_count == 1
        # action_dict assertions
        assert d._action_dict[('account21', 'name21', 'updates')] == [mock_action1]
        assert d._action_dict[('account22', 'name22', 'updates')] == [mock_action2]
        assert d._action_dict[(None, None, 'updates')] == [mock_action3]
        # action functions call order assertions
        m.assert_has_calls([call.mock_action3(fake_block2.get('transactions')[0]['trx']['transaction'].get('actions')[0], block=fake_block2, transaction=fake_block2.get('transactions')[0]),
                            call.mock_action1(fake_block2.get('transactions')[0]['trx']['transaction'].get('actions')[0], block=fake_block2, transaction=fake_block2.get('transactions')[0]),
                            call.mock_action3(fake_block2.get('transactions')[0]['trx']['transaction'].get('actions')[1], block=fake_block2, transaction=fake_block2.get('transactions')[0]),
                            call.mock_action2(fake_block2.get('transactions')[0]['trx']['transaction'].get('actions')[1], block=fake_block2, transaction=fake_block2.get('transactions')[0])])

    @patch.object(Demux, '_get_block')
    @patch.object(Demux, '_get_info')
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
        # register the mock callback functions
        d = Demux(start_block_fn=mock_start_block,
                  commit_block_fn=mock_commit_block)
        d.register_action(mock_action1, "account11", "name11")
        d.register_action(mock_action2, "account21", "name21")
        d.register_action(mock_action3)
        d.register_action(mock_action4, "account22", "name22")
        # process the mock fake blocks 1 and 2
        d.process_blocks(100,102)
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
        assert d._action_dict[('account11', 'name11', 'updates')] == [mock_action1]
        assert d._action_dict[('account21', 'name21', 'updates')] == [mock_action2]
        assert d._action_dict[(None, None, 'updates')] == [mock_action3]
        assert d._action_dict[('account22', 'name22', 'updates')] == [mock_action4]
        # action functions call order assertions (order is: action3-account11, action1-account11, action3-account21, action2-account21, action3-account22, action4-account22
        m.assert_has_calls([call.mock_action3(fake_block1.get('transactions')[0]['trx']['transaction'].get('actions')[0], block=fake_block1, transaction=fake_block1.get('transactions')[0]),
                            call.mock_action1(fake_block1.get('transactions')[0]['trx']['transaction'].get('actions')[0], block=fake_block1, transaction=fake_block1.get('transactions')[0]),
                            call.mock_action3(fake_block2.get('transactions')[0]['trx']['transaction'].get('actions')[0], block=fake_block2, transaction=fake_block2.get('transactions')[0]),
                            call.mock_action2(fake_block2.get('transactions')[0]['trx']['transaction'].get('actions')[0], block=fake_block2, transaction=fake_block2.get('transactions')[0]),
                            call.mock_action3(fake_block2.get('transactions')[0]['trx']['transaction'].get('actions')[1], block=fake_block2, transaction=fake_block2.get('transactions')[0]),
                            call.mock_action4(fake_block2.get('transactions')[0]['trx']['transaction'].get('actions')[1], block=fake_block2, transaction=fake_block2.get('transactions')[0])])

    @patch.object(Demux, '_get_block')
    @patch.object(Demux, '_get_info')
    def test_update_effect_action_functions_stored_and_called_correctly(self, mock_get_info_head_block, mock_get_block):
        """
        Test that update and effect action functions are stored and called correctly for multiple blocks
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
        # register the mock callback functions
        d = Demux(start_block_fn=mock_start_block,
                  commit_block_fn=mock_commit_block)
        d.register_action(mock_action1, "account11", "name11", is_effect=True)
        d.register_action(mock_action2, "account21", "name21")
        d.register_action(mock_action3, is_effect=True)
        d.register_action(mock_action4, "account22", "name22", is_effect=True)
        # process the mock fake blocks 1 and 2
        # action_dict assertions that updates/effects stored correctly
        d.process_blocks(100,102, include_effects=True)
        assert d._action_dict[('account11', 'name11', 'effects')] == [mock_action1]
        assert d._action_dict[('account21', 'name21', 'updates')] == [mock_action2]
        assert d._action_dict[(None, None, 'effects')] == [mock_action3]
        assert d._action_dict[('account22', 'name22', 'effects')] == [mock_action4]
        # assertions that function calls correct
        assert mock_get_block.call_count == 2
        assert mock_get_block.call_args_list == [call(100), call(101)]
        assert mock_start_block.call_count == 2
        assert mock_action1.call_count == 1
        assert mock_action2.call_count == 0
        assert mock_action3.call_count == 3
        assert mock_action4.call_count == 1
        assert mock_commit_block.call_count == 2
