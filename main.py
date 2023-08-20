import sys
from PyQt5.QtWidgets import QApplication
from window import MainWindow

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    #window.show()
    #sys.exit(app.exec_())
    app.exec()

if __name__ == "__main__":
    main()
