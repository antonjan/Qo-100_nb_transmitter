import socket
import pyaudio

# Set up constants
CHUNK = 1024 # Size of each audio chunk (measured in samples)
FORMAT = pyaudio.paInt16 # Audio format (16 bits per sample)
CHANNELS = 1 # Number of audio channels
RATE = 44100 # Sampling rate (samples/second)
WAVE_OUTPUT_FILENAME = "/home/anton/bacar_sstv.wav" # Output file name

# Set up audio recording stream
p = pyaudio.PyAudio()
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

# Set up network connection
SERVER_IP = '192.168.10.218' # Replace with the IP address of remote machine
SERVER_PORT = 12345 # Choose a port number that is not used by other applications
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((SERVER_IP, SERVER_PORT))

# Begin audio streaming
print("Streaming audio...")
while True:
#    data = stream.read(CHUNK,exception_on_overflow = False)
    data = stream.read(CHUNK)
    sock.sendall(data) # Send audio data to remote machine
