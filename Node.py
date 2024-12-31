import socket


def connect_to_node(node_id):
    port = 5000 + node_id
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', port))
    return client_socket


def store_file(node_id, file_name, file_data):
    request = f"STORE {file_name} {file_data}"
    client_socket = connect_to_node(node_id)
    client_socket.send(request.encode('utf-8'))
    response = client_socket.recv(1024).decode('utf-8')
    print(f"Response from Node {node_id} (Port {5000 + node_id}): {response}")
    client_socket.close()


def retrieve_file(node_id, file_name):
    request = f"RETRIEVE {file_name}"
    client_socket = connect_to_node(node_id)
    client_socket.send(request.encode('utf-8'))
    response = client_socket.recv(1024).decode('utf-8')
    print(f"Response from Node {node_id} (Port {5000 + node_id}): {response}")
    client_socket.close()


def heartbeat(node_id):
    request = "HEARTBEAT"
    client_socket = connect_to_node(node_id)
    client_socket.send(request.encode('utf-8'))
    response = client_socket.recv(1024).decode('utf-8')
    print(f"Heartbeat response from Node {node_id} (Port {5000 + node_id}): {response}")
    client_socket.close()


def print_status(node_id, all_nodes):
    print(f"Connected to Node {node_id} (Port {5000 + node_id}). Nodes in the system: {', '.join(map(str, all_nodes))}")


def start_client():
    node_id = int(input("Enter node ID to connect to: "))
    all_nodes = [1, 2, 3]  # Danh sách các node
    print_status(node_id, all_nodes)
    
    while True:
        command = input("Enter command (STORE <file_name> <file_data>, RETRIEVE <file_name>, HEARTBEAT, EXIT): ").strip().split(" ")

        if command[0] == "STORE":
            file_name = command[1]
            file_data = " ".join(command[2:])
            store_file(node_id, file_name, file_data)

        elif command[0] == "RETRIEVE":
            file_name = command[1]
            retrieve_file(node_id, file_name)

        elif command[0] == "HEARTBEAT":
            heartbeat(node_id)

        elif command[0] == "EXIT":
            print("Exiting the client.")
            break

        else:
            print("Invalid command. Please try again.")


if __name__ == "__main__":
    start_client()
