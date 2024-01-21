#!/usr/bin/env python3

import socket
import threading

clients = []
usernames = {}

SERVER_HOST = 'localhost'
SERVER_PORT = 12345

def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((SERVER_HOST, SERVER_PORT))
    server_socket.listen()

    print(f"[+] Server started and listening for connetions at port {SERVER_PORT}...")

    while True:
        client_socket, client_address = server_socket.accept()
        clients.append(client_socket)

        thread = threading.Thread(target=client_thread, args=(client_socket, client_address, clients, usernames))
        thread.daemon = True
        thread.start()

    server_socket.close()

def client_thread(client_socket, client_address, clients, usernames):
    username = client_socket.recv(1024).decode()
    usernames[client_socket] = username

    print(f"[+] User \"{username}\" connected at {client_address}")

    for client in clients:
        if client is not client_socket:
            client.sendall(f"\nServer > ({username}) has connected\n\n".encode())

    while True:
        try:
            message = client_socket.recv(1024).decode()

            if not message:
                break

            for client in clients:
                if client is not client_socket:
                    client.sendall(message.encode())
        except:
            break

if __name__ == "__main__":
    server()
 
