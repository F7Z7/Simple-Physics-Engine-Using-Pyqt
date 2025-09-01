from PyQt5.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QPushButton, QVBoxLayout


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simple Physics Engine")
        self.resize(500, 500)
        self.show()
        self.initUI()

    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        self.main_layout = QVBoxLayout(central_widget)

        self.button_layout = QHBoxLayout()
        self.button_list=["Launch","Reset Settings","Gravity"]
        for button in self.button_list:
            self.button_layout.addWidget(QPushButton(button))

        self.main_layout.addLayout(self.button_layout)


