from datetime import datetime
from src.utils import read_file_binary, generate_document_hash, hex_to_bytes32
from src.blockchain import get_account, send_transaction

def add_document_ui(contract, web3):
    path = input("Ścieżka do pliku: ")
    name = input("Nazwa dokumentu: ")
    doc_type = input("Typ dokumentu: ")
    content = read_file_binary(path)
    add_document(contract, web3, content, name, doc_type)

def add_document(contract, web3, content, name, doc_type):
    doc_hash = generate_document_hash(content)
    bytes32_hash = hex_to_bytes32(doc_hash)
    nonce = web3.eth.get_transaction_count(get_account().address)
    txn = contract.functions.addDocument(bytes32_hash, name, doc_type).build_transaction({
        'from': get_account().address,
        'nonce': nonce,
        'gas': 2000000,
        'gasPrice': web3.to_wei('50', 'gwei')
    })
    tx_hash, block, status = send_transaction(web3, txn)
    print("Transakcja:", tx_hash, "| Blok:", block, "| Status:", "OK" if status == 1 else "BŁĄD")

def verify_document_ui(contract):
    path = input("Ścieżka do pliku do weryfikacji: ")
    content = read_file_binary(path)
    doc_hash = generate_document_hash(content)
    bytes32_hash = hex_to_bytes32(doc_hash)
    try:
        verified, issuer, timestamp, name, doc_type = contract.functions.verifyDocument(bytes32_hash).call()
        dt = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
        print(f"Weryfikacja: {verified}\nDokument: {name} ({doc_type})\nWystawca: {issuer}\nData: {dt}")
    except Exception as e:
        print("Błąd:", str(e))

def update_document_ui(contract, web3):
    path = input("Ścieżka do pliku: ")
    new_name = input("Nowa nazwa: ")
    new_type = input("Nowy typ: ")
    content = read_file_binary(path)
    doc_hash = generate_document_hash(content)
    bytes32_hash = hex_to_bytes32(doc_hash)
    nonce = web3.eth.get_transaction_count(get_account().address)
    txn = contract.functions.updateDocument(bytes32_hash, new_name, new_type).build_transaction({
        'from': get_account().address,
        'nonce': nonce,
        'gas': 2000000,
        'gasPrice': web3.to_wei('50', 'gwei')
    })
    tx_hash, block, status = send_transaction(web3, txn)
    print("Zaktualizowano:", tx_hash, "| Blok:", block, "| Status:", "OK" if status == 1 else "BŁĄD")

def delete_document_ui(contract, web3):
    path = input("Ścieżka do pliku do usunięcia: ")
    content = read_file_binary(path)
    doc_hash = generate_document_hash(content)
    bytes32_hash = hex_to_bytes32(doc_hash)
    
    nonce = web3.eth.get_transaction_count(get_account().address)
    txn = contract.functions.deleteDocument(bytes32_hash).build_transaction({
        'from': get_account().address,
        'nonce': nonce,
        'gas': 2000000,
        'gasPrice': web3.to_wei('50', 'gwei')
    })
    
    tx_hash, block, status = send_transaction(web3, txn)
    print("Usunięto:", tx_hash, "| Blok:", block, "| Status:", "OK" if status == 1 else "BŁĄD")

