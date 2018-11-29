# py-demux-eos - Deterministic event-sourced state and side effect handling for blockchain applications
# Copyright (C) 2018 BlockRepublic Pty Ltd
# Licenced under the Apache 2.0 Licence

import unittest
from demux import Demux
from unittest.mock import patch, Mock
from demux.exceptions import UnknownBlockError
import pytest


class TestBlockchainAPI(unittest.TestCase):
    @patch('demux.requests.get')
    def test_info_calls_requests(self, mock_requests_get):
        d = Demux()
        d._get_info()
        # assertions
        mock_requests_get.assert_called_with('https://node2.eosphere.io/v1/chain/get_info')

    @patch('demux.requests.post')
    def test_get_a_block_calls_requests(self, mock_requests_post):
        mock_requests_post.return_value = Mock(status_code=200)
        d = Demux()
        d._get_block(555)
        # assertions
        mock_requests_post.assert_called_with('https://node2.eosphere.io/v1/chain/get_block',
            json={'block_num_or_id': 555})

    @patch('demux.requests.post')
    def test_invalid_post_raises_exception(self, mock_requests_post):
        mock_requests_post.return_value = Mock(status_code=500)
        d = Demux()
        with pytest.raises(UnknownBlockError):
            d._get_block(9999999999)
