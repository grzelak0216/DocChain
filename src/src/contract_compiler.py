from solcx import compile_standard, install_solc, set_solc_version
import json
import os

CONTRACT_PATH = "contracts/DocumentVerifier.sol"
CONTRACT_NAME = "DocumentVerifier"

def compile_contract():
    install_solc("0.8.0")
    set_solc_version("0.8.0")

    with open(CONTRACT_PATH, 'r') as f:
        source_code = f.read()

    compiled = compile_standard({
        "language": "Solidity",
        "sources": {
            CONTRACT_PATH: {"content": source_code}
        },
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "evm.bytecode"]}
            }
        }
    })
    return compiled

def get_abi():
    compiled = compile_contract()
    return compiled['contracts'][CONTRACT_PATH][CONTRACT_NAME]['abi']

def get_bytecode():
    compiled = compile_contract()
    return compiled['contracts'][CONTRACT_PATH][CONTRACT_NAME]['evm']['bytecode']['object']
