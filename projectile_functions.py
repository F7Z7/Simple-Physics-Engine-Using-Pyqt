import math


class Projectile_Functions():
    def __init__(self):
        self.v = 0  # initial speed
        self.vx, self.vy = 0, 0  # velocity components
        self.x, self.y = 0, 0  # position
        self.ax, self.ay = 0, 0  # accelerations
        self.G = 9.81  # gravity
        self.air_resistance = False

    def default_condtions(self, speed, deg_ang=45):
        launch_angle = math.radians(deg_ang)
        self.v = speed
        self.vx = speed * math.cos(launch_angle)
        self.vx = speed * math.cos(launch_angle)  # basic equations
        self.x, self.y = 0, 0

    def with_air_resistance(self):
        pass

    def stats(self):
        v0 = self.v
        theta = self.angle
        g = self.G

        # default equations
        T = (2 * v0 * math.sin(theta)) / g
        H = (v0 ** 2 * (math.sin(theta)) ** 2) / (2 * g)
        R = (v0 ** 2 * math.sin(2 * theta)) / g
        vx = v0 * math.cos(theta)

    def without_air_resistance(self, dt=0.1):
        self.ax = 0
        self.ay = -self.G
        # interpolating the values of the trajectory
        self.vx += self.ax * dt
        self.vy += self.ay * dt

        self.x += self.vx * dt
        self.y += self.vy * dt

        # this values will be given to the pyqt graph which will plot this
        return self.x, self.y
