#!/usr/bin/env python3

import sys
import socket
import threading
from tkinter import *
from tkinter.scrolledtext import ScrolledText
from tkinter.simpledialog import askstring as DialogBox

class Client:

    def __init__(self, server_host, server_port) -> None:
        self.SERVER_HOST = server_host
        self.SERVER_PORT = server_port

        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((self.SERVER_HOST, self.SERVER_PORT))
        except:
            print(f"[!] Server at {self.SERVER_HOST}:{self.SERVER_PORT} unavailable")
            sys.exit()

        print(f"[+] Starting client")

        self.username = DialogBox("Chat", "Username")
        self.client_socket.sendall(self.username.encode())

        thread = threading.Thread(target=self.__receive_message)
        thread.daemon = True
        thread.start()

        self.__render_chat()

        self.client_socket.close()

    def __render_chat(self):
        self.window = Tk()
        self.window.title("Chat")

        self.text_widget = ScrolledText(self.window, state='disabled')
        self.text_widget.pack(padx=5, pady=5)

        frame_widget = Frame(self.window)
        frame_widget.pack(fill=BOTH)

        self.input_widget = Entry(frame_widget, font=("Arial", 14))
        self.input_widget.bind("<Return>", lambda _: self.__send_message())
        self.input_widget.pack(padx=5, pady=5, side=LEFT, fill=BOTH, expand=1)

        send_widget = Button(frame_widget, text="Send", command=lambda: self.__send_message())
        send_widget.pack(padx=3, pady=5, side=RIGHT)

        list_users_widget = Button(self.window, text="List users", command=lambda: self.__list_users())
        list_users_widget.pack(padx=5, pady=5, fill=X, expand=1)

        exit_widget = Button(self.window, text="Exit", command=lambda: self.__exit())
        exit_widget.pack(padx=5, pady=5, fill=X, expand=1)

        self.window.mainloop()

    def __send_message(self):
        message = f"({self.username}) > {self.input_widget.get()}\n"

        self.input_widget.delete(0, END)
        self.text_widget.configure(state='normal')
        self.text_widget.insert(END, message)
        self.text_widget.configure(state='disabled')

        self.client_socket.sendall(message.encode())

    def __receive_message(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode()
 
                if not message:
                    break

                self.text_widget.configure(state='normal')
                self.text_widget.insert(END, message)
                self.text_widget.configure(state='disabled')

            except:
                print(f"[!] Connection lost")
                break

    def __list_users(self):
        self.client_socket.sendall("!users".encode())

    def __exit(self):
        self.client_socket.sendall(f"\n[!] {self.username} leave the chat\n\n".encode())
        self.client_socket.close()
        self.window.quit()
        self.window.destroy()

if __name__ == "__main__":
    Client("localhost", 12345)
