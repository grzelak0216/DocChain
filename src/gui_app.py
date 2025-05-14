import sys
from PyQt5.QtWidgets import QApplication
from src.gui.blockchainApp import BlockchainApp

def main():
    app = QApplication(sys.argv)
    window = BlockchainApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
