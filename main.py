# Author: przewnic

from PyQt5 import QtWidgets
import sys

from MainWindow import MainWindow


def main():
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
