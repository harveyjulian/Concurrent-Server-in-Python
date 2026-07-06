import socket

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 5050
CLIENT_NAME = "Client of Raphael Romero"

num = int(input("Enter an integer (1-100): "))
print("You entered:", num)

# create socket and connect to server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((SERVER_HOST, SERVER_PORT))
print("Connected to server.")

# send message: "name,number"
message = CLIENT_NAME + "," + str(num)
s.send(message.encode())
print("Sent to server:", message)

data = s.recv(1024).decode()
print("Received from server:", data)

if data.startswith("ERROR"):
    print("Server reported an error and is shutting down.")
else:
    server_name, server_num_str = data.split(",")
    server_num = int(server_num_str)
    total = num + server_num

    print("Client name:", CLIENT_NAME)
    print("Server name:", server_name)
    print("Client number:", num)
    print("Server number:", server_num)
    print("Sum:", total)

s.close()
print("Connection closed.")
