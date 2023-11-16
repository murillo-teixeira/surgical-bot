class Position:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.z = 0

class Orientation:
    def __init__(self):
        self.roll = 0
        self.pitch = 0

class Pose:
    def __init__(self):
        self.position = Position()
        self.orientation = Orientation()

    def update_pose(self, pose_array):
        self.position.x = pose_array[0]
        self.position.y = pose_array[1]
        self.position.z = pose_array[2]
        self.orientation.roll = pose_array[3]
        self.orientation.pitch = pose_array[4]

    def __str__(self):
        return f"X: {self.position.x}, Y: {self.position.y}, Z: {self.position.x}, P: {self.orientation.pitch}, R: {self.orientation.roll}"