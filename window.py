class Window():
    def __init__(self, x_min, x_max, y_min, y_max):
        self.x_min = x_min
        self.padrao_x_min = x_min
        self.x_max = x_max
        self.padrao_x_max = x_max
        self.y_min = y_min
        self.padrao_y_min = y_min
        self.y_max = y_max
        self.padrao_y_max = y_max
        self.centerX = self.x_max - self.x_min
        self.centerY = self.y_max - self.y_min
