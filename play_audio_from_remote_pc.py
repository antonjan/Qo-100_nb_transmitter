import socket
import pyaudio

# Set up constants
CHUNK = 1024 # Size of each audio chunk (measured in samples)
FORMAT = pyaudio.paInt16 # Audio format (16 bits per sample)
CHANNELS = 1 # Number of audio channels
RATE = 44100 # Sampling rate (samples/second)

# Set up network connection
LISTEN_IP = '192.168.10.218' # Listen to all incoming connections
LISTEN_PORT = 12345 # Choose a port number that is not used by other applications
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((LISTEN_IP, LISTEN_PORT))
sock.listen(1)
conn, addr = sock.accept()

# Set up audio playback stream
p = pyaudio.PyAudio()
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                output=True,
                frames_per_buffer=CHUNK)

# Begin audio streaming
print(f"Receiving audio from {addr[0]}...")
while True:
    data = conn.recv(CHUNK)
    stream.write(data) # Play received audio data
