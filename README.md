# 📄 Document Verifier – Ethereum Blockchain

System do **dodawania, przechowywania i weryfikacji dokumentów na blockchainie Ethereum** z wykorzystaniem lokalnej sieci Hardhat oraz narzędzi do monitorowania (Grafana + Prometheus).

---

## 🔧 Wymagania

- Python 3.10+
- Docker + Docker Compose
- Node.js (jeśli nie używasz Dockera do uruchamiania Hardhat)
- Ganache/Hardhat (w tym projekcie: Hardhat + Docker)
- Web3.py
- py-solc-x

---

## 📁 Struktura projektu

```

document\_verifier/
├── contracts/             # Smart kontrakt Solidity
├── data/                  # Adres kontraktu, hash dokumentów
├── src/                   # Logika aplikacji i integracje z Web3
├── main.py                # Uruchomienie aplikacji w trybie CLI
├── requirements.txt
├── Dockerfile             # Obraz dla sieci Hardhat
├── docker-compose.yml     # Wszystkie serwisy (Hardhat, Prometheus, Grafana, Exporter)
└── prometheus.yml         # Konfiguracja Prometheusa

```

---

## 🚀 Uruchamianie systemu

### ✅ 1. Uruchom lokalną sieć Ethereum + monitoring (Docker)

W katalogu projektu:

```bash
docker compose up --build
```

To uruchamia:

- `hardhat` – lokalna sieć Ethereum (port 8545)
- `exporter` – eksportuje metryki z RPC
- `prometheus` – zbiera dane
- `grafana` – dashboard monitorujący (port 3000)

🧠 _Hardhat uruchamia 20 kont z 10 000 ETH każde do testowania._

---

### ✅ 2. Skonfiguruj środowisko Pythona

```bash
cd document_verifier
python -m venv venv

source venv/bin/activate        # Linux/macOS
venv\Scripts\activate           # Windows

pip install -r requirements.txt
```

---

### ✅ 3. Uruchom aplikację

Upewnij się, że:

- Smart kontrakt jest wdrożony (np. przez Hardhat CLI),
- Adres kontraktu znajduje się w `data/contract_address.txt`.

Następnie uruchom:

```bash
python main.py
```

Aplikacja pozwoli Ci:

- dodać hash dokumentu do blockchaina,
- sprawdzić czy hash istnieje (czy dokument był wcześniej zapisany),
- podejrzeć szczegóły transakcji.

---

## 📊 Monitoring

### 🔹 Prometheus UI

🟢 [http://localhost:9091](http://localhost:9091)
Służy do testowania zapytań i weryfikacji metryk

### 🔹 Grafana UI

🟢 [http://localhost:3000](http://localhost:3000)
Login: `admin` / Hasło: `admin`
Możesz dodać źródło danych `Prometheus` (URL: `http://prometheus:9090`)
Następnie zaimportuj dashboard ID `11888` (Ethereum Overview) lub stwórz własny np. z:

- `eth_exe_block_head_transactions_in_block`
- `eth_exe_gas_price_gwei`
- `eth_exe_sync_current_block`

---

## 🛠️ Narzędzia i obrazy

- Hardhat Node: `node:18 + hardhat`
- Prometheus: `prom/prometheus:latest`
- Grafana: `grafana/grafana:latest`
- Ethereum Exporter: `samcm/ethereum-metrics-exporter:latest`

---

## 📎 Przykładowe zapytania Prometheus

| Co monitoruje              | Zapytanie Prometheus                       |
| -------------------------- | ------------------------------------------ |
| Aktualna liczba transakcji | `eth_exe_block_head_transactions_in_block` |
| Aktualna cena gasu         | `eth_exe_gas_price_gwei`                   |
| Numer ostatniego bloku     | `eth_exe_sync_current_block`               |
| Wykorzystanie gasu w bloku | `eth_exe_block_head_gas_used`              |

---
