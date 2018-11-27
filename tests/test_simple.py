# py-demux-eos - Deterministic event-sourced state and side effect handling for blockchain applications
# Copyright (C) 2018 BlockRepublic Pty Ltd
# Licenced under the Apache 2.0 Licence

import unittest
import pytest
from unittest.mock import Mock, patch
from demux import Demux
from tests.utils import fake_block1

# Basic tests for pydemux, run the process_block() functions and connect to the bp api node


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

        d = Demux(start_block_fn=start, commit_block_fn=commit)

        assert d._start_block_fn == start
#        assert action_fn == action
        assert d._commit_block_fn == commit

    @patch.object(Demux, 'get_a_block')
    @patch.object(Demux, 'get_info')
    def test_start_and_commit_callback_functions_called(self, mock_get_info_head_block, mock_get_block):
        """
        Ensure the start_block and commit_block functions are called when processing a block
        """
        mock_get_info_head_block.return_value = {'head_block_num': 99999999999}
        mock_get_block.return_value = fake_block1
        # mock callback functions
        mock_start_block = Mock()
        mock_action = Mock()
        mock_commit_block = Mock()

        d = Demux(start_block_fn=mock_start_block,
                  commit_block_fn=mock_commit_block)
        d.register_action(mock_action)
        d.process_block(9999)
        mock_start_block.assert_called_once()
        mock_action.assert_called()
        mock_commit_block.assert_called_once()


    @patch.object(Demux, 'get_a_block')
    @patch.object(Demux, 'get_info')
    def test_no_start_block_function(self, mock_get_info_head_block, mock_get_block):
        """
        When users do not want to use the start_block function
        """
        mock_get_info_head_block.return_value = {'head_block_num': 99999999999}
        mock_get_block.return_value = fake_block1
        # mock callback functions
        mock_start_block = Mock()
        mock_action = Mock()
        mock_commit_block = Mock()

        d = Demux(commit_block_fn=mock_commit_block)
        d.register_action(mock_action)
        d.process_block(9999)

        mock_start_block.assert_not_called()
        mock_action.assert_called()
        mock_commit_block.assert_called_once()

    @patch.object(Demux, 'get_a_block')
    @patch.object(Demux, 'get_info')
    def test_no_commit_block_function(self, mock_get_info_head_block, mock_get_block):
        """
        When users do not want to use the commit_block function
        """
        mock_get_info_head_block.return_value = {'head_block_num': 99999999999}
        mock_get_block.return_value = fake_block1
        # mock callback functions
        mock_start_block = Mock()
        mock_action = Mock()
        mock_commit_block = Mock()

        d = Demux(start_block_fn=mock_start_block)
        d.register_action(mock_action)
        d.process_block(9999)

        mock_start_block.assert_called_once()
        mock_action.assert_called()
        mock_commit_block.assert_not_called()

    @patch.object(Demux, 'get_a_block')
    @patch.object(Demux, 'get_info')
    def test_only_action_function(self, mock_get_info_head_block, mock_get_block):
        """
        When users only want to use the action function
        """
        mock_get_info_head_block.return_value = {'head_block_num': 99999999999}
        mock_get_block.return_value = fake_block1
        # mock callback functions
        mock_start_block = Mock()
        mock_action = Mock()
        mock_commit_block = Mock()

        d = Demux()
        d.register_action(mock_action)
        d.process_block(9999)

        mock_start_block.assert_not_called()
        mock_action.assert_called()
        mock_commit_block.assert_not_called()


    @patch.object(Demux, 'get_a_block')
    @patch.object(Demux, 'get_info')
    def test_multiple_block_processing_with_start_and_end_block(self,
            mock_get_info_head_block, mock_get_block):
        """
        Ensure we can process multiple blocks with a start and end block
        """
        mock_get_info_head_block.return_value = {'head_block_num': 99999999999}
        mock_get_block.return_value = fake_block1
        # set up the action_dict
        #initialise_action_dict()
        # mock callback functions
        mock_start_block = Mock()
        mock_action = Mock()
        mock_commit_block = Mock()

        d = Demux(start_block_fn=mock_start_block,
                  commit_block_fn=mock_commit_block)
        #register_start_commit(mock_start_block, mock_commit_block)
        d.register_action(mock_action)
        # process multiple blocks (in this case there are 9)
        d.process_blocks(9990,9999)

        # assert the callback functions were called for each block only
        assert mock_start_block.call_count == 9
        assert mock_commit_block.call_count == 9
        # NEED: assert that process_block was called for each block
        #assert mock_process_block.call_count == 9
