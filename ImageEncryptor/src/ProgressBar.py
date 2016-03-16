'''
Created on 14 Mar 2016

@author: Janion
'''

import wx

class GaugeFrame(wx.MiniFrame):
    def __init__(self, parent, title, maximum):
        wx.MiniFrame.__init__(self, parent, title=title, size=(200, 60) )

        self.bar = wx.Gauge(self, range=maximum)
        self.cancelBtn = wx.Button(self, label="Cancel")

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.bar)
        sizer.Add(self.cancelBtn, flag=wx.CENTER)
        self.SetSizer(sizer)
        self.Fit()

        self.Bind(wx.EVT_BUTTON, self.onCancel, self.cancelBtn)

    def updateGauge(self, value):
        if self.GetTitle() != "Cancelling...":
            self.bar.SetValue(value)
            self.SetTitle("%d%%" % value)

    def onCancel(self, e):
        self.SetTitle("Cancelling...")