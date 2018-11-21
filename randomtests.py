
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
    register_start_commit(mock_start_block, mock_commit_block)
    register_action(mock_action)
    # process the mock blocks 9999
    with pytest.raises(StopIteration) as excinfo:
        process_blocks(9999998, irreversible_only=True)
     # assertions
    assert mock_get_block.call_count == 2
    assert mock_get_block.call_args_list == [call(9999998), call(9999999)]
    assert mock_start_block.call_count == 2
    assert mock_action.call_count == 132
    assert mock_commit_block.call_count == 2
    assert mock_sleep.call_count == 1


@patch.object(Client, 'get_block')
@patch.object(Client, 'get_info')
def test_rollback_function_called(self, mock_get_info_irr_block, mock_get_block):
    """
    Tests that rollback function is successfully called when rollback has occurred
    """
    mock_get_info_irr_block.return_value = {'last_irreversible_block_num': 999999}
    # get block iterates through blocks each time it is called
    mock_get_block.side_effect = [block_9999998, block_9999999]

    mock_start_block = Mock()
    mock_action = Mock()
    mock_commit_block = Mock()

    # register the mock callback functions
    register_start_commit(mock_start_block, mock_commit_block)
    register_action(mock_action)
    # process the mock blocks 9999 in an infinite loop
    process_blocks(9999998, irreversible_only=True)

    # assertions
    assert mock_get_block.call_count == 2
    assert mock_get_block.call_args_list == [call(9999998), call(9999999)]
    assert mock_start_block.call_count == 2
    assert mock_action.call_count == 132
    assert mock_commit_block.call_count == 2

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
    # set up the action_dict
    initialise_action_dict()
    initialise_block_id_dict()
    # register the mock callback functions
    register_start_commit(mock_start_block, mock_commit_block)
    register_action(mock_action)
    # process the mock blocks 9999
    with pytest.raises(StopIteration) as excinfo:
        from demux.demux import block_id_dict
        print("block_id_dict=", block_id_dict)
        process_blocks(9999998)
     # assertions
    assert mock_get_block.call_count == 2
    assert mock_get_block.call_args_list == [call(9999998), call(9999999)]
    assert mock_start_block.call_count == 2
    assert mock_action.call_count == 132
    assert mock_commit_block.call_count == 2
    assert mock_sleep.call_count == 1
    # PREVIOUS SUGGESTION
    #instead call get_info all the time, and go to sleep if it is at the head  (100ms)
    # test that the infinite loop works -->
        #mock get_block and get_info, and sleep() and test that things are called in the right way
        #do the mocking so you raise a side_effect (exception), catch the exception and test all the test conditions worked
        # test if i get a block, if start from block < head : it will keep calling get_block for every block
        # if it matches the head --> it will call sleep
        # get out of infinite loop by using side effect from a mock to get an exception (this exits the function), assert it is raised
        # check that all the mocks were called correctly
