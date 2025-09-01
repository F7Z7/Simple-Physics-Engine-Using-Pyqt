from PyQt5.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QPushButton, QVBoxLayout, QMessageBox


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

        #flags
        self.gravity=True
        self.air_resistance=True


        self.main_layout = QVBoxLayout(central_widget)

        self.button_layout = QHBoxLayout()
        self.buttons = {
            "Launch": self.launch_btn,
            "Reset Settings": self.reset_btn,
            "Gravity": self.gravity_btn,
            "Air Resistance": self.air_resistance_btn,
        }

        for name,fn in self.buttons.items():
            btn=QPushButton(name)
            btn.clicked.connect(fn)
            self.button_layout.addWidget(btn)

        self.main_layout.addLayout(self.button_layout)

    def launch_btn(self):
        print("Launching button")
    def reset_btn(self):
        self.gravity = True
        self.air_resistance = True
        QMessageBox.about(self, "Reset", "Settings have been reset")
        print("Settings reset -> Gravity=ON, Air Resistance=ON")

    def gravity_btn(self):
        self.gravity = not self.gravity
        state = "ON" if self.gravity else "OFF"
        print(f"🌍 Gravity is now {state}")

    def air_resistance_btn(self):
        self.air_resistance = not self.air_resistance  # toggle
        state = "ON" if self.air_resistance else "OFF"
        print(f"💨 Air Resistance is now {state}")
