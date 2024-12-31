import socket
import tkinter as tk
from tkinter import messagebox


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
    client_socket.close()
    return response


def retrieve_file(node_id, file_name):
    request = f"RETRIEVE {file_name}"
    client_socket = connect_to_node(node_id)
    client_socket.send(request.encode('utf-8'))
    response = client_socket.recv(1024).decode('utf-8')
    client_socket.close()
    return response


def heartbeat(node_id):
    request = "HEARTBEAT"
    client_socket = connect_to_node(node_id)
    client_socket.send(request.encode('utf-8'))
    response = client_socket.recv(1024).decode('utf-8')
    client_socket.close()
    return response


def print_status(node_id, all_nodes):
    return f"Connected to Node {node_id} (Port {5000 + node_id}). Nodes in the system: {', '.join(map(str, all_nodes))}"


def on_store_button_click():
    node_id = int(node_id_entry.get())
    file_name = file_name_entry.get()
    file_data = file_data_entry.get()
    response = store_file(node_id, file_name, file_data)
    response_label.config(text=f"Response: {response}")


def on_retrieve_button_click():
    node_id = int(node_id_entry.get())
    file_name = file_name_entry.get()
    response = retrieve_file(node_id, file_name)
    response_label.config(text=f"Response: {response}")


def on_heartbeat_button_click():
    node_id = int(node_id_entry.get())
    response = heartbeat(node_id)
    response_label.config(text=f"Heartbeat response: {response}")


def on_exit_button_click():
    window.quit()



window = tk.Tk()
window.title("Distributed File System Client")


node_id_label = tk.Label(window, text="Node ID:")
node_id_label.grid(row=0, column=0, padx=10, pady=5)
node_id_entry = tk.Entry(window)
node_id_entry.grid(row=0, column=1, padx=10, pady=5)

file_name_label = tk.Label(window, text="File Name:")
file_name_label.grid(row=1, column=0, padx=10, pady=5)
file_name_entry = tk.Entry(window)
file_name_entry.grid(row=1, column=1, padx=10, pady=5)

file_data_label = tk.Label(window, text="File Data:")
file_data_label.grid(row=2, column=0, padx=10, pady=5)
file_data_entry = tk.Entry(window)
file_data_entry.grid(row=2, column=1, padx=10, pady=5)

store_button = tk.Button(window, text="Store File", command=on_store_button_click)
store_button.grid(row=3, column=0, padx=10, pady=5)

retrieve_button = tk.Button(window, text="Retrieve File", command=on_retrieve_button_click)
retrieve_button.grid(row=3, column=1, padx=10, pady=5)

heartbeat_button = tk.Button(window, text="Send Heartbeat", command=on_heartbeat_button_click)
heartbeat_button.grid(row=4, column=0, padx=10, pady=5)

exit_button = tk.Button(window, text="Exit", command=on_exit_button_click)
exit_button.grid(row=4, column=1, padx=10, pady=5)

response_label = tk.Label(window, text="Response: ")
response_label.grid(row=5, column=0, columnspan=2, padx=10, pady=5)


window.mainloop()
