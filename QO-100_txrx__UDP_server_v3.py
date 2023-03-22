import socket

# create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# bind the socket to a specific address and port
server_address = ('localhost', 10000)
sock.bind(server_address)

print('Listening for incoming connections...')

# dictionary to keep track of client addresses and ports
clients = {}

while True:
    # receive data from client
    data, client_address = sock.recvfrom(1024)
    
    if client_address not in clients:
        # if the client is not in the dictionary, add it
        clients[client_address] = []
    
    if not data:
        # if no data is received, the client has disconnected
        del clients[client_address]
        continue
    
    # append the data to the client's stream
    clients[client_address].append(data)
    
    # send the data to all other clients
    for address in clients:
        if address != client_address:
            for packet in clients[client_address]:
                sock.sendto(packet, address)
