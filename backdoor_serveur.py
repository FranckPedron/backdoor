# SOCKETS RÉSEAU : SERVEUR
#
# socket
#   bind (ip, port)  127.0.0.1 -> localhost
#   listen
#   accept -> socket / (ip, port)
#   close

# already used

import socket

HOST_IP = "127.0.0.1"
HOST_PORT = 32000
MAX_DATA_SIZE = 1024


def socket_receive_all_data(socket, data_len):
    total_data = None
    current_data_len = 0
    print("Socket data receive len:", data_len)
    while current_data_len < data_len:
        chunk_len = data_len - current_data_len
        if chunk_len > MAX_DATA_SIZE:
            chunk_len = MAX_DATA_SIZE
        data = socket.recv(chunk_len)
        print("  len:", len(data))
        if not data:
            return None
        if not total_data:
            total_data = data
        else:
            total_data += data
        current_data_len += len(data)
        print("  Total len:", current_data_len, "/", data_len)
    return total_data


s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST_IP, HOST_PORT))
s.listen()

print(f"Attente de connexion sur {HOST_IP}, port {HOST_PORT}...")
connection_socket, client_address = s.accept()
print(f"Connexion établie avec {client_address}")

while True:
    commande = input("Commande: ")
    if commande == "":
        continue
    connection_socket.sendall(commande.encode())

    header_data = socket_receive_all_data(connection_socket, 13)
    data_length = int(header_data.decode())

    data_recues = socket_receive_all_data(connection_socket, data_length)
    if not data_recues:
        break
    print(data_recues.decode())

s.close()
connection_socket.close()
