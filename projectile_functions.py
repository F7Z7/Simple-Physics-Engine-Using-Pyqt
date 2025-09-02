import math


class Projectile_Functions():
    def __init__(self):
        self.v = 0  # initial speed
        self.vx, self.vy = 0, 0  # velocity components
        self.x, self.y = 0, 0  # position
        self.ax, self.ay = 0, 0  # accelerations
        self.G = 9.81  # gravity
        self.air_resistance = False

    def with_air_resistance(self, dt=0.05, speed=30, deg_ang=45, m=1, k=0.1):
        points = []
        angle = math.radians(deg_ang)
        self.vx = speed * math.cos(angle)
        self.vy = speed * math.sin(angle)
        self.x, self.y = 0, 0

        while self.y >= 0:
            ax = - (k / m) * self.vx
            ay = -self.G - (k / m) * self.vy

            self.vx += ax * dt
            self.vy += ay * dt
            self.x += self.vx * dt
            self.y += self.vy * dt

            points.append((self.x, self.y))

        return points

    def stats(self):
        v0 = self.v
        theta = self.angle
        g = self.G

        # default equations
        T = (2 * v0 * math.sin(theta)) / g
        H = (v0 ** 2 * (math.sin(theta)) ** 2) / (2 * g)
        R = (v0 ** 2 * math.sin(2 * theta)) / g
        vx = v0 * math.cos(theta)

        return {
            "Time of Flight": round(T, 3),
            "Max Height": round(H, 3),
            "Range": round(R, 3),
            "Horizontal Velocity": round(vx, 3),
        }

    def without_air_resistance(self, dt=0.05,speed=30, deg_ang=45):
        points = []
        angle = math.radians(deg_ang)
        self.vx = speed * math.cos(angle)
        self.vy = speed * math.sin(angle)
        self.x, self.y = 0, 0
        self.ax = 0
        self.ay = -self.G
        while self.y >= 0:
            self.vx += self.ax * dt
            self.vy += self.ay * dt
            self.x += self.vx * dt
            self.y += self.vy * dt
            points.append((self.x, self.y))
        return points
