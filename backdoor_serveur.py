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


def socket_receive_all_data(socket_p, data_len):
    total_data = None
    current_data_len = 0
    # print("Socket data receive len:", data_len)
    while current_data_len < data_len:
        chunk_len = data_len - current_data_len
        if chunk_len > MAX_DATA_SIZE:
            chunk_len = MAX_DATA_SIZE
        data = socket_p.recv(chunk_len)
        # print("  len:", len(data))
        if not data:
            return None
        if not total_data:
            total_data = data
        else:
            total_data += data
        current_data_len += len(data)
        # print("  Total len:", current_data_len, "/", data_len)
    return total_data


def socket_send_command_and_receive_all_data(socket_p, command):
    if not command:
        return None
    socket_p.sendall(command.encode())

    header_data = socket_receive_all_data(socket_p, 13)
    data_length = int(header_data.decode())

    data_recues = socket_receive_all_data(socket_p, data_length)
    return data_recues


s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST_IP, HOST_PORT))
s.listen()

print(f"Attente de connexion sur {HOST_IP}, port {HOST_PORT}...")
connection_socket, client_address = s.accept()
print(f"Connexion établie avec {client_address}")
dl_filename = None

while True:
    infos_data = socket_send_command_and_receive_all_data(connection_socket, "infos")
    if not infos_data:
        break
    commande = input(client_address[0] + ":" + str(client_address[1]) + " " + infos_data.decode())

    commande_split = commande.split(" ")
    if len(commande_split) == 2 and commande_split[0] == "dl":
        dl_filename = commande_split[1]

    data_recues = socket_send_command_and_receive_all_data(connection_socket, commande)
    if not data_recues:
        break
    if dl_filename:
        if len(data_recues) == 1 and data_recues == b" ":
            print("ERREUR! Le fichier n'existe pas")
        else:
            file = open(dl_filename, "wb")
            file.write(data_recues)
            file.close()
            print("Fichier téléchargé")
        dl_filename = None
    else:
        print(data_recues.decode())

s.close()
connection_socket.close()
