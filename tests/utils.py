
# Block 1: transactions = 0, actions = 0
block_1 = {
  "previous": "0000000000000000000000000000000000000000000000000000000000000000",
  "transactions": [],
  "id": "00000001405147477ab2f5f51cda427b638191c66d2c59aa392d5c2c98076cb0",
  "block_num": 1,
}

# Fake block 1: only transaction data
# transactions = 1, actions = 1
fake_block1 = {
  "previous": "0000270f03c8abd538ea5937391e139cffbc0eca6206d43753675ffc95088a61",
  "transactions": [
    {
      "trx": {
        "id": "aafc90a8d2669c0f4b7de86046322e7d1306a0fd22f559f7103c6db59fb1f6ed",
        "transaction": {
          "actions": [
            {
              "account": "account11",
              "name": "name11",
              "data": {
                "ethereum_address": "0xaf6a0d44c77c915c0f099bbd85236459093c00b7",
                "balance": "1.0000 EOS"
              }
            }
          ]
        }
      }
    }
  ],
  "id": "fakebloke1id",
  "block_num": 100
}

# Fake block 2: only transaction data
# transactions = 1, actions = 2
fake_block2 = {
  "previous": "fakebloke1id",
  "transactions": [
    {
      "trx": {
        "id": "aafc90a8d2669c0f4b7de86046322e7d1306a0fd22f559f7103c6db59fb1f6ed",
        "transaction": {
          "actions": [
            {
              "account": "account21",
              "name": "name21",
              "data": {
                "ethereum_address": "0xaf6a0d44c77c915c0f099bbd85236459093c00b7",
                "balance": "1.0000 EOS"
              }
            },
            {
              "account": "account22",
              "name": "name22",
              "data": {
                "ethereum_address": "0xaf6a0d44c77c915c0f099bbd85236459093c00b7",
                "balance": "2.0000 EOS"
              }
            }
          ]
        }
      }
    }
  ],
  "id": "fakebloke2id",
  "block_num": 101
}
