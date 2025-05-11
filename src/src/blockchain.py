import os
from web3 import Web3
from src.contract_compiler import get_abi, get_bytecode
from eth_account import Account

PRIVATE_KEY = "0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80"
ACCOUNT = Account.from_key(PRIVATE_KEY)
CONTRACT_ADDRESS_FILE = "data/contract_address.txt"
RPC_URL = "http://0.0.0.0:8545"

def deploy_contract(web3) -> str:
    abi = get_abi()
    bytecode = get_bytecode()

    contract = web3.eth.contract(abi=abi, bytecode=bytecode)
    nonce = web3.eth.get_transaction_count(ACCOUNT.address)

    txn = contract.constructor().build_transaction({
        'from': ACCOUNT.address,
        'nonce': nonce,
        'gas': 4000000,
        'gasPrice': web3.to_wei('50', 'gwei')
    })

    signed_txn = web3.eth.account.sign_transaction(txn, PRIVATE_KEY)
    tx_hash = web3.eth.send_raw_transaction(signed_txn.raw_transaction)
    receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

    contract_address = receipt.contractAddress
    os.makedirs("data", exist_ok=True)
    with open(CONTRACT_ADDRESS_FILE, "w") as f:
        f.write(contract_address)

    print(f"Kontrakt wdrożony pod adresem: {contract_address}")
    return contract_address

def load_contract(web3, auto_deploy=True):
    if not os.path.exists(CONTRACT_ADDRESS_FILE):
        if auto_deploy:
            print("Brak kontraktu – automatyczne wdrożenie...")
            contract_address = deploy_contract(web3)
        else:
            raise FileNotFoundError("Brak kontraktu i auto_deploy = False.")
    else:
        with open(CONTRACT_ADDRESS_FILE, "r") as f:
            contract_address = f.read().strip()
        print(f"Wczytano kontrakt: {contract_address}")

    abi = get_abi()
    return web3.eth.contract(address=contract_address, abi=abi)

def connect_web3():
    web3 = Web3(Web3.HTTPProvider(RPC_URL))
    if not web3.is_connected():
        raise ConnectionError("Brak połączenia z Ethereum")
    return web3

def load_contract(web3, auto_deploy=True):
    from src.contract_compiler import get_abi, get_bytecode

    if not os.path.exists(CONTRACT_ADDRESS_FILE):
        if auto_deploy:
            print("Brak kontraktu – automatyczne wdrożenie...")
            contract_address = deploy_contract(web3)
        else:
            raise FileNotFoundError("Brak kontraktu i auto_deploy = False.")
    else:
        with open(CONTRACT_ADDRESS_FILE, "r") as f:
            contract_address = f.read().strip()
        print(f"Wczytano kontrakt: {contract_address}")

    abi = get_abi()
    return web3.eth.contract(address=contract_address, abi=abi)



def send_transaction(web3, txn_dict):
    signed_txn = web3.eth.account.sign_transaction(txn_dict, PRIVATE_KEY)
    tx_hash = web3.eth.send_raw_transaction(signed_txn.raw_transaction)
    receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    return tx_hash.hex(), receipt['blockNumber'], receipt['status']

def get_account():
    return ACCOUNT
