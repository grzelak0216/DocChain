import sys
from PyQt5.QtWidgets import QApplication
from src.gui.blockchainApp import BlockchainApp
from src.gui.startupDialog import StartupDialog

def main():
    app = QApplication(sys.argv)

    startup = StartupDialog()
    if startup.exec_() == StartupDialog.Accepted:
        window = BlockchainApp(startup.rpc_url, startup.private_key)
        window.show()
        sys.exit(app.exec_())
    else:
        sys.exit(0)

if __name__ == "__main__":
    main()
