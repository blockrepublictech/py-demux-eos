
# Block 1: transactions = 0, actions = 0
block_1 = {
  "previous": "0000000000000000000000000000000000000000000000000000000000000000",
  "transactions": [],
  "id": "00000001405147477ab2f5f51cda427b638191c66d2c59aa392d5c2c98076cb0",
  "block_num": 1,
}

# Block 9999: transactions = 14, actions = 14
block_9999 = {
  "previous": "0000270eae4a6fc021b47c17ae79e2ed6904bf4ade796f4cc7e4bf1f984fd3a6",
  "transactions": [
    {
      "trx": {
        "id": "aafc90a8d2669c0f4b7de86046322e7d1306a0fd22f559f7103c6db59fb1f6ed",
        "transaction": {
          "actions": [
            {
              "account": "eosio.unregd",
              "name": "add"
            },
            {
              "account": "eosio.unregd",
              "name": "add"
            },
            {
              "account": "eosio.unregd",
              "name": "add"
            },
            {
              "account": "eosio.unregd",
              "name": "add"
            }
          ]
        }
      }
    },
    {
      "trx": {
        "id": "cd04e391e314429a49cb6d4b3d861903df0a0faa7ce6ff354c4cffd70d7a9d53",
        "transaction": {
          "actions": [
            {
              "account": "eosio.unregd",
              "name": "add",
            },
            {
              "account": "eosio.unregd",
              "name": "add"
            },
            {
              "account": "eosio.unregd",
              "name": "add"
            },
            {
              "account": "eosio.unregd",
              "name": "add"
            },
            {
              "account": "eosio.unregd",
              "name": "add"
            },
            {
              "account": "eosio.unregd",
              "name": "add"
            },
            {
              "account": "eosio.unregd",
              "name": "add"
            }
          ]
        }
      }
    },
    {
      "trx": {
        "id": "4bef46d447ed1bf46c4a152ee404bee95d435074cf3cbdafc3adc6a3166c1602",
        "transaction": {
          "actions": [
            {
              "account": "eosio.unregd",
              "name": "add"
            },
            {
              "account": "eosio.unregd",
              "name": "add"
            },
            {
              "account": "eosio.unregd",
              "name": "add"
            }
          ]
        }
      }
    }
  ],
  "id": "0000270f03c8abd538ea5937391e139cffbc0eca6206d43753675ffc95088a61",
  "block_num": 9999
}

# Block 10000: transactions = 2, actions = 5
block_10000 = {
  "previous": "0000270f03c8abd538ea5937391e139cffbc0eca6206d43753675ffc95088a61",
  "transactions": [
    {
      "trx": {
        "id": "aafc90a8d2669c0f4b7de86046322e7d1306a0fd22f559f7103c6db59fb1f6ed",
        "transaction": {
          "actions": [
            {
              "account": "eosio.unregd",
              "name": "add"
            },
            {
              "account": "eosio.unregd",
              "name": "transfer"
            }
          ]
        }
      }
    },
    {
      "trx": {
        "id": "cd04e391e314429a49cb6d4b3d861903df0a0faa7ce6ff354c4cffd70d7a9d53",
        "transaction": {
          "actions": [
            {
              "account": "eosio.unregd",
              "name": "add",
            },
            {
              "account": "eosio.unregd",
              "name": "transfer"
            },
            {
              "account": "eosio.unregd",
              "name": "add"
            }
          ]
        }
      }
    }
  ],
  "id": "000027102a47393efa1d0575dbad538e95ca9b41b2678d74b16450f64155d78e",
  "block_num": 10000
}

# Fake block 1: only transaction data
# transactions = 1, actions = 1
fake_block1 = {
  "transactions": [
    {
      "trx": {
        "id": "aafc90a8d2669c0f4b7de86046322e7d1306a0fd22f559f7103c6db59fb1f6ed",
        "transaction": {
          "actions": [
            {
              "account": "account11",
              "name": "name11",
              "authorization": [
                {
                  "actor": "account11",
                  "permission": "active"
                }
              ],
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
  "block_num": 100
}

# Fake block 2: only transaction data
# transactions = 1, actions = 2
fake_block2 = {
  "transactions": [
    {
      "trx": {
        "id": "aafc90a8d2669c0f4b7de86046322e7d1306a0fd22f559f7103c6db59fb1f6ed",
        "transaction": {
          "actions": [
            {
              "account": "account21",
              "name": "name21",
              "authorization": [
                {
                  "actor": "account21",
                  "permission": "active"
                }
              ],
              "data": {
                "ethereum_address": "0xaf6a0d44c77c915c0f099bbd85236459093c00b7",
                "balance": "1.0000 EOS"
              }
            },
            {
              "account": "account22",
              "name": "name22",
              "authorization": [
                {
                  "actor": "account2",
                  "permission": "active"
                }
              ],
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
  "block_num": 200
}
