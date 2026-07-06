import socket
import threading
import os
import time  # for testing only to make the two client concurrently connect

HOST = ""
PORT = 5050
SERVER_NAME = "Server of Jane Q. Public"


def handle_client(conn, addr):
    print("Connected by", addr)
    time.sleep(3) # for testing only to make the two clients concurrently connect
    
    # receive the client's message: "name,number"
    data = conn.recv(1024).decode()
    print("Received from client:", data)

    client_name, client_num_str = data.split(",")
    client_num = int(client_num_str)

    print("Client name:", client_name)
    print("Server name:", SERVER_NAME)

    # check for out-of-range value -> shut server down
    if client_num < 1 or client_num > 100:
        print("Out-of-range value received:", client_num)
        conn.send("ERROR,out of range".encode())
        conn.close()
        print("Closing server.")
        os._exit(0)   # terminate the whole server process right away

    server_num = 42   # server always picks this number

    total = client_num + server_num
    print("Client number:", client_num)
    print("Server number:", server_num)
    print("Sum:", total)

    # send reply back: "name,number"
    reply = SERVER_NAME + "," + str(server_num)
    conn.send(reply.encode())
    print("Sent to client:", reply)

    conn.close()
    print("Connection closed with", addr)


# create socket, bind, listen
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(5)
print("Server started, listening on port", PORT)

while True:
    conn, addr = s.accept()
    # spawn a new thread to handle each client (concurrent server)
    t = threading.Thread(target=handle_client, args=(conn, addr))
    t.start()
