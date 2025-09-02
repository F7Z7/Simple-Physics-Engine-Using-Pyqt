import math


class Projectile_Functions():
    def __init__(self):
        v = 0  # initial speed
        vx, vy = 0, 0  # velocity components
        x, y = 0, 0  # position
        ax, ay = 0, 0  # accelerations
        G = 9.81  # gravity
        air_resistance = False
        TIME_STEP = 0.05

    @staticmethod
    def with_air_resistance(self, dt=0.05, speed=30, deg_ang=45, m=1, k=0.1):
        points = []
        G = 9.81
        angle = math.radians(deg_ang)
        vx = speed * math.cos(angle)
        vy = speed * math.sin(angle)
        x, y = 0, 0

        while y >= 0:
            ax = - (k / m) * vx
            ay = -G - (k / m) * vy

            vx += ax * dt
            vy += ay * dt
            x += vx * dt
            y += vy * dt

            points.append((x,y))

        return points
    @staticmethod
    def stats(v0, theta, g=9.81):

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
    @staticmethod
    def without_air_resistance(self, dt=0.05,speed=30, deg_ang=45):
        G = 9.81
        points = []
        angle = math.radians(deg_ang)
        vx = speed * math.cos(angle)
        vy = speed * math.sin(angle)
        x, y = 0, 0
        ax = 0
        ay = -G
        while y >= 0:
            vx += ax * dt
            vy += ay * dt
            x += vx * dt
            y += vy * dt
            points.append((x, y))
        return points
