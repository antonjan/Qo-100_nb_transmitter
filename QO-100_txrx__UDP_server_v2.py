import socket
import pyaudio
import time

# Initialize socket and PyAudio
UDP_IP = '127.0.0.1'
UDP_PORT = 5005
BUFFER_SIZE = 1024
audio = pyaudio.PyAudio()

# Initialize UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

# Open speaker stream
stream = audio.open(format=pyaudio.paInt16, channels=1, rate=44100, output=True)

# Receive and play audio data
while True:
    try:
        data, addr = sock.recvfrom(BUFFER_SIZE)
        stream.write(data)
    except socket.error:
        # Handle connection error
        print('Connection lost. Retrying in 5 seconds...')
        time.sleep(5)
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((UDP_IP, UDP_PORT))

