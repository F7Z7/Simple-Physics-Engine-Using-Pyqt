from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QPushButton, QVBoxLayout, QMessageBox, QLabel, QLineEdit, \
    QComboBox, QCheckBox
from projectile_functions import Projectile_Functions
import pyqtgraph as pg


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simple Physics Engine")
        self.resize(500, 500)
        self.show()
        self.initUI()

        self.points_air = []
        self.points_no_air = []
        self.both_cases = False
        self.TIMER_INTERVAL = 50

    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.setStyleSheet("""
                QMainWindow {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                      stop:0 #f0f4f8, stop:1 #e2e8f0);
        }
        
        QGroupBox {
            font-weight: bold;
            font-size: 14px;
            color: #2d3748;
            border: 2px solid #cbd5e0;
            border-radius: 8px;
            margin-top: 10px;
            padding-top: 10px;
            background-color: rgba(255, 255, 255, 0.8);
        }
        
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 8px 0 8px;
        }
        
        QPushButton {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                      stop:0 #4299e1, stop:1 #3182ce);
            border: none;
            border-radius: 8px;
            color: white;
            font-weight: bold;
            font-size: 12px;
            padding: 10px 20px;
            min-width: 100px;
            min-height: 35px;
        }
        
      QPushButton {
    background: #3182ce;   /* primary blue */
    color: white;
    border-radius: 6px;
    padding: 6px 12px;
    font-size: 13px;
}

QPushButton:hover {
    background: #2b6cb0;   /* darker blue on hover */
}

QPushButton:pressed {
    background: #2c5282;   /* even darker on press */
}

QPushButton#launchButton {
    background: #38a169;   /* green */
    font-weight: bold;
    min-width: 120px;
}

QPushButton#launchButton:hover {
    background: #2f855a;
}

QPushButton#resetButton {
    background: #dd6b20;   /* orange */
}

QPushButton#resetButton:hover {
    background: #c05621;
}

        
        QLineEdit {
            border: 2px solid #cbd5e0;
            border-radius: 6px;
            padding: 8px 12px;
            font-size: 12px;
            background-color: white;
            selection-background-color: #4299e1;
        }
        
        QLineEdit:focus {
            border-color: #4299e1;
            outline: none;
        }
        
        QLineEdit:read-only {
            background-color: #f7fafc;
            color: #4a5568;
        }
        
        QComboBox {
            border: 2px solid #cbd5e0;
            border-radius: 6px;
            padding: 8px 12px;
            font-size: 12px;
            background-color: white;
            min-width: 150px;
        }
        
        QComboBox:focus {
            border-color: #4299e1;
        }

        QLabel {
            font-size: 12px;
            font-weight: bold;
            color: #2d3748;
            padding: 5px;
        }
        
            """)

        # flags
        self.gravity = True
        self.air_resistance = True

        self.main_layout = QHBoxLayout(central_widget)

        # --- Left controls panel ---
        self.controls_layout = QVBoxLayout()

        # Input fields
        # Angle row
        angle_row = QHBoxLayout()
        angle_label = QLabel("Angle (°):")
        self.angle_input = QLineEdit()
        self.angle_input.setPlaceholderText("Enter Launch Angle")
        self.angle_input.setValidator(QDoubleValidator(0, 90, 2))
        self.angle_input.setFixedWidth(100)  # keeps it compact
        angle_row.addWidget(angle_label)
        angle_row.addWidget(self.angle_input)
        self.controls_layout.addLayout(angle_row)

        # Speed row
        speed_row = QHBoxLayout()
        speed_label = QLabel("Speed (m/s):")
        self.speed_input = QLineEdit()
        self.speed_input.setPlaceholderText("Enter Launch Velocity")
        self.speed_input.setValidator(QDoubleValidator(0, 1000, 2))
        self.speed_input.setFixedWidth(100)
        speed_row.addWidget(speed_label)
        speed_row.addWidget(self.speed_input)
        self.controls_layout.addLayout(speed_row)

        # Buttons
        self.launch_button = QPushButton("Launch")
        self.launch_button.setObjectName("launchButton")
        self.launch_button.clicked.connect(self.launch_btn)
        self.controls_layout.addWidget(self.launch_button)

        self.reset_button = QPushButton("Reset Settings")
        self.reset_button.setObjectName("resetButton")
        self.reset_button.clicked.connect(self.reset_btn)
        self.controls_layout.addWidget(self.reset_button)

        # Dropdown
        self.air_resistance_select = QComboBox()
        self.air_resistance_select.addItems(["Air Resistance", "Without Air Resistance", "Both"])
        self.air_resistance_select.currentIndexChanged.connect(self.air_resistance_btn)
        self.controls_layout.addWidget(self.air_resistance_select)

        # Optional: add stats panel later here
        self.stats_layout = QVBoxLayout()
        self.show_stats=QCheckBox("Show Stats")
        self.show_stats.setChecked(True)
        self.show_stats.stateChanged.connect(self.toggle_stats)
        self.controls_layout.addWidget(self.show_stats)
        self.controls_layout.addLayout(self.stats_layout)

        # Compact fixed width
        controls_widget = QWidget()
        controls_widget.setLayout(self.controls_layout)
        controls_widget.setFixedWidth(200)

        # --- Right plot panel ---
        self.plot_widget = pg.PlotWidget()
        self.plot_widget.setBackground("w")
        self.plot_widget.setLabel("bottom", "X Distance (m)")
        self.plot_widget.setLabel("left", "Y Height (m)")
        self.plot_widget.showGrid(x=True, y=True)

        # Add to main layout
        self.main_layout.addWidget(controls_widget)
        self.main_layout.addWidget(self.plot_widget, stretch=1)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_position)

    def launch_btn(self):
        try:
            angle_text = self.angle_input.text().strip()
            speed_text = self.speed_input.text().strip()
            angle = float(angle_text) if angle_text != "" else 45
            speed = float(speed_text) if speed_text != "" else 20
        except ValueError:
            QMessageBox.warning(self, "Warning", "Please enter valid numbers for angle and speed")
            return

        # Clear previous plots
        self.plot_widget.clear()
        self.plot_widget.addLegend()

        self.index = 0  # reset animation

        if self.both_cases:
            # Compute both trajectories
            self.points_air = Projectile_Functions.with_air_resistance(speed=speed, deg_ang=angle)
            self.points_no_air = Projectile_Functions.without_air_resistance(speed=speed, deg_ang=angle)

            # Plot curves
            self.curve_air = self.plot_widget.plot([], [], pen='b', name="With Air Resistance")
            self.curve_no_air = self.plot_widget.plot([], [], pen='r', name="Without Air Resistance")

            # Balls
            self.ball_air = self.plot_widget.plot([], [], pen=None, symbol='o', symbolBrush='b')
            self.ball_no_air = self.plot_widget.plot([], [], pen=None, symbol='o', symbolBrush='r')

        else:
            if self.air_resistance:
                self.points_air = Projectile_Functions.with_air_resistance(speed=speed, deg_ang=angle)
                self.curve_air = self.plot_widget.plot([], [], pen='b', name="With Air Resistance")
                self.ball_air = self.plot_widget.plot([], [], pen=None, symbol='o', symbolBrush='b')
                self.points_no_air = []
            else:
                self.points_no_air = Projectile_Functions.without_air_resistance(speed=speed, deg_ang=angle)
                self.curve_no_air = self.plot_widget.plot([], [], pen='r', name="Without Air Resistance")
                self.ball_no_air = self.plot_widget.plot([], [], pen=None, symbol='o', symbolBrush='r')
                self.points_air = []

        self.timer.start(50)

        self.index = 0
        self.timer.start(self.TIMER_INTERVAL)
        print("Launching button")

    def reset_btn(self):
        self.gravity = True
        self.air_resistance = True

        self.timer.stop()
        self.index = 0

        self.plot_widget.clear()
        self.plot_widget.setLabel("bottom", "X Distance (m)")
        self.plot_widget.setLabel("left", "Y Height (m)")
        self.plot_widget.showGrid(x=True, y=True)

        self.points_air = []
        self.points_no_air = []
        self.both_cases = False

        self.angle_input.clear()
        self.speed_input.clear()

        self.air_resistance_select.setCurrentIndex(0)

    def air_resistance_btn(self):
        self.air_resistance_select_input = self.air_resistance_select.currentText()

        if self.air_resistance_select_input == "Air Resistance":
            self.air_resistance = True
        elif self.air_resistance_select_input == "Without Air Resistance":
            self.air_resistance = False
        else:
            self.both_cases = True

    def update_position(self):
        moved = False
        if self.index < len(self.points_air):
            x, y = self.points_air[self.index]
            if self.ball_air:
                self.ball_air.setData([x], [y])
                x_vals = [p[0] for p in self.points_air[:self.index + 1]]
                y_vals = [p[1] for p in self.points_air[:self.index + 1]]
                self.curve_air.setData(x_vals, y_vals)
            moved = True

        if self.index < len(self.points_no_air):
            x, y = self.points_no_air[self.index]
            if self.ball_air:
                self.ball_no_air.setData([x], [y])
                x_vals = [p[0] for p in self.points_no_air[:self.index + 1]]
                y_vals = [p[1] for p in self.points_no_air[:self.index + 1]]
                self.curve_no_air.setData(x_vals, y_vals)
            moved = True
        self.index += 1
        if not moved:
            self.timer.stop()
