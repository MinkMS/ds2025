import socket

def start_server(host='127.0.0.1', port=65432, output_file='received_file.txt'):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)

    print(f"Server listening on {host}:{port}...")

    conn, addr = server_socket.accept()
    print(f"Connected by {addr}")

    with open(output_file, 'wb') as file:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            file.write(data)

    print(f"File received and saved as {output_file}.")
    conn.close()
    server_socket.close()

if __name__ == "__main__":
    start_server()