
import os

class Brick:
    def __init__(self, brick_name, node_id, volume_name):
        self.brick_name = brick_name
        self.node_id = node_id
        self.volume_name = volume_name
        self.path = os.path.join('./storage', f"volume_{volume_name}_brick_{brick_name}")
        if not os.path.exists(self.path):
            os.makedirs(self.path)

    def store_file(self, file_name, file_data):
        file_path = os.path.join(self.path, file_name)
        with open(file_path, 'w') as file:
            file.write(file_data)
        return file_path
