class Projectile_Functions():
    def __init__(self):
        self.v = 0  # initial speed
        self.vx, self.vy = 0, 0  # velocity components
        self.x, self.y = 0, 0  # position
        self.ax, self.ay = 0, 0  # accelerations
        self.G = 9.81  # gravity (m/s^2)
        self.air_resistance = False  # toggle (can connect to GUI)
