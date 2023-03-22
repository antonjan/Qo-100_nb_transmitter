import socket
import pyaudio

# Initialize socket and PyAudio
UDP_IP = '127.0.0.1'  # IP address of receiver
UDP_PORT = 5005
BUFFER_SIZE = 1024
audio = pyaudio.PyAudio()

# Open microphone stream
stream = audio.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=BUFFER_SIZE)

# Initialize UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Stream audio data
while True:
    data = stream.read(BUFFER_SIZE)
    sock.sendto(data, (UDP_IP, UDP_PORT))
