from datetime import datetime
from src.utils import read_file_binary, generate_document_hash, hex_to_bytes32
from src.blockchain import get_account, send_transaction
from logging import getLogger
from web3.exceptions import ContractLogicError

logger = getLogger("DocChain")


# === ADD ===
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


# === VERIFY ===
def verify_document_ui(contract):
    try:
        path = input("Ścieżka do pliku do weryfikacji: ")
        content = read_file_binary(path)
        verify_document(contract, content)
    except Exception as e:
        logger.exception(f"Błąd w verify_document_ui(): {str(e)}")


def verify_document(contract, content) -> bool:
    try:
        doc_hash = generate_document_hash(content)
        bytes32_hash = hex_to_bytes32(doc_hash)

        verified, issuer, timestamp, name, doc_type = contract.functions.verifyDocument(bytes32_hash).call()
        dt = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

        logger.info(
            f"Weryfikacja: {verified}\nDokument: {name} ({doc_type})\nWystawca: {issuer}\nData: {dt}"
        )

        return verified  # ✅ ZWRACAMY WYNIK
    except ContractLogicError as e:
        logger.warning("Dokument nie istnieje w blockchainie.")
        return False
    except Exception as e:
        logger.exception(f"Błąd podczas weryfikacji dokumentu: {str(e)}")
        raise


# === UPDATE ===
def update_document_ui(contract, web3):
    try:
        path = input("Ścieżka do pliku: ")
        new_name = input("Nowa nazwa: ")
        new_type = input("Nowy typ: ")
        content = read_file_binary(path)
        update_document(contract, web3, content, new_name, new_type)
    except Exception as e:
        logger.exception(f"Błąd w update_document_ui(): {str(e)}")


def update_document(contract, web3, content, new_name, new_type):
    try:
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


# === DELETE ===
def delete_document_ui(contract, web3):
    try:
        path = input("Ścieżka do pliku do usunięcia: ")
        content = read_file_binary(path)
        delete_document(contract, web3, content)
    except Exception as e:
        logger.exception(f"Błąd w delete_document_ui(): {str(e)}")


def delete_document(contract, web3, content):
    try:
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