#!/usr/bin/env python
"""
QO-100 Remite interface
sudo modprobe snd-aloop
aplay -l
arecord -l
speaker-test -c2 -D hw:0,0
arecord -D hw:0,1 -f S16_LE -c 2 -r 48000 audio.wav
/etc/asound.conf
#/usr/share/alsa/alsa.conf 
"""
import time
import xmlrpc.client
import wx
import wx.html
import wx.adv
import socket
import pyaudio
import threading
from threading import Thread, Event
from time import sleep
from queue import Queue
import configparser

import time
import wx.lib.masked as masked
from pylab import *
CHUNK = 1024 # Size of each audio chunk (measured in samples)
FORMAT = pyaudio.paInt16 # Audio format (16 bits per sample)
CHANNELS = 1 # Number of audio channels
RATE = 44100 # Sampling rate (samples/second)
audioDevice = 0
maxValue = 2**16
bars = 50
audioInputDevice=[]
audioInterface = 0
frames = []
#port1 = 123456

class MainFrame(wx.Frame):
    """
    Main frame
    """
    def getAudioDeviceList():    
        p = pyaudio.PyAudio()
        for i in range(p.get_device_count()):
           print (p.get_device_info_by_index(i),"\n")
           audioDevice.append(p.get_device_info_by_index(i))
           #audioDevice.Append(i)
           print ("audio list = ",audioDevice)
                      #comboAudio.SetSelection(sel)
           #sizer.Add(comboAudio)
        return audioDevice      


    def __init__(self, parent, title):
        # ensure the parent's __init__ is called
        super(MainFrame, self).__init__(parent, title=title, size=(1000, 700))
        
        self.Centre()
        pnl = wx.Panel(self,size=(800,600))
        
        #Adding TX frequency
        wx.StaticBox(pnl, label='Audio Info', pos=(5, 5), size=(280, 100))
        wx.StaticText(pnl, label='Audio Output device', pos=(15, 30))
        self.comboAudio = wx.SpinCtrl(pnl,-1,"", pos=(15, 50), size=(140, -1))
        self.audioGage = wx.Gauge(pnl, range = 90, pos = (15, 70),size=(230, -1))
        # the TCP connection details
        wx.StaticBox(pnl, label='TCP connection details', pos=(5, 120), size=(280, 160))
        wx.StaticText(pnl, label='TCP Adress', pos=(15, 150))
        wx.StaticText(pnl, label='Port', pos=(205, 150))
        #control = masked.IpAddrCtrl(pnl, pos=(5, 240)) #, mask = '###.###.###.###') #,defaultValue='192.168.010.218')
        self.ipaddr1 = wx.TextCtrl( pnl, -1, pos=(15, 180),size=(170, -1),value="127.0.0.1")
        #self.apaddr1.SetVal(ip)
        self.port1 = masked.TextCtrl( pnl, -1, pos=(205, 180),size=(75, -1),mask = '######' ,defaultValue="12345")
        btn = wx.Button(pnl, label='Start to listen', pos=(15, 220), size=(100, -1))
        btn.Bind(wx.EVT_BUTTON, self.OnStartListen)
        btn2 = wx.Button(pnl, label='Stop listen', pos=(120, 220), size=(100, -1))
        btn2.Bind(wx.EVT_BUTTON, self.OnStopListen)
        self.SetSize((470, 450))
        self.SetTitle('QO-100 Audio Receiver')
        self.Centre()
        self.Show(True)          
        # put some text with a larger bold font on it
        st = wx.StaticText(pnl, label="")
        font = st.GetFont()
        font.PointSize += 3
        font = font.Bold()
        st.SetFont(font)
        
        # and create a sizer to manage the layout of child widgets
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(st, wx.SizerFlags().Border(wx.TOP|wx.LEFT, 50))
        pnl.SetSizer(sizer)

        # create a menu bar
        self.makeMenuBar()

        # and a status bar
        self.CreateStatusBar()
        self.SetStatusText("Welcome to Qo-100 TXRX!")
#        form2 = FormWithSizer(notebook)
        config = configparser.RawConfigParser() 
        try:
           print ("loading config file")  
           configFilePath = r'qo-100rx.conf'
           config.read(configFilePath)
           ip = config.get('qo-100rx', 'ip')
           self.ipaddr1.SetValue(ip)
           port = config.get('qo-100rx', 'port')
           self.port1.SetValue(port)
           mic = config.get('qo-100rx', 'audio_channel')
           ptt = config.get('qo-100rx', 'ptt')
           logfile = config.get('qo-100rx', 'logfile')
        except configparser.NoSectionError:
           print("No qo-100tx.conf file found. Please create config file in home directory")
           exit()   
    def SetVal(self, e):
        
        state1 = str(self.rb1.GetValue())
        state2 = str(self.rb2.GetValue())
        state3 = str(self.rb3.GetValue())
        state4 = str(self.rbtx.GetValue())
        wx.MessageBox(state1,state2,state3,state4)
        

    def OnClose(self, e):
        
        self.Close(True)     
           

    def OnStartListen(self, e):
        print ("do noting")
        
    def OnStopListen(self, e):
        event.set() # stop the thread
        print("stop Listening for stream")
        #wx.MessageBox("TX on")
       
      
        

    

    def makeMenuBar(self):
        """
        A menu bar is composed of menus, which are composed of menu items.
        This method builds a set of menus and binds handlers to be called
        when the menu item is selected.
        """

        # Make a file menu with Hello and Exit items
        fileMenu = wx.Menu()
        fileMenu.AppendSeparator()
        # When using a stock ID we don't need to specify the menu item's
        # label
        exitItem = fileMenu.Append(wx.ID_EXIT)
        saveItem = fileMenu.Append(-1, "&Save...\tCtrl-S","Saving configeration")
               
        # Now a help menu for the about item
        helpMenu = wx.Menu()
        aboutItem = helpMenu.Append(wx.ID_ABOUT)

        # Make the menu bar and add the two menus to it. The '&' defines
        # that the next letter is the "mnemonic" for the menu item. On the
        # platforms that support it those letters are underlined and can be
        # triggered from the keyboard.
        menuBar = wx.MenuBar()
        
        menuBar.Append(fileMenu, "&File")
#        menuBar.Append(startMenu,"Start/Stop")
#        menuBar.Append(mapMenu,"Heatmap")
        menuBar.Append(helpMenu, "&Help")
        
        

        # Give the menu bar to the frame
        self.SetMenuBar(menuBar)

        # Finally, associate a handler function with the EVT_MENU event for
        # each of the menu items. That means that when that menu item is
        # activated then the associated handler function will be called.
        self.Bind(wx.EVT_MENU, self.OnExit,  exitItem)
        self.Bind(wx.EVT_MENU, self.OnAbout, aboutItem)
        self.Bind(wx.EVT_MENU, self.OnSave, saveItem)
        


    def OnExit(self, event):
        """Close the frame, terminating the application."""
        self.Close(True)


    def OnAbout(self, event):
        """Display an About Dialog"""
#        wx.MessageBox("This is a QO-100 Audio Recever application","This an aplication that takes the audio stream and send it to Audio loop back device for Gnuradio to transmit it to the satellite)
        description = """This application allows you to send Mic audio to QO-100 raspberry py aplication"""

        licence = """This is free software; you can redistribute it and/or modify
         it under the terms of the GNU General Public License as published by the
          Free Software Foundation; either version 2 of the License,
        or (at your option) any later version.

        QO-100 is distributed in the hope that it will be useful,
        but WITHOUT ANY WARRANTY; without even the implied warranty of
        MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
        See the GNU General Public License for more details. You should have
        received a copy of the GNU General Public License along with Giga Technology;
        if not, write to the Free Software Foundation, Inc., 59 Temple Place,
        Suite 330, Boston, MA  02111-1307  USA"""


        info = wx.adv.AboutDialogInfo()

        info.SetIcon(wx.Icon('Giga_Technology.png', wx.BITMAP_TYPE_PNG))
        info.SetName('Audio Streame Recever TXRX')
        info.SetVersion('0.1')
        info.SetDescription(description)
        info.SetCopyright('(C) 2007 - 2023 Giga Technology PTY. Ltd')
        info.SetWebSite('https://www.giga.co.za/ocart')
        info.SetLicence(licence)
        info.AddDeveloper('Anton Janovsky ZR6AIC')
        info.AddDocWriter('----')
        info.AddArtist('----')
        info.AddTranslator('----')

        wx.adv.AboutBox(info)
    def OnNew(self, event):
        """New file dialog box."""
        wx.MessageBox("New file dialog box")
      
    def OnSave(self, event):
        """Save file dialog box."""
        wx.MessageBox("Save file dialog box")
        
    def OnConnect(self,event):
        """Connect to host to send Mic Audio"""
        wx.MessageBox("Connecting to host")
        
    def OnSliderScroll(self,event):
        res = self.frequency.GetValue()
        assert isinstance(res, int)
        obj = event.GetEventObject() 
        val = obj.GetValue()
        self.frequency.SetValue(res + val) 
        print (val + res )     
        
           
        
    

#def udpStream(CHUNK,ipaddr1,port1):
def udpStream(CHUNK):
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    port =  int(port1)
    #ipaddr = ipaddr1
    try:
        udp.bind((ipaddr1,port))
    except OSError: # [Errno 98] Address already in use
        print ("[Errno 98] Address already in use port is already in use please stop application using this port or change the port")    
    #udp.bind((ipaddr,port))
    while True:
        soundData, addr = udp.recvfrom(CHUNK*CHANNELS*2)
        frames.append(soundData)
        print("receiving audio...", end='\r')
    udp.close()

def play(stream, CHUNK):
    BUFFER = 10
    
    while True:
        try:
            if len(frames) == BUFFER:
                while True:
                    stream.write(frames.pop(0), CHUNK)
        except IndexError:
              print("No Stream connection, Wating for connection")
        
                 
        
if __name__ == '__main__':
    app = wx.App()
    frm = MainFrame(None, title='QO-100 TX')
    # create a new Worker thread
    #threadStreem = WorkerStreamming(event)
    # start the thread
      
    #    frm = MyHtmlFrame(None, "Simple HTML File Viewer")  
    frm.Show()
    pnl = wx.Panel()
    print("start Listening stream")
    # create a new Worker thread
    #audioInterface = self.comboAudio.GetValue()
    #print("audio device = " , audioInterface)
    FORMAT = pyaudio.paInt16
    CHUNK = 1024
    CHANNELS = 2
    RATE = 44100
    ipaddr1 = frm.ipaddr1.GetValue()
    #ipaddr1 = "127.0.0.1"
    #port1 = 12345
    print( "ip =", ipaddr1)
    port1 = frm.port1.GetValue()
    print (" port = ",port1)
    Audio = pyaudio.PyAudio()
    stream = Audio.open(format=FORMAT,
                    channels = CHANNELS,
                    rate = RATE,
                    output = True,
                    frames_per_buffer = CHUNK,
                    )
    print("--1--")
    #udpThread  = Thread(target = udpStream, args=(CHUNK,ipaddr1,port1))
    udpThread  = Thread(target = udpStream, args=(CHUNK,))
    AudioThread  = Thread(target = play, args=(stream, CHUNK,))
    udpThread .setDaemon(True)
    AudioThread.setDaemon(True)
    udpThread .start()
    AudioThread.start()
    print ("Listening for stream")
    #udpThread .join()
    #AudioThread.join()
    print ("--2--")
    app.MainLoop()
