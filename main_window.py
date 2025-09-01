from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QPushButton, QVBoxLayout, QMessageBox, QLabel, QLineEdit
from projectile_functions import Projectile_Functions
import pyqtgraph as pg


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simple Physics Engine")
        self.resize(500, 500)
        self.projectile = Projectile_Functions()
        self.projectile.default_condtions(speed=20, deg_ang=45)
        self.show()
        self.initUI()

    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # flags
        self.gravity = True
        self.air_resistance = True

        self.main_layout = QVBoxLayout(central_widget)

        self.plot_widget = pg.PlotWidget()
        self.main_layout.addWidget(self.plot_widget)

        self.plot_widget.setBackground("w")

        # Create curve (trajectory line) and ball (point)
        self.curve = self.plot_widget.plot([], [], pen='r')
        self.ball = self.plot_widget.plot([], [], pen=None, symbol='o', symbolBrush='b')

        self.input_layout = QHBoxLayout()


        self.input_layout.addWidget(QLabel("Angle"))
        self.angle_input = QLineEdit()
        self.angle_input.setPlaceholderText("Enter Launch Angle")
        self.input_layout.addWidget(self.angle_input)


        self.input_layout.addWidget(QLabel("Speed"))
        self.speed_input = QLineEdit()
        self.speed_input.setPlaceholderText("Enter Launch Velocity")
        self.input_layout.addWidget(self.speed_input)


        self.main_layout.addLayout(self.input_layout)

        self.button_layout = QHBoxLayout()
        self.buttons = {
            "Launch": self.launch_btn,
            "Reset Settings": self.reset_btn,
            "Gravity": self.gravity_btn,
            "Air Resistance": self.air_resistance_btn,
        }

        for name, fn in self.buttons.items():
            btn = QPushButton(name)
            btn.clicked.connect(fn)
            self.button_layout.addWidget(btn)

        self.main_layout.addStretch(1)
        self.main_layout.addLayout(self.button_layout)

        self.stats_layout = QHBoxLayout()
        stats_out = self.projectile.stats()
        for name, stat in stats_out.items():
            self.stats_layout.addWidget(QLabel(name))
            line = QLineEdit(str(stat))
            line.setReadOnly(True)
            self.stats_layout.addWidget(line)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_position)

    def launch_btn(self):
        try:
            angle = float(self.angle_input.text())
        except ValueError:
            QMessageBox.warning(self, "Warning", "Please enter a valid angle (degrees)")
            return

        try:
            speed = float(self.speed_input.text())
        except ValueError:
            QMessageBox.warning(self, "Warning", "Please enter a valid speed")
            return

        if angle == 0 or speed == 0:
            self.projectile.default_condtions(speed=speed, deg_ang=angle)

        if self.air_resistance:
            self.points = self.projectile.with_air_resistance(speed,deg_ang)
        else:
            self.points = self.projectile.without_air_resistance()

        # here the points are returned as an array of two x and y at index 0 and 1
        x_vals = [p[0] for p in self.points]
        y_vals = [p[1] for p in self.points]

        self.curve.setData(x_vals, y_vals)

        self.index = 0
        self.timer.start(50)  # update every 50 ms

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

    def update_position(self):
        if self.index < len(self.trajectory):
            x, y = self.points[self.index]
            self.ball.setData([x], [y])  # move ball
            self.index += 1
        else:
            self.timer.stop()
