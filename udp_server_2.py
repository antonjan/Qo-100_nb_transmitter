# Welcome to PyShine
# This is client code to receive video and audio frames over UDP

import socket
import threading, wave, pyaudio, time, queue

host_name = socket.gethostname()
host_ip = '127.0.0.1'#  socket.gethostbyname(host_name)
print(host_ip)
port = 9633
# For details visit: www.pyshine.com
q = queue.Queue(maxsize=2000)
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100

def audio_stream_UDP():
	BUFF_SIZE = 65536
	client_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
	client_socket.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,BUFF_SIZE)
	p = pyaudio.PyAudio()
	CHUNK = 10*1024
	stream = p.open(format=FORMAT,
                    channels = CHANNELS,
                    rate = RATE,
                    output = True,
                    frames_per_buffer = CHUNK,
                    )
					
	# create socket
	#message = b'Hello'
	#client_socket.sendto(message,(host_ip,port))
	#socket_address = (host_ip,port)
	
	def getAudioData():
		while True:
			frame,_= client_socket.recvfrom(BUFF_SIZE)
			q.put(frame)
			print('Queue size...',q.qsize())
	t1 = threading.Thread(target=getAudioData, args=())
	t1.start()
	time.sleep(5)
	print('Now Playing...')
	while True:
		frame = q.get()
		stream.write(frame)

	client_socket.close()
	print('Audio closed')
	os._exit(1)



t1 = threading.Thread(target=audio_stream_UDP, args=())
t1.start()

