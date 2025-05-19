import os
import sys
import logging
from PyQt5.QtWidgets import (
    QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox,
    QLineEdit, QStyle, QLabel, QTextEdit, QSizePolicy
)
from PyQt5.QtGui import QPixmap, QPalette, QBrush
from PyQt5.QtCore import Qt, QObject, pyqtSignal

from src.blockchain import connect_web3, load_contract, deploy_contract
from src.gui.transactionDialog import TransactionDialog
from src.document_handler import (
    add_document, verify_document_ui,
    update_document_ui, delete_document_ui
)
from src.utils import read_file_binary


# === Logger setup ===
if not os.path.exists("logs"):
    os.makedirs("logs")

logger = logging.getLogger("DocChain")
logger.setLevel(logging.INFO)
logger.handlers.clear()

formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')

# File handler
file_handler = logging.FileHandler("logs/app_logs.log", encoding="utf-8")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Terminal handler
stream_handler = logging.StreamHandler(sys.__stdout__)
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

# GUI handler
class GuiLogHandler(logging.Handler):
    def __init__(self, callback):
        super().__init__()
        self.callback = callback

    def emit(self, record):
        msg = self.format(record)
        self.callback(msg)


class BlockchainApp(QWidget):
    def __init__(self, rpc_url, private_key):
        super().__init__()
        self.rpc_url = rpc_url
        self.private_key = private_key
        self.web3 = connect_web3(rpc_url, private_key)
        self.contract = load_contract(self.web3) if os.path.exists("data/contract_address.txt") else None
        self.init_ui()

        gui_handler = GuiLogHandler(self.append_log)
        gui_handler.setFormatter(formatter)
        logger.addHandler(gui_handler)

    def init_ui(self):
        self.setWindowTitle("DocChain - GUI")
        self.setMinimumSize(1000, 800)

        # Tło
        background = QPixmap("./src/gui/bg.jpg").scaled(self.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(background))
        self.setAutoFillBackground(True)
        self.setPalette(palette)

        # Layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(15)

        # Sekcje
        main_layout.addLayout(self.section_add_document())
        main_layout.addLayout(self.section_verify_document())
        main_layout.addLayout(self.section_update_document())
        main_layout.addLayout(self.section_delete_document())
        main_layout.addWidget(self.create_button("5. Wdróż kontrakt", QStyle.SP_DialogOpenButton, self.handle_deploy_contract))
        main_layout.addWidget(self.create_button("6. Weryfikacja transakcji", QStyle.SP_MessageBoxInformation, self.handle_verify_transaction))
        main_layout.addWidget(self.create_button("7. Wyjście", QStyle.SP_DialogCloseButton, self.close))

        # Logi
        main_layout.addWidget(QLabel("Logi aplikacji:"))
        self.console_output = QTextEdit()
        self.console_output.setReadOnly(True)
        self.console_output.setMinimumHeight(200)
        self.console_output.setStyleSheet("""
            QTextEdit {
                background-color: #111;
                color: #00ffcc;
                font-family: "Courier New", "Menlo", "Consolas", monospace;
                font-size: 11px;
                border-radius: 6px;
                border: 1px solid #00cec9;
            }
        """)
        main_layout.addWidget(self.console_output)

        self.setLayout(main_layout)

        # Styl
        self.setStyleSheet("""
            QLineEdit {
                background-color: #1e272e;
                color: white;
                border: 2px solid #00cec9;
                border-radius: 6px;
                padding: 8px;
                font-size: 14px;
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
            QLabel {
                color: white;
                font-size: 13px;
            }
        """)

    def resizeEvent(self, event):
        background = QPixmap("./src/gui/bg.jpg").scaled(self.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        palette = self.palette()
        palette.setBrush(QPalette.Window, QBrush(background))
        self.setPalette(palette)
        super().resizeEvent(event)

    def append_log(self, text):
        self.console_output.append(text)

    def create_button(self, text, icon_enum, func):
        btn = QPushButton(text)
        icon = self.style().standardIcon(icon_enum)
        btn.setIcon(icon)
        btn.setFixedHeight(40)
        btn.clicked.connect(func)
        return btn

    def icon_button(self, text, icon_enum, callback):
        btn = QPushButton(text)
        icon = self.style().standardIcon(icon_enum)
        btn.setIcon(icon)
        btn.setFixedWidth(250)
        btn.setFixedHeight(40)
        btn.clicked.connect(callback)
        return btn

    def section_add_document(self):
        layout = QHBoxLayout()
        btn = self.icon_button("1. Dodaj dokument", QStyle.SP_FileDialogNewFolder, self.handle_add_document)
        layout.addWidget(btn)

        form = QVBoxLayout()
        self.add_path = QLineEdit()
        self.add_path.setPlaceholderText("Ścieżka do pliku")
        form.addWidget(self.add_path)

        lower_fields = QHBoxLayout()
        self.add_name = QLineEdit()
        self.add_type = QLineEdit()
        self.add_name.setPlaceholderText("Nazwa dokumentu")
        self.add_type.setPlaceholderText("Typ dokumentu")
        lower_fields.addWidget(self.add_name)
        lower_fields.addWidget(self.add_type)

        form.addLayout(lower_fields)
        layout.addLayout(form)
        return layout

    def section_verify_document(self):
        layout = QHBoxLayout()
        self.verify_path = QLineEdit()
        self.verify_path.setPlaceholderText("Ścieżka do pliku do weryfikacji")
        btn = self.icon_button("2. Zweryfikuj dokument", QStyle.SP_DialogApplyButton, self.handle_verify_document)
        layout.addWidget(btn)
        layout.addWidget(self.verify_path)
        return layout

    def section_update_document(self):
        layout = QHBoxLayout()
        btn = self.icon_button("3. Zaktualizuj", QStyle.SP_BrowserReload, self.handle_update_document)
        layout.addWidget(btn)

        form = QVBoxLayout()
        self.update_path = QLineEdit()
        self.update_path.setPlaceholderText("Ścieżka do pliku")
        form.addWidget(self.update_path)

        lower_fields = QHBoxLayout()
        self.update_name = QLineEdit()
        self.update_type = QLineEdit()
        self.update_name.setPlaceholderText("Nowa nazwa")
        self.update_type.setPlaceholderText("Nowy typ")
        lower_fields.addWidget(self.update_name)
        lower_fields.addWidget(self.update_type)

        form.addLayout(lower_fields)
        layout.addLayout(form)
        return layout

    def section_delete_document(self):
        layout = QHBoxLayout()
        self.delete_path = QLineEdit()
        self.delete_path.setPlaceholderText("Ścieżka do pliku do usunięcia")
        btn = self.icon_button("4. Usuń dokument", QStyle.SP_TrashIcon, self.handle_delete_document)
        layout.addWidget(btn)
        layout.addWidget(self.delete_path)
        return layout

    def handle_add_document(self):
        if not self.contract:
            QMessageBox.warning(self, "Brak kontraktu", "Najpierw wdroż kontrakt.")
            return
        path = self.add_path.text().strip()
        name = self.add_name.text().strip()
        doc_type = self.add_type.text().strip()
        if not all([path, name, doc_type]):
            QMessageBox.warning(self, "Brak danych", "Uzupełnij wszystkie pola.")
            return
        content = read_file_binary(path)
        logger.info(f"Dodawanie dokumentu: {name} ({doc_type}) | Plik: {path}")
        # add_document(self.contract, self.web3, content, name, doc_type)
        try:
            add_document(self.contract, self.web3, content, name, doc_type)
            QMessageBox.information(self, "OK", "Dokument dodany.")
        except Exception as e:
            logger.exception("Błąd podczas dodawania dokumentu")
            QMessageBox.critical(self, "Błąd", f"Błąd dodawania dokumentu:\n{str(e)}")

    def handle_verify_document(self):
        if not self.contract:
            QMessageBox.warning(self, "Brak kontraktu", "Najpierw wdroż kontrakt.")
            return
        path = self.verify_path.text().strip()
        if not path:
            QMessageBox.warning(self, "Brak pliku", "Podaj ścieżkę.")
            return
        logger.info(f"Weryfikacja dokumentu: {path}")
        verify_document_ui(self.contract)

    def handle_update_document(self):
        if not self.contract:
            QMessageBox.warning(self, "Brak kontraktu", "Najpierw wdroż kontrakt.")
            return
        path = self.update_path.text().strip()
        name = self.update_name.text().strip()
        doc_type = self.update_type.text().strip()
        if not all([path, name, doc_type]):
            QMessageBox.warning(self, "Brak danych", "Uzupełnij wszystkie pola.")
            return
        logger.info(f"Aktualizacja dokumentu: {path} → {name} ({doc_type})")
        update_document_ui(self.contract, self.web3)

    def handle_delete_document(self):
        if not self.contract:
            QMessageBox.warning(self, "Brak kontraktu", "Najpierw wdroż kontrakt.")
            return
        path = self.delete_path.text().strip()
        if not path:
            QMessageBox.warning(self, "Brak pliku", "Podaj ścieżkę.")
            return
        logger.info(f"Usuwanie dokumentu: {path}")
        delete_document_ui(self.contract, self.web3)

    def handle_deploy_contract(self):
        self.contract = deploy_contract(self.web3)
        self.contract = load_contract(self.web3, auto_deploy=False)
        logger.info("Kontrakt wdrożony i załadowany.")
        QMessageBox.information(self, "OK", "Kontrakt wdrożony.")

    def handle_verify_transaction(self):
        dialog = TransactionDialog(self.web3)
        dialog.exec_()
