# Document Verifier (Blockchain)

System do dodawania i weryfikacji dokumentów na blockchainie Ethereum.

## Uruchomienie

1. Stwórz wirtualne środowisko i zainstaluj wymagania:

   ```
   cd //document_verifier_project//
   python -m venv venv

   source venv/bin/activate    # Linux/macOS
   venv\Scripts\activate       # Windows

   pip install -r requirements.txt
   ```

2. Uruchom główny plik:

   ```
   python main.py
   ```

3. Upewnij się, że masz wdrożony smart kontrakt i jego adres zapisany w `data/contract_address.txt`.

## Struktura

- `main.py` – uruchamianie aplikacji.
- `src/` – kod źródłowy.
- `contracts/` – smart kontrakt.
- `data/` – dane, adres kontraktu, pliki.

## Wymagania

- Web3
- Py-Solc-X
