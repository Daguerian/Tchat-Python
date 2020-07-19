import sys
from PyQt5.QtWidgets import QApplication, QMainWindow,QWidget, QPushButton, QAction

class Fenetre(QMainWindow):
    def __init__(self):
        bar = self.menuBar()
        filemenu = bar.addMenu("File")

        newAct = QAction(QIcon("python.png"), "New...", self)
        newAct.setShortcut(QKeySequence("Ctrl+N"))
        newAct.setToolTip(tr("New File"))
        newAct.setStatusTip(tr("New File"))

        filemenu.addAction(newAct)

        newAct.triggered.connect(self.my_new_slot_method)

