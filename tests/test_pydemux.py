import unittest
import pytest
from mock import Mock, patch
from eosapi import Client
from demux.demux import register, process_block, process_blocks, get_head_block

# Robust tests for pydemux

class TestPyDemux(unittest.TestCase):
    #test_register call back functions
    #1. setup test with register() and make fake functions to give to it
    #2. setup a block and assert that something was called
    #def setUp():

    def test_manual_block_with_no_transactions(self):
        """
        Ensure we can get a block with no transactions
        """
        c = Client(nodes=['https://node2.eosphere.io'])
        block = c.get_block(1)
        assert block.get("transactions") == []

    #Patch should be used like: @patch('package.module.ClassName')
    @patch('demux.demux.process_block')
    def test_mock_block_processing(self, mock_process_block):
        """
        Tests block processing on a mocked block
        """
        # mock callback functions
        mock_start_block = Mock()
        mock_action = Mock()
        mock_commit_block = Mock()

        # register the mock callback functions
        register(mock_action, mock_start_block, mock_commit_block)
        # process the mock blocks 1 and 5
        process_block(1)

#    @patch('get_block')
#    def test_mock_single_block_processing(self, mock_block):
#        # mock callback functions
#        #        mock_start_block = Mock()
#        #        mock_action = Mock()
#        #        mock_commit_block = Mock()
#
#        register(mock_action, mock_start_block, mock_commit_block)
#
#        mock_block.return_value =
