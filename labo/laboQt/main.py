from PyQt6 import QtWidgets, QtGui, uic
import sys

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("interface.ui", self)

        # Connecter le bouton à la fonction
        self.pushButton_image.clicked.connect(self.show_image)

    def show_image(self):
        pixmap = QtGui.QPixmap("image.png")  # Remplacez par le chemin de votre image
        self.label_image.setPixmap(pixmap)
        self.label_image.setScaledContents(True)

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec())