import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QLabel
from PyQt5.QtWidgets import QMainWindow, QAction, qApp




class Fenetre(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.setUi()

    def setUi(self):
        self.setWindowTitle("Client")
        self.resize(800,600)
        self.move(300,200)

        exitAction = QAction("&Exit", self)
        exitAction.setShortcut("Ctrl+Q")
        exitAction.setStatusTip("Quitter l'application")
        exitAction.triggered.connect(qApp.exit)

        client_text = QLabel("Fenetre client")
        self.bouton1 = QPushButton("Bouton 1")
        
        layout = QVBoxLayout()
        layout.addWidget(client_text)
        layout.addWidget(self.bouton1)
        self.setLayout(layout)

    # def mousePressEvent(self, event):

app = QApplication.instance()
if not app:
    app = QApplication(sys.argv)
    
fen = Fenetre() #créé la fenetre via sa classe
fen.show()      #Affiche la fenetre

app.exec_()