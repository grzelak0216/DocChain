import webbrowser
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit,
    QLabel, QRadioButton, QButtonGroup, QFrame, QSizePolicy, QMessageBox
)
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import Qt
from src.blockchain_verify import (
    get_transaction_data,
    get_transaction_status,
    stream_blocks
)

class TransactionDialog(QDialog):
    def __init__(self, web3):
        super().__init__()
        self.web3 = web3
        self.setWindowTitle("Weryfikacja Transakcji")
        self.setMinimumSize(500, 350)

        self.setStyleSheet("""
            QDialog {
                background-color: #1e1e1e;
                color: white;
            }
            QLineEdit {
                background-color: #2f3640;
                color: white;
                border: 2px solid #00cec9;
                border-radius: 6px;
                padding: 8px;
                font-size: 14px;
            }
            QLabel {
                color: #dfe6e9;
                font-size: 13px;
            }
            QRadioButton {
                font-size: 14px;
                padding: 5px;
            }
            QRadioButton::indicator {
                width: 16px;
                height: 16px;
            }
            QPushButton {
                background-color: #00b894;
                color: white;
                font-weight: bold;
                border: none;
                padding: 10px 16px;
                border-radius: 6px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #019875;
            }
        """)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(15)

        # 🔹 Górne przyciski Docker
        docker_layout = QHBoxLayout()
        docker_btn_1 = QPushButton("Prometheus UI")
        docker_btn_1.clicked.connect(lambda: self.open_url("http://localhost:9091"))
        docker_btn_2 = QPushButton("Grafana")
        docker_btn_2.clicked.connect(lambda: self.open_url("http://localhost:3000"))
        docker_layout.addWidget(docker_btn_1)
        docker_layout.addWidget(docker_btn_2)
        main_layout.addLayout(docker_layout)

        # 🔹 Hash transakcji
        self.tx_hash_input = QLineEdit()
        self.tx_hash_input.setPlaceholderText("Wprowadź hash transakcji (0x...)")
        main_layout.addWidget(QLabel("Hash transakcji:"))
        main_layout.addWidget(self.tx_hash_input)

        # 🔹 Wybór akcji
        main_layout.addWidget(QLabel("Wybierz akcję:"))
        self.action_group = QButtonGroup(self)
        self.radio_details = QRadioButton("Szczegóły transakcji")
        self.radio_status = QRadioButton("Status transakcji")
        self.radio_monitor = QRadioButton("Monitorowanie nowych bloków")
        self.radio_details.setChecked(True)

        self.action_group.addButton(self.radio_details)
        self.action_group.addButton(self.radio_status)
        self.action_group.addButton(self.radio_monitor)

        main_layout.addWidget(self.radio_details)
        main_layout.addWidget(self.radio_status)
        main_layout.addWidget(self.radio_monitor)

        # 🔹 Wykonaj
        main_layout.addStretch()
        exec_btn = QPushButton("Wykonaj")
        exec_btn.clicked.connect(self.run_action)
        main_layout.addWidget(exec_btn)

    def run_action(self):
        tx_hash = self.tx_hash_input.text().strip()
        if not tx_hash.startswith("0x"):
            QMessageBox.warning(self, "Błąd", "Nieprawidłowy hash.")
            return

        if self.radio_details.isChecked():
            get_transaction_data(self.web3, tx_hash)
        elif self.radio_status.isChecked():
            get_transaction_status(self.web3, tx_hash)
        elif self.radio_monitor.isChecked():
            stream_blocks(self.web3)
        self.close()

    def open_url(self, url):
        webbrowser.open(url)
