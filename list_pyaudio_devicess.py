#pip install sounddevice --user
#python -m sounddevice
import pyaudio
p = pyaudio.PyAudio()
for i in range(p.get_device_count()):
    print (p.get_device_info_by_index(i),"\n")
