
class Volume:
    def __init__(self, volume_name):
        self.volume_name = volume_name
        self.bricks = []

    def add_brick(self, brick):
        self.bricks.append(brick)
