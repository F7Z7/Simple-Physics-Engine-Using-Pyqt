import math
class Projectile_Functions():
    def __init__(self):
        self.v = 0  # initial speed
        self.vx, self.vy = 0, 0  # velocity components
        self.x, self.y = 0, 0  # position
        self.ax, self.ay = 0, 0  # accelerations
        self.G = 9.81  # gravity
        self.air_resistance = False

    def default_condtions(self,speed,deg_ang=45):
        launch_angle=math.radians(deg_ang)
        self.v=speed
        self.vx=speed*math.cos(launch_angle)
        self.vx=speed*math.cos(launch_angle) #basic equations
        self.x, self.y = 0, 0

    def with_air_resistance(self):
        pass
    def without_air_resistance(self):
        pass