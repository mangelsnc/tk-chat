#!/usr/bin/env python3

import socket
import threading
from tkinter import *
from tkinter.scrolledtext import ScrolledText

def client(server_host, server_port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_host, server_port))

    print(f"[+] Starting client")
    
    username = input(f"[?] Username: ")
    client_socket.sendall(username.encode())

    window = Tk()
    window.title("Chat")

    text_widget = ScrolledText(window, state='disabled')
    text_widget.pack(padx=5, pady=5)
 
    frame_widget = Frame(window)
    frame_widget.pack(fill=BOTH)

    input_widget = Entry(frame_widget)
    input_widget.bind("<Return>", lambda _: send_message(client_socket, username, text_widget, input_widget))
    input_widget.pack(padx=5, pady=5, side=LEFT, fill=BOTH, expand=1)

    button_widget = Button(frame_widget, text="Send")
    button_widget.pack(padx=3, pady=5, side=RIGHT)

    thread = threading.Thread(target=receive_message, args=(client_socket, text_widget))
    thread.daemon = True
    thread.start()

    window.mainloop()
    client_socket.close()

def send_message(client_socket, username, text_widget, input_widget):
    message = f"({username}) > {input_widget.get()}\n"
    
    input_widget.delete(0, END)
    text_widget.configure(state='normal')
    text_widget.insert(END, message)
    text_widget.configure(state='disabled')

    client_socket.sendall(message.encode())

def receive_message(client_socket, text_widget):
    while True:
        try:
            message = client_socket.recv(1024).decode()
            
            if not message:
                break

            text_widget.configure(state='normal')
            text_widget.insert(END, message)
            text_widget.configure(state='disabled')

        except:
            print(f"[!] Connection lost")
            break

if __name__ == "__main__":
    client("localhost", 12345)
