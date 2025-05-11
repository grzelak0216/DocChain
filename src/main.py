import os
from src.blockchain import connect_web3, load_contract, deploy_contract
from src.document_handler import (
    add_document_ui,
    verify_document_ui,
    update_document_ui,
    delete_document_ui
)
from src.blockchain_verify import blockchain_verify_main

def main():
    web3 = connect_web3()

    contract = None
    if not os.path.exists("data/contract_address.txt"):
        print("⚠️ Kontrakt jeszcze nie wdrożony.")
    else:
        contract = load_contract(web3)

    while True:
        print("\n== MENU ==")
        print("1. Dodaj dokument")
        print("2. Zweryfikuj dokument")
        print("3. Zaktualizuj dokument")
        print("4. Usuń dokument")
        print("5. Wdróż kontrakt")
        print("6. Weryfikacja transakcji")
        print("7. Wyjście")
        choice = input("Wybierz opcję: ")

        if choice == "1":
            if contract:
                add_document_ui(contract, web3)
            else:
                print("⚠️ Najpierw wdroż kontrakt (opcją 5).")
        elif choice == "2":
            if contract:
                verify_document_ui(contract)
            else:
                print("⚠️ Najpierw wdroż kontrakt (opcją 5).")
        elif choice == "3":
            if contract:
                update_document_ui(contract, web3)
            else:
                print("⚠️ Najpierw wdroż kontrakt (opcją 5).")
        elif choice == "4":
            if contract:
                delete_document_ui(contract, web3)
            else:
                print("⚠️ Najpierw wdroż kontrakt (opcją 5).")
        elif choice == "5":
            contract_address = deploy_contract(web3)
            contract = load_contract(web3, auto_deploy=False)
        elif choice == "6":
            blockchain_verify_main(web3)
        elif choice == "7":
            break
        else:
            print("Nieprawidłowy wybór.")


if __name__ == "__main__":
    main()

