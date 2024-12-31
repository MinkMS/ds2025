# server.py
import socket
import threading
from Volume import volume
from Brick import brick
import os


STORAGE_DIR = './storage'
if not os.path.exists(STORAGE_DIR):
    os.makedirs(STORAGE_DIR)


file_metadata = {}


def store_file(file_name, file_data, volume, brick):
    file_path = brick.store_file(file_name, file_data)
    file_metadata[file_name] = {"size": len(file_data), "volume": volume.volume_name, "brick": brick.brick_name, "node_id": brick.node_id}
    return f"File {file_name} stored in volume {volume.volume_name}, brick {brick.brick_name}, node {brick.node_id}. Metadata: {file_metadata[file_name]}"


def retrieve_file(file_name, volume):
    if file_name in file_metadata:
        brick_name = file_metadata[file_name]["brick"]
        node_id = file_metadata[file_name]["node_id"]
        brick = next(brick for brick in volume.bricks if brick.brick_name == brick_name and brick.node_id == node_id)
        file_path = os.path.join(brick.path, file_name)
        with open(file_path, 'r') as file:
            file_data = file.read()
        return file_data
    return "File not found"


def handle_client(client_socket, node_id, volume):
    print(f"Node {node_id} is handling request on port {5000 + node_id}.")
    while True:
        request = client_socket.recv(1024).decode('utf-8')
        if request.startswith("STORE"):
            parts = request.split(" ", 2)
            file_name, file_data = parts[1], parts[2]
            brick = volume.bricks[node_id % len(volume.bricks)]  
            response = store_file(file_name, file_data, volume, brick)
            client_socket.send(response.encode('utf-8'))

        elif request.startswith("RETRIEVE"):
            parts = request.split(" ", 1)
            file_name = parts[1]
            response = retrieve_file(file_name, volume)
            client_socket.send(response.encode('utf-8'))

        elif request.startswith("HEARTBEAT"):
            client_socket.send("OK".encode('utf-8'))

        else:
            client_socket.send("Invalid Command".encode('utf-8'))

def start_node(node_id, port, volume):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', port))
    server_socket.listen(5)
    print(f"Node {node_id} is listening on port {port}...")
    
    while True:
        client_socket, _ = server_socket.accept()
        print(f"Connection established with Node {node_id}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket, node_id, volume))
        client_handler.start()
