VeChain for humans.

This library enables you to talk to VeChain blockchain without hassle.

It automatically estimate gas and decode events/revert reasons for you.

## Installation

```
pip3 install -U thor-requests
```

# Quick Start
```python
from thor_requests.connect import Connect

connector = Connect("http://testnet.veblocks.net")

# ... Now you can access VeChain
```

## API Reference

```python
from thor_requests import Connect, Wallet, Contract

# Wallet
wallet = Wallet.fromPrivate(priv=b'')
wallet = Wallet.fromMnemonic(words=[])
wallet = Wallet.fromKeyStore(ks=dict, password='')

# Contract
contract = Contract(meta_dict=dict)
contract = Contract.fromFile(meta_file_path='')

# Connect
connector = Connect(node_url='')
connector.get_chainTag()
connector.get_account(address='')
connector.get_block(block_id='')
connector.get_tx(tx_id='')
connector.get_tx_receipt(tx_id='')
connector.wait_for_tx_receipt(tx_id='', time_out=20)
connector.replay_tx(tx_id='')

# Deploy a smart contract
connector.deploy(wallet, contract)

# Call a contract function (won't spend gas)
connector.call(caller, contract, func_name, func_params, to, value=0, gas=None)

# Execute a contract fucntion (spend real gas)
connector.commit(wallet, contract, func_name, func_params, to, value=0, gas=None)

# Multi clauses support (MTT)
clause1 = connector.clause(contract, func_name, func_params, to, value=0)
clause2 = connector.clause(contract, func_name, func_params, to, value=0)

# Call them (won't spend gas)
connector.call_multi(caller, clauses=[clause1, clause2])
# Or execute them
connector.commit_multi(wallet, clauses=[clause1, clause2])
```

# Examples (Blockchain)
## Get Tx/Block/Account/Receipt
```python
from thor_requests.connect import Connect

connector = Connect("http://testnet.veblocks.net")

# Account
connector.get_account('0x7567d83b7b8d80addcb281a71d54fc7b3364ffed')

# >>> {'balance': '0x21671d16fd19254d67', 'energy': '0xf809f75231563b5f1d', 'hasCode': False}

# Block
connector.get_block('0x0084f21562e046b1ae9aa70b6cd3b7bc2e8312f3961716ee3fcd58ce8bcb7392')

# >>> {'number': 8712725, 'id': '0x0084f21562e046b1ae9aa70b6cd3b7bc2e8312f3961716ee3fcd58ce8bcb7392', 'size': 243, 'parentID': '0x0084f214dd0b96059a142b5ac33668a3bb56245bde62d72a7874dc5a842c89e7', 'timestamp': 1617158500, 'gasLimit': 281323205, 'beneficiary': '0xb4094c25f86d628fdd571afc4077f0d0196afb48', 'gasUsed': 0, 'totalScore': 33966653, 'txsRoot': '0x45b0cfc220ceec5b7c1c62c4d4193d38e4eba48e8815729ce75f9c0ab0e4c1c0', 'txsFeatures': 1, 'stateRoot': '0xfe32d569f127a9a1d6f690bb83dae1c91fee31cac6596ae573ad3fa76c209670', 'receiptsRoot': '0x45b0cfc220ceec5b7c1c62c4d4193d38e4eba48e8815729ce75f9c0ab0e4c1c0', 'signer': '0x39218d415dc252a50823a3f5600226823ba4716e', 'isTrunk': True, 'transactions': []}

# Transaction
connector.get_tx("0xda2ce6bddfb3bd32541c999e81ef56019a6314a23c90a466896aeefca33aebc1")

# >>> {'id': '0xda2ce6bddfb3bd32541c999e81ef56019a6314a23c90a466896aeefca33aebc1', 'chainTag': 39, 'blockRef': '0x00825266c5688208', 'expiration': 18, 'clauses': [{'to': '0x0000000000000000000000000000456e65726779', 'value': '0x0', 'data': '0xa9059cbb0000000000000000000000007567d83b7b8d80addcb281a71d54fc7b3364ffed0000000000000000000000000000000000000000000000056bc75e2d63100000'}], 'gasPriceCoef': 0, 'gas': 51582, 'origin': '0xfa6e63168115a9202dcd834f6c20eabf48f18ba7', 'delegator': None, 'nonce': '0x32c31a501fcd9752', 'dependsOn': None, 'size': 190, 'meta': {'blockID': '0x0082526895631e850b6cae1ba0a05deb24b8719b6896b69437cea87ee939bf3d', 'blockNumber': 8540776, 'blockTimestamp': 1615439010}}

# Transaction receipt
connector.get_tx_receipt('0xda2ce6bddfb3bd32541c999e81ef56019a6314a23c90a466896aeefca33aebc1')

# >>> {'gasUsed': 36582, 'gasPayer': '0xfa6e63168115a9202dcd834f6c20eabf48f18ba7', 'paid': '0x1fbad5f2e25570000', 'reward': '0x984d9c8dd8008000', 'reverted': False, 'meta': {'blockID': '0x0082526895631e850b6cae1ba0a05deb24b8719b6896b69437cea87ee939bf3d', 'blockNumber': 8540776, 'blockTimestamp': 1615439010, 'txID': '0xda2ce6bddfb3bd32541c999e81ef56019a6314a23c90a466896aeefca33aebc1', 'txOrigin': '0xfa6e63168115a9202dcd834f6c20eabf48f18ba7'}, 'outputs': [{'contractAddress': None, 'events': [{'address': '0x0000000000000000000000000000456e65726779', 'topics': ['0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef', '0x000000000000000000000000fa6e63168115a9202dcd834f6c20eabf48f18ba7', '0x0000000000000000000000007567d83b7b8d80addcb281a71d54fc7b3364ffed'], 'data': '0x0000000000000000000000000000000000000000000000056bc75e2d63100000'}], 'transfers': []}]}

# Chain Tag
connector.get_chainTag()
# >>> 39
```
## Debug a Failed Transaction

This operation will yield pretty revert reason if any.

```python
from thor_requests.connect import Connect

connector = Connect("http://testnet.veblocks.net")
connector.replay_tx("0x1d05a502db56ba46ccd258a5696b9b78cd83de6d0d67f22b297f37e710a72bb5")

# Notice: Revert Reason is decoded for you.

# [{
#     'data': '0x08c379a00000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000000000000000001c7472616e7366657220746f20746865207a65726f206164647265737300000000',
#     'events': [],
#     'transfers': [],
#     'gasUsed': 659,
#     'reverted': True,
#     'vmError': 'evm: execution reverted',
#     'decoded': {
#         'revertReason': 'transfer to the zero address'
#     }
# }]
```
# Examples (Smart Contract)

## Deploy a Smart Contract

```python
from thor_requests.connect import Connect
from thor_requests.wallet import Wallet
from thor_requests.contract import Contract

connector = Connect("http://testnet.veblocks.net")

# wallet address: 0x7567d83b7b8d80addcb281a71d54fc7b3364ffed
_wallet = Wallet.fromPrivateKey(bytes.fromhex("dce1443bd2ef0c2631adc1c67e5c93f13dc23a41c18b536effbbdcbcdb96fb65")) 

_contract = Contract.fromFile("/path/to/solc/compiled/WETH9.json")

res = connector.deploy(_wallet, _contract)
print(res)
# >>> {'id': '0xa670ae6fc053f3e63e9a944947d1e2eb9f53dc613fd305552ee00af987a6d140'}
```

## Call a Function (won't spend gas, emulate only)

```python
from thor_requests.connect import Connect
from thor_requests.contract import Contract

connector = Connect("http://testnet.veblocks.net")

_contract_addr = '0x535b9a56c2f03a3658fc8787c44087574eb381fd'
_contract = Contract.fromFile("/path/to/solc/compiled/WETH9.json")

# Emulate the "balanceOf()" function
res = connector.call(
    caller='',
    contract=_contract,
    func_name="balanceOf",
    func_params=['0x7567d83b7b8d80addcb281a71d54fc7b3364ffed'],
    to=_contract_addr,
)
print(res)

# Notice: The return value is decoded for you.

# {
#     'data': '0x0000000000000000000000000000000000000000000000006124fee993bc0004',
#     'events': [],
#     'transfers': [],
#     'gasUsed': 557,
#     'reverted': False,
#     'vmError': '',
#     'decoded': {
#         '0': 7000000000000000004
#     }
# }

# Emulate the "deposit()" function
res = connector.call(
    caller='0x7567d83b7b8d80addcb281a71d54fc7b3364ffed',
    contract=_contract,
    func_name="deposit",
    func_params=[],
    to=_contract_addr,
    value=4
)
print(res)

# Notice the Event is decoded for you.

# {
#     'data': '0x',
#     'events': [{
#         'address': '0x535b9a56c2f03a3658fc8787c44087574eb381fd',
#         'topics': ['0xe1fffcc4923d04b559f4d29a8bfc6cda04eb5b0d3c460751c2402c5c5cc9109c', '0x0000000000000000000000007567d83b7b8d80addcb281a71d54fc7b3364ffed'],
#         'data': '0x0000000000000000000000000000000000000000000000000000000000000004',
#         'decoded': {
#             '0': '0x7567d83b7b8d80addcb281a71d54fc7b3364ffed',
#             'dst': '0x7567d83b7b8d80addcb281a71d54fc7b3364ffed',
#             '1': 4,
#             'wad': 4
#         },
#         'name': 'Deposit'
#     }],
#     'transfers': [{
#         'sender': '0x7567d83b7b8d80addcb281a71d54fc7b3364ffed',
#         'recipient': '0x535b9a56c2f03a3658fc8787c44087574eb381fd',
#         'amount': '0x4'
#     }],
#     'gasUsed': 6902,
#     'reverted': False,
#     'vmError': ''
# }
```

## Execute a Function (spend real gas)

```python
from thor_requests.connect import Connect
from thor_requests.wallet import Wallet
from thor_requests.contract import Contract

connector = Connect("http://testnet.veblocks.net")

# wallet address: 0x7567d83b7b8d80addcb281a71d54fc7b3364ffed
_wallet = Wallet.fromPrivateKey(bytes.fromhex("dce1443bd2ef0c2631adc1c67e5c93f13dc23a41c18b536effbbdcbcdb96fb65")) 
_contract_addr = '0x535b9a56c2f03a3658fc8787c44087574eb381fd'
_contract = Contract.fromFile("/path/to/solc/compiled/WETH9.json")

# Execute the "deposit()" function. (will pay gas)
# Send along 5 VET with the tx
res = connector.commit(_wallet, _contract, "deposit", [], to=_contract_addr, value=5 * (10 ** 18))
print(res)

# >>> {'id': '0x51222328b7395860cb9cc6d69d822cf31056851b5694eeccc9f243021eecd547'}
```
