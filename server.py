#!/usr/bin/env python3

import ssl
import socket
import threading

class Server:

    def __init__(self, port: int = 12345) -> None:
    
        self.clients = []
        self.usernames = {}

        self.SERVER_HOST = 'localhost'
        self.SERVER_PORT = port

    def run(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((self.SERVER_HOST, self.SERVER_PORT))
        ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        ssl_context.load_cert_chain("server-cert.pem", "server-key.key")
        server_socket = ssl_context.wrap_socket(sock=server_socket, server_side=True)
        server_socket.listen()

        print(f"[+] Server started and listening for connetions at port {self.SERVER_PORT}...")

        while True:
            client_socket, client_address = server_socket.accept()
            self.clients.append(client_socket)

            thread = threading.Thread(target=self.__client_thread, args=(client_socket, client_address))
            thread.daemon = True
            thread.start()

        server_socket.close()

    def __client_thread(self, client_socket, client_address):
        username = client_socket.recv(1024).decode()
        self.usernames[client_socket] = username

        print(f"[+] User \"{username}\" connected from {client_address}")

        for client in self.clients:
            if client is not client_socket:
                client.sendall(f"\nServer > ({username}) joined the chat\n\n".encode())

        while True:
            try:
                message = client_socket.recv(1024).decode()

                if not message:
                    break

                if message == '!users':
                    users = "\n".join(self.usernames.values())
                    client_socket.sendall(f"\n[+] Connected users:\n{users}\n\n".encode())
                    continue


                for client in self.clients:
                    if client is not client_socket:
                        client.sendall(message.encode())
            except:
                break

        client_socket.close()
        self.clients.remove(client_socket)
        del self.usernames[client_socket]

if __name__ == "__main__":
    Server().run()
 
