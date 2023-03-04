import socket
import pyaudio
import wave

# Set up constants
CHUNK = 1024 # Size of each audio chunk (measured in bytes)
FORMAT = pyaudio.paInt16 # Audio format (16 bits per sample)
CHANNELS = 1 # Number of audio channels
RATE = 44100 # Sampling rate (samples/second)
WAVE_OUTPUT_FILENAME = "output.wav"

# Set up audio recording stream
p = pyaudio.PyAudio()
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

# Set up network connection
SERVER_IP = '192.168.1.100'
SERVER_PORT = 12345
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((SERVER_IP, SERVER_PORT))

# Begin audio streaming
print("Streaming audio...")
while True:
    data = stream.read(CHUNK)
    sock.sendall(data)

    # Store recorded sound into file
    frames.append(data)

    # Stop streaming after 60 seconds
    if elapsed_time > 60: 
        break

# Create wave file object and write to disk
wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()
