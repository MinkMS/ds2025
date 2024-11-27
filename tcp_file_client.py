import socket

def send_file(file_path, host='127.0.0.1', port=65432):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    with open(file_path, 'rb') as file:
        while (chunk := file.read(1024)):
            client_socket.sendall(chunk)

    print(f"File {file_path} has been sent.")
    client_socket.close()

if __name__ == "__main__":
    send_file('send.txt')