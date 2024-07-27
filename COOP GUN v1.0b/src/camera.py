class Camera:
    def __init__(self, app) -> None:
        self.target_pos = [0, 0]
        self.center = app.center
        self.dx = 0
        self.dy = 0
        self.move_delta = 0.01
        self.pos = [0, 0]
        

    def update(self):
        self.dx = (self.target_pos[0]-self.center[0]+self.pos[0])*self.move_delta
        self.dy = (self.target_pos[1]-self.center[1]+self.pos[1])*self.move_delta
        self.pos[0]-=self.dx
        self.pos[1]-=self.dy

    