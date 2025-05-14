import os
from PyQt5.QtWidgets import (
    QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox,
    QLineEdit, QStyle
)
from PyQt5.QtGui import QPixmap, QPalette, QBrush
from PyQt5.QtCore import Qt

from src.blockchain import connect_web3, load_contract, deploy_contract
from src.gui.transactionDialog import TransactionDialog
from src.document_handler import (
    add_document, verify_document_ui,
    update_document_ui, delete_document_ui
)
from src.utils import read_file_binary

class BlockchainApp(QWidget):
    def __init__(self):
        super().__init__()
        self.web3 = connect_web3()
        self.contract = load_contract(self.web3) if os.path.exists("data/contract_address.txt") else None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("DocChain - GUI")
        self.setMinimumSize(700, 550)

        # === Ustawiamy tło aplikacji poprzez paletę ===
        background_pixmap = QPixmap("./src/gui/bg.jpg").scaled(self.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(background_pixmap))
        self.setAutoFillBackground(True)
        self.setPalette(palette)

        # === Layout interfejsu ===
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(15)

        main_layout.addLayout(self.section_add_document())
        main_layout.addLayout(self.section_verify_document())
        main_layout.addLayout(self.section_update_document())
        main_layout.addLayout(self.section_delete_document())
        main_layout.addWidget(self.create_button("5. Wdróż kontrakt", QStyle.SP_DialogOpenButton, self.handle_deploy_contract))
        main_layout.addWidget(self.create_button("6. Weryfikacja transakcji", QStyle.SP_MessageBoxInformation, self.handle_verify_transaction))
        main_layout.addWidget(self.create_button("7. Wyjście", QStyle.SP_DialogCloseButton, self.close))

        self.setLayout(main_layout)

        self.setStyleSheet("""
            QLineEdit {
                background-color: #1e272e;
                color: white;
                border: 2px solid #00cec9;
                border-radius: 6px;
                padding: 8px;
                font-size: 14px;
            }

            QLineEdit:focus {
                border: 2px solid #00b894;
                background-color: #2f3640;
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

            QPushButton:disabled {
                background-color: #636e72;
                color: #dfe6e9;
            }

            QLabel {
                color: white;
                font-size: 13px;
            }
        """)


    def resizeEvent(self, event):
        background_pixmap = QPixmap("./src/gui/bg.jpg").scaled(self.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        palette = self.palette()
        palette.setBrush(QPalette.Window, QBrush(background_pixmap))
        self.setPalette(palette)
        super().resizeEvent(event)


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
        add_document(self.contract, self.web3, content, name, doc_type)
        QMessageBox.information(self, "OK", "Dokument dodany.")

    def handle_verify_document(self):
        if not self.contract:
            QMessageBox.warning(self, "Brak kontraktu", "Najpierw wdroż kontrakt.")
            return
        path = self.verify_path.text().strip()
        if not path:
            QMessageBox.warning(self, "Brak pliku", "Podaj ścieżkę.")
            return
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
        update_document_ui(self.contract, self.web3)

    def handle_delete_document(self):
        if not self.contract:
            QMessageBox.warning(self, "Brak kontraktu", "Najpierw wdroż kontrakt.")
            return
        path = self.delete_path.text().strip()
        if not path:
            QMessageBox.warning(self, "Brak pliku", "Podaj ścieżkę.")
            return
        delete_document_ui(self.contract, self.web3)

    def handle_deploy_contract(self):
        self.contract = deploy_contract(self.web3)
        self.contract = load_contract(self.web3, auto_deploy=False)
        QMessageBox.information(self, "OK", "Kontrakt wdrożony.")

    def handle_verify_transaction(self):
        dialog = TransactionDialog(self.web3)
        dialog.exec_()
