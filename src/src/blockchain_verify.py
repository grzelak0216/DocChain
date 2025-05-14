import time
import sqlite3
from logging import getLogger

logger = getLogger("DocChain")
conn = sqlite3.connect("logi/blockchain_logs.db")
cursor = conn.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS transactions (
    tx_hash TEXT PRIMARY KEY,
    sender TEXT,
    recipient TEXT,
    gas_used INTEGER,
    status TEXT,
    timestamp INTEGER,
    block_number INTEGER
)""")
conn.commit()

def save_transaction(web3, tx_hash):
    try:
        tx = web3.eth.get_transaction(tx_hash)
        receipt = web3.eth.get_transaction_receipt(tx_hash)
        block = web3.eth.get_block(receipt['blockNumber'])

        status = "SUKCES" if receipt['status'] == 1 else "BŁĄD"

        cursor.execute("INSERT OR IGNORE INTO transactions VALUES (?, ?, ?, ?, ?, ?, ?)", (
            tx_hash,
            tx['from'],
            tx['to'],
            receipt['gasUsed'],
            status,
            block['timestamp'],
            receipt['blockNumber']
        ))
        conn.commit()

        logger.info(f"Zapisano transakcję {tx_hash[:10]}... | Status: {status}")

    except Exception as e:
        logger.info(f"Błąd zapisu transakcji {tx_hash}: {e}")

def get_transaction_data(web3, tx_hash):
    try:
        tx = web3.eth.get_transaction(tx_hash)
        receipt = web3.eth.get_transaction_receipt(tx_hash)
        block = web3.eth.get_block(receipt['blockNumber'])

        logger.info(f"""
        Transakcja:
        Od: {tx['from']}
        Do (kontrakt): {tx['to']}
        Gas: {tx['gas']}
        Nonce: {tx['nonce']}

        Odbiór transakcji:
        Status: {"SUKCES" if receipt['status'] == 1 else "BŁĄD"}
        Gas zużyty: {receipt['gasUsed']}
        Logi: {receipt['logs']}

        Blok:
        Numer bloku: {receipt['blockNumber']}
        Timestamp: {block['timestamp']}
        Liczba transakcji w bloku: {len(block['transactions'])}
        """)
    except Exception as e:
        logger.info(f"Error fetching transaction data: {e}")
        return None
    
def get_transaction_status(web3, tx_hash):
    try:
        receipt = web3.eth.get_transaction_receipt(tx_hash)
        if receipt is None:
            logger.info("Transakcja w toku\n")
        elif receipt['status'] == 1:
            logger.info("SUKCES\n")
        else:
            logger.info("BŁĄD\n")
    except Exception as e:
        logger.info(f"Error fetching transaction status: {e}")
        return None
    
def stream_blocks(web3):
    logger.info("Monitoring nowych bloków Hardhat...")
    latest = web3.eth.block_number

    while True:
        current = web3.eth.block_number
        if current > latest:
            for block_number in range(latest + 1, current + 1):
                block = web3.eth.get_block(block_number, full_transactions=True)
                logger.info(f"\n Nowy blok: {block_number} ({len(block['transactions'])} transakcji)")
                for tx in block['transactions']:
                    save_transaction(tx['hash'].hex())
            latest = current
        time.sleep(1)
    
def blockchain_verify_main(web3):
    logger.info("\n== WERYFIKACJA TRANSAKCJI ==")
    logger.info("Podaj hash transakcji, aby uzyskać szczegóły.")

    tx_hash = input("Hash transakcji: ")
    if not tx_hash.startswith("0x"):
        logger.info("Nieprawidłowy hash transakcji.")
        return

    while True:
        logger.info("\n== MENU ==")
        logger.info("1. Szczegóły transakcji")
        logger.info("2. Status transakcji")
        logger.info("3. Monitorowanie nowych bloków")
        logger.info("4. Nowy hash transakcji")
        logger.info("5. Powrót do menu głównego")
        choice = input("Wybierz opcję: ")

        if choice == "1":
            get_transaction_data(web3, tx_hash)
        elif choice == "2":
            get_transaction_status(web3, tx_hash)
        elif choice == "3":
            stream_blocks(web3)
        elif choice == "4":
            tx_hash = input("Hash transakcji: ")
        elif choice == "5":
            logger.info("Powrót do menu głównego...")
            break
        else:
            logger.info("Nieprawidłowy wybór.")