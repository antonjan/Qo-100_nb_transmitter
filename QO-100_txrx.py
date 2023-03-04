#!/usr/bin/env python
"""
Hello World, but with more meat.
"""

import wx
import wx.html
import wx.adv
#import webbrowser
#from rtlsdr import *
#from numpy import *
import time
from pylab import *

class MainFrame(wx.Frame):
    """
    Main frame
    """

    def __init__(self, parent, title):
        # ensure the parent's __init__ is called
        super(MainFrame, self).__init__(parent, title=title, size=(1000, 700))
#        super(Example, self).__init__(parent, title=title, size=(650, 250))
#        flags = wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX)
#        super().__init__(None, title='Qo-100 TXRX', style=flags, size=wx.Size(1800, 900))
        # create a panel in the frame
        self.Centre()
        pnl = wx.Panel(self,size=(800,600))
        
        # adding TX button
        txButton = wx.Button(pnl, label='TX', pos=(150, 20))
        txButton.Bind(wx.EVT_BUTTON, self.OnTX)
        rxButton = wx.Button(pnl, label='RX', pos=(150, 60))
        rxButton.Bind(wx.EVT_BUTTON, self.OnRX)
        self.SetSize((350, 250))
        self.SetTitle('wx.Button')
        self.Centre()
        #Adding TX frequency
        wx.StaticBox(pnl, label='TX Info', pos=(5, 5), size=(280, 170))
        wx.StaticText(pnl, label='Audio Input', pos=(15, 30))
#        wx.CheckBox(pnl, label='1khz tone', pos=(15, 30))
#        wx.CheckBox(pnl, label='Wav file', pos=(15, 55))
#        wx.CheckBox(pnl, label='Mic', pos=(15, 75))
        self.rb1 = wx.RadioButton(pnl, label='1khz tone', pos=(15, 50))
        self.rb2 = wx.RadioButton(pnl, label='Wav file', pos=(15, 70))
        self.rb3 = wx.RadioButton(pnl, label='Mic', pos=(15, 90))
        self.rbtx = wx.RadioButton(pnl, label='TX ON', pos=(90, 90))
        self.rb1.Bind(wx.EVT_RADIOBUTTON, self.SetVal)
        self.rb2.Bind(wx.EVT_RADIOBUTTON, self.SetVal)
        self.rb3.Bind(wx.EVT_RADIOBUTTON, self.SetVal)
        self.rbtx.Bind(wx.EVT_RADIOBUTTON, self.SetVal)
        wx.StaticText(pnl, label='TX frequency (Hz)', pos=(15, 110))
        wx.SpinCtrl(pnl, value='2450500', pos=(15, 130), size=(80, -1), min=2400000, max=24100000)
        wx.StaticText(pnl, label='(Hz)', pos=(85, 130))
        slider = wx.Slider(pnl, 5, 6, 1, 10, (120, 130), (110, -1))
        
        btn = wx.Button(pnl, label='Ok', pos=(90, 185), size=(60, -1))

        btn.Bind(wx.EVT_BUTTON, self.OnClose)
        

        self.SetSize((270, 250))
        self.SetTitle('Static box')
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
    def SetVal(self, e):
        
        state1 = str(self.rb1.GetValue())
        state2 = str(self.rb2.GetValue())
        state3 = str(self.rb3.GetValue())
        state4 = str(self.rbtx.GetValue())
        wx.MessageBox(state1,state2,state3,state4)
        
#        self.sb.SetStatusText(state1, 0)
#        self.sb.SetStatusText(state2, 1)
#        self.sb.SetStatusText(state3, 2)  



    def OnClose(self, e):
        
        self.Close(True)     
           

    def OnTX(self, e):

        wx.MessageBox("TX on")
        
    def OnRX(self, e):

        wx.MessageBox("TX off")    


    def doLayout(self):
        ''' Layout the controls by means of sizers. '''

        # A horizontal BoxSizer will contain the GridSizer (on the left)
        # and the logger text control (on the right):
        boxSizer = wx.BoxSizer(orient=wx.HORIZONTAL)
        # A GridSizer will contain the other controls:
        gridSizer = wx.FlexGridSizer(rows=5, cols=2, vgap=10, hgap=10)

        # Prepare some reusable arguments for calling sizer.Add():
        expandOption = dict(flag=wx.EXPAND)
        noOptions = dict()
        emptySpace = ((0, 0), noOptions)
    
        # Add the controls to the sizers:
        for control, options in \
                [(self.nameLabel, noOptions),
                 (self.nameTextCtrl, expandOption),
                 (self.referrerLabel, noOptions),
                 (self.referrerComboBox, expandOption),
                  emptySpace,
                 (self.insuranceCheckBox, noOptions),
                  emptySpace,
                 (self.colorRadioBox, noOptions),
                  emptySpace, 
                 (self.saveButton, dict(flag=wx.ALIGN_CENTER))]:
            gridSizer.Add(control, **options)

        for control, options in \
                [(gridSizer, dict(border=5, flag=wx.ALL)),
                 (self.logger, dict(border=5, flag=wx.ALL|wx.EXPAND, 
                    proportion=1))]:
            boxSizer.Add(control, **options)

        self.SetSizerAndFit(boxSizer)


    def makeMenuBar(self):
        """
        A menu bar is composed of menus, which are composed of menu items.
        This method builds a set of menus and binds handlers to be called
        when the menu item is selected.
        """

        # Make a file menu with Hello and Exit items
        fileMenu = wx.Menu()
        # The "\t..." syntax defines an accelerator key that also triggers
        # the same event
        helloItem = fileMenu.Append(-1, "&Hello...\tCtrl-H",
                "Help string shown in status bar for this menu item")
        fileMenu.AppendSeparator()
        # When using a stock ID we don't need to specify the menu item's
        # label
        exitItem = fileMenu.Append(wx.ID_EXIT)
        
        newItem = fileMenu.Append(-1, "&New...\tCtrl-N", "Creating a New recording file")
        saveItem = fileMenu.Append(-1, "&Save...\tCtrl-S","Saving recorded file")
        openItem = fileMenu.Append(-1, "&Open...\tCtrl-O", "Open exsiting recording")   
        
        # Strat and Stop recording meny
        startMenu = wx.Menu()
        startstopMenu = wx.Menu()
        startItem = startMenu.Append(-1, "&Start...\tCtrl-N", "Start Recording RF signal strenth")
        stopItem = startMenu.Append(-1, "&Stop...\tCtrl-N", "Stop Recording RF signal strenth")
        
        #Map menu
        mapMenu = wx.Menu()
        mapItem = mapMenu.Append(-1, "&Show Map...\tCtrl-N", "Display the Heatmap")     
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
        self.Bind(wx.EVT_MENU, self.OnHello, helloItem)
        self.Bind(wx.EVT_MENU, self.OnExit,  exitItem)
        self.Bind(wx.EVT_MENU, self.OnAbout, aboutItem)
        self.Bind(wx.EVT_MENU, self.OnNew, newItem)
        self.Bind(wx.EVT_MENU, self.OnSave, saveItem)
        self.Bind(wx.EVT_MENU, self.OnOpen, openItem)
#        self.Bind(wx.EVT_MENU, self.OnStart, startItem)
        self.Bind(wx.EVT_MENU, self.OnStop, stopItem)


    def OnExit(self, event):
        """Close the frame, terminating the application."""
        self.Close(True)


    def OnHello(self, event):
        """Say hello to the user."""
        wx.MessageBox("Hello again from wxPython")


    def OnAbout(self, event):
        """Display an About Dialog"""
#        wx.MessageBox("This is a QO-100 Trancever remote application","This an aplicationthat talks to gnuradio via rpcXML to controle a gnuradio tracever.\n The trancever could be a hackRF or an pluto", wx.OK|wx.ICON_INFORMATION)
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
        info.SetName('Remote TXRX')
        info.SetVersion('0.1')
        info.SetDescription(description)
        info.SetCopyright('(C) 2007 - 2023 Giga Technology PTY. Ltd')
        info.SetWebSite('https://www.giga.co.za/ocart')
        info.SetLicence(licence)
        info.AddDeveloper('Anton Janovsky ZR6AIC')
        info.AddDocWriter('Anton Janovsky ZR6AIC')
        info.AddArtist('----')
        info.AddTranslator('----')

        wx.adv.AboutBox(info)
    def OnNew(self, event):
        """New file dialog box."""
        wx.MessageBox("New file dialog box")
      
    def OnSave(self, event):
        """Save file dialog box."""
        wx.MessageBox("Save file dialog box")
        
    def OnOpen(self, event):
        """Open file dialog box."""
        wx.MessageBox("Open file dialog box")
        

    def OnStop(self, event):
        """Stop recording rtl power measurmrnts."""
        sdr.read_samples_async()
#       wx.MessageBox("Stop recording rtl Power Measurements")            
        
#    def OnAboutBox(self, e):


 
         
        
if __name__ == '__main__':
    # When this module is run (not imported) then create the app, the
    # frame, show it, and start the event loop.
      app = wx.App()
      frm = MainFrame(None, title='Geo Heatmap recorder')
#    frm = MyHtmlFrame(None, "Simple HTML File Viewer")  
      frm.Show()
      app.MainLoop()
