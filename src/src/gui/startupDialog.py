from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
)
from PyQt5.QtCore import Qt


class StartupDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Konfiguracja połączenia")
        self.setMinimumSize(300, 100)

        self.rpc_url = ""
        self.private_key = ""

        layout = QVBoxLayout()
        layout.setSpacing(15)

        self.label_rpc = QLabel("Adres RPC:")
        self.input_rpc = QLineEdit()
        self.input_rpc.setPlaceholderText("np. http://127.0.0.1:8545")

        self.label_key = QLabel("Klucz prywatny:")
        self.input_key = QLineEdit()
        self.input_key.setPlaceholderText("np. 0xABCDEF...")
        self.input_key.setEchoMode(QLineEdit.Password)

        self.submit_btn = QPushButton("Zatwierdź")
        self.submit_btn.clicked.connect(self.accept_inputs)

        layout.addWidget(self.label_rpc)
        layout.addWidget(self.input_rpc)
        layout.addWidget(self.label_key)
        layout.addWidget(self.input_key)
        layout.addWidget(self.submit_btn)

        self.setLayout(layout)

    def accept_inputs(self):
        rpc = self.input_rpc.text().strip()
        key = self.input_key.text().strip()

        if not rpc or not key:
            QMessageBox.warning(self, "Brak danych", "Wprowadź oba pola.")
            return

        self.rpc_url = rpc
        self.private_key = key
        self.accept()
