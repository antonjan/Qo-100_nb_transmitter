import socket
import pyaudio

# create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# set the server address and port
server_address = ('localhost', 10000)

# create a PyAudio object
p = pyaudio.PyAudio()

# set the audio format
FORMAT = pyaudio.paInt16

# set the number of channels
CHANNELS = 1

# set the sampling rate
RATE = 44100

# set the buffer size
CHUNK = 1024

# open the audio stream
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                output=True,
                frames_per_buffer=CHUNK)

# send a connection message to the server
sock.sendto(b'connect', server_address)

while True:
    # receive data from the server
    data, server_address = sock.recvfrom(1024)
    
    if not data:
        # if no data is received, the server has disconnected
        break
    
    # play the audio data
    stream.write(data)
    
# close the audio stream and PyAudio object
stream.stop_stream()
stream.close()
p.terminate()
