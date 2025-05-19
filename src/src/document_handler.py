from datetime import datetime
from src.utils import read_file_binary, generate_document_hash, hex_to_bytes32
from src.blockchain import get_account, send_transaction
from logging import getLogger
from web3.exceptions import ContractLogicError

logger = getLogger("DocChain")


def add_document_ui(contract, web3):
    try:
        path = input("Ścieżka do pliku: ")
        name = input("Nazwa dokumentu: ")
        doc_type = input("Typ dokumentu: ")
        content = read_file_binary(path)
        add_document(contract, web3, content, name, doc_type)
    except Exception as e:
        logger.exception(f"Błąd w add_document_ui(): {str(e)}")


def add_document(contract, web3, content, name, doc_type):
    try:
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
        logger.info(f"Transakcja: {tx_hash} | Blok: {block} | Status: {'OK' if status == 1 else 'BŁĄD'}")

    except ContractLogicError as e:
        if "Document already exists" in str(e):
            logger.warning("Dokument już istnieje w blockchainie.")
        else:
            logger.exception(f"Błąd logiki kontraktu: {str(e)}")
        raise
    except Exception as e:
        logger.exception(f"Błąd podczas dodawania dokumentu: {str(e)}")
        raise


def verify_document_ui(contract):
    try:
        path = input("Ścieżka do pliku do weryfikacji: ")
        logger.info(f"Weryfikacja dokumentu: {path}")

        content = read_file_binary(path)
        doc_hash = generate_document_hash(content)
        bytes32_hash = hex_to_bytes32(doc_hash)

        verified, issuer, timestamp, name, doc_type = contract.functions.verifyDocument(bytes32_hash).call()
        dt = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

        logger.info(
            f"Weryfikacja: {verified}\nDokument: {name} ({doc_type})\nWystawca: {issuer}\nData: {dt}"
        )
    except ContractLogicError as e:
        logger.warning(f"Weryfikacja nie powiodła się (logika kontraktu): {str(e)}")
    except Exception as e:
        logger.exception(f"Błąd podczas weryfikacji dokumentu: {str(e)}")


def update_document_ui(contract, web3):
    try:
        path = input("Ścieżka do pliku: ")
        new_name = input("Nowa nazwa: ")
        new_type = input("Nowy typ: ")

        logger.info(f"Aktualizacja dokumentu: {path} → {new_name} ({new_type})")

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
        logger.info(f"Zaktualizowano: {tx_hash} | Blok: {block} | Status: {'OK' if status == 1 else 'BŁĄD'}")

    except ContractLogicError as e:
        logger.warning(f"Błąd logiki kontraktu podczas aktualizacji: {str(e)}")
    except Exception as e:
        logger.exception(f"Błąd podczas aktualizacji dokumentu: {str(e)}")


def delete_document_ui(contract, web3):
    try:
        path = input("Ścieżka do pliku do usunięcia: ")
        logger.info(f"Usuwanie dokumentu: {path}")

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
        logger.info(f"Usunięto: {tx_hash} | Blok: {block} | Status: {'OK' if status == 1 else 'BŁĄD'}")

    except ContractLogicError as e:
        logger.warning(f"Błąd logiki kontraktu podczas usuwania: {str(e)}")
    except Exception as e:
        logger.exception(f"Błąd podczas usuwania dokumentu: {str(e)}")
