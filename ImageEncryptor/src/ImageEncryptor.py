'''
Created on 13 Mar 2016

@author: Janion
'''

# Use pixelArray = Image.load()
# self.img.putdata(pixelArray)
# Maybe don't event need to put data

# Allow user to create key and don't store it in the image
# Faster way to encrypt image?
# Save images
# Split into objects

import wx
import Image
import os
import random
import threading
import numpy as np
from scipy.misc import fromimage
from scipy.misc import toimage

from ProgressBar import GaugeFrame

################################################################################
################################################################################

class Window(wx.Frame):
    
    alpha = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n",
             "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", " ", "#"
             ]
    
    imgTypes = "JPEG Image (*.jpg)|*.jpg|"\
               "Bitmap Image (*.bmp)|*.bmp|"\
               "All files (*.*)|*.*"
               
    dir = os.getcwd()
    img = None
    display = None
    
    def __init__(self, parent, idd, title):
        wx.Frame.__init__(self, parent, idd, title, size=(300, 150))
        self.panel = wx.ScrolledWindow(self)
        self.maxWidth  = 500
        self.maxHeight = 500
        
        self.panel.SetVirtualSize((self.maxWidth, self.maxHeight))
        self.panel.SetScrollRate(20,20)
        
        self.setupMenu()
            
################################################################################
            
    def setupMenu(self):
        self.menuBar = wx.MenuBar()
        
        menu1 = wx.Menu()
        menu1.Append(101, "Open image")
        menu1.Append(102, "Save image")
        menu1.AppendSeparator()
        menu1.Append(103, "Quit")
        self.menuBar.Append(menu1, "File")
        
        menu2 = wx.Menu()
        menu2.Append(201, "Add message")
        menu2.Append(202, "Encrypt entire image")
        menu2.AppendSeparator()
        menu2.Append(203, "Reset image")
        self.menuBar.Append(menu2, "Encrypt")
        
        menu3 = wx.Menu()
        menu3.Append(301, "Read message")
        menu3.Append(302, "Decrypt entire image")
        menu3.AppendSeparator()
        menu3.Append(303, "Reset image")
        self.menuBar.Append(menu3, "Decrypt")
        
        self.SetMenuBar(self.menuBar)
        
        self.Bind(wx.EVT_MENU, self.openImage, id=101)
        self.Bind(wx.EVT_MENU, self.threadyThreadMaster, id=102)
        self.Bind(wx.EVT_MENU, self.encryptMessage, id=201)
        self.Bind(wx.EVT_MENU, self.encryptImage, id=202)
        self.Bind(wx.EVT_MENU, self.decryptMessage, id=301)
        self.Bind(wx.EVT_MENU, self.decryptImage, id=302)
        
################################################################################

    def threadyThreadMaster(self, event):
        
        self.progressDlg = GaugeFrame(self, title="0%", maximum=100)
        self.progressDlg.Show()
        self.progressDlg.Center()
        workThread = threading.Thread(target=self.threadyThread, args=() )
        workThread.start()
        
################################################################################
    
    def iterator(self, data, positions, x, pc):
        updated = False
        for y in xrange(len(data)):
            (xx, yy) = positions[y]
            (R, G, B) = data[y]
              
            if ((x + y) % 3) == 0:
                oldColour = (R, G, B)
            elif ((x + y) % 3) == 1:
                oldColour = (G, B, R)
            else:
                oldColour = (B, R, G)

            self.newData[yy, xx] = oldColour
            
            if float(y) / len(data) > pc and not updated:
                updated = True
                wx.CallAfter(self.progressDlg.updateGauge, int(float(100 * y) / len(data)))
            
            if self.progressDlg.GetTitle() == "Cancelling...":
                break
        
        self.tCount += 1
        
################################################################################
    
    def threadyThread(self):
         
        size = self.img.size
        data = fromimage(self.img)
        self.newData = np.zeros((size[1], size[0], 3))
         
        (r, g, b) = (5, 13, 31)
        seed = int(str(r) + str(g) + str(b))
        random.seed(seed)
        self.tCount = 0
         
        positions = []
        for x in xrange(size[0]):
            for y in xrange(size[1]):
                positions.append((x, y))
         
        for x in xrange(size[0]):
            
            randPositions = []
            for z in xrange(size[1]):
                randPositions.append(positions.pop(random.randint(0, len(positions) - 1)))
            workThread = threading.Thread(target=self.iterator, args=(data[:,x], randPositions, x, float(x)/size[0]) )
            workThread.start()
            if self.progressDlg.GetTitle() == "Cancelling...":
                break
            
        while self.tCount < size[0]:
            if self.progressDlg.GetTitle() == "Cancelling...":
                break

        if self.progressDlg.GetTitle() != "Cancelling...":
            self.img = toimage(self.newData)
            self.img.putpixel((size[0] - 1, size[1] - 1), (r, g, b))
            wx.CallAfter(self.showImage)
            
        wx.CallAfter(self.progressDlg.Destroy)
        
################################################################################
    
    def randomHashThread(self):
         
        size = self.img.size
        data = fromimage(self.img)
        newData = np.zeros((size[1], size[0], 3))
         
        (r, g, b) = (5, 13, 31)
        seed = int(str(r) + str(g) + str(b))
        random.seed(seed)
         
        positions = []
        for x in xrange(size[0]):
            for y in xrange(size[1]):
                positions.append((x, y))
         
        for x in xrange(size[0]):
            print x
            for y in xrange(size[1]):
                (xx, yy) = positions.pop(random.randint(0, len(positions) - 1))
                (R, G, B) = data[y, x]
                  
                if ((x + y) % 3) == 0:
                    oldColour = (R, G, B)
                elif ((x + y) % 3) == 1:
                    oldColour = (G, B, R)
                else:
                    oldColour = (B, R, G)
                       
                newData[yy, xx] = oldColour
                 
                if self.progressDlg.GetTitle() == "Cancelling...":
                    break
             
            wx.CallAfter(self.progressDlg.updateGauge, int(float(100 * x) / size[0]))
            if self.progressDlg.GetTitle() == "Cancelling...":
                break
         
        if not self.progressDlg.GetTitle() == "Cancelling...":
            self.img = toimage(newData)
            self.img.putpixel((size[0] - 1, size[1] - 1), (r, g, b))
            wx.CallAfter(self.showImage)
        
        wx.CallAfter(self.progressDlg.Destroy)
        
################################################################################
    
#     def randomHashThread(self):
#          
#         size = self.img.size
#         newImg = Image.new('RGB', size, "black")
# #         pxlMap = self.img.load()
# #         newp = [0] * size[0] * size[1]
#          
#         (r, g, b) = (5, 13, 31)
#         seed = int(str(r) + str(g) + str(b))
#         random.seed(seed)
#          
#         positions = []
#          
#         for x in xrange(size[0]):
#             for y in xrange(size[1]):
#                 positions.append((x, y))
#          
#         for x in xrange(size[0]):
#             print x
#             for y in xrange(size[1]):
#                 (xx, yy) = positions.pop(random.randint(0, len(positions) - 1))
#                 (R, G, B) = self.img.getpixel((x, y))
# #                 (R, G, B) = pxlMap[x, y]
#                   
#                 if ((x + y) % 3) == 0:
#                     oldColour = (R, G, B)
#                 elif ((x + y) % 3) == 1:
#                     oldColour = (G, B, R)
#                 else:
#                     oldColour = (B, R, G)
#                       
#                 newImg.putpixel((xx, yy), oldColour)
# #                 newp[xx + yy * size[0]] = oldColour
#                  
#                 if self.progressDlg.GetTitle() == "Cancelling...":
#                     break
#              
#             wx.CallAfter(self.progressDlg.updateGauge, int(float(100 * x) / size[0]))
#             if self.progressDlg.GetTitle() == "Cancelling...":
#                 break
#          
#         if not self.progressDlg.GetTitle() == "Cancelling...":
# #             newImg.putdata(newp)
#             newImg.putpixel((size[0] - 1, size[1] - 1), (r, g, b))
#             self.img = newImg
#             wx.CallAfter(self.showImage)
#         
#         wx.CallAfter(self.progressDlg.Destroy)
        
################################################################################
    
    def randomDehashThread(self):
        
        size = self.img.size
        newImg = Image.new('RGB', size, "black")
        
        (r, g, b) = self.img.getpixel((size[0] - 1, size[1] - 1))
        seed = int(str(r) + str(g) + str(b))
        random.seed(seed)
        
        positions = []
        
        for x in xrange(size[0]):
            for y in xrange(size[1]):
                positions.append((x, y))
        
        for x in xrange(size[0]):
            for y in xrange(size[1]):
                (xx, yy) = positions.pop(random.randint(0, len(positions) - 1))
                    
                (R, G, B) = self.img.getpixel((xx, yy))
                
                if ((x + y) % 3) == 0:
                    oldColour = (R, G, B)
                elif ((x + y) % 3) == 1:
                    oldColour = (B, R, G)
                else:
                    oldColour = (G, B, R)
                
                newImg.putpixel((x, y), oldColour)
                
                if self.progressDlg.GetTitle() == "Cancelling...":
                    break
            wx.CallAfter(self.progressDlg.updateGauge, int(float(100 * x) / size[0]))
            if self.progressDlg.GetTitle() == "Cancelling...":
                break
        
        if not self.progressDlg.GetTitle() == "Cancelling...":
            wx.CallAfter(self.progressDlg.Destroy)
            self.img = newImg
            wx.CallAfter(self.showImage)
        else:
            wx.CallAfter(self.progressDlg.Destroy)
        
################################################################################

    def decryptImage(self, event):
        
        self.progressDlg = GaugeFrame(self, title="0%", maximum=100)
        self.progressDlg.Show()
        self.progressDlg.Center()
        workThread = threading.Thread(target=self.randomDehashThread, args=() )
        workThread.start()
        
################################################################################

    def encryptImage(self, event):
        
        self.progressDlg = GaugeFrame(self, title="0%", maximum=100)
        self.progressDlg.Show()
        self.progressDlg.Center()
        workThread = threading.Thread(target=self.randomHashThread, args=() )
        workThread.start()
        
################################################################################

    def decryptMessage(self, event):
        
        (width, height) = self.img.size
        area = height * width
        
        string = ""
        
        (offset, period, multiplier) = self.img.getpixel( (width - 1, height - 1) )
        gap = period * multiplier
                 
        for pos in xrange(gap, area, gap):
            x = (pos) % width
            y = (pos) / width
            (r, g, b) = self.img.getpixel((x, y))
            (R, G, B) = ((r - offset) % len(self.alpha), (g - offset) % len(self.alpha), (b - offset) % len(self.alpha))
            
            try:
                string += self.alpha[R]
            except:
                R = R
            
            try:
                string += self.alpha[G]
            except:
                G = G
            
            try:
                string += self.alpha[B]
            except:
                B = B
            
            if "#" in string:
                string = string[0 : string.index("#")]
                break

        dlg = wx.MessageDialog(self, string,
                               'Decrypted message',
                               wx.OK | wx.ICON_INFORMATION
                               )
        dlg.ShowModal()
        dlg.Destroy()
        
################################################################################

    def encryptMessage(self, event):
        
        offset = 12
        period = 237
        multiplier = 53
        
        dlg = wx.TextEntryDialog(
                self, 'Please enter a message to be encrypted',
                'Encrypt message', '')

        if dlg.ShowModal() == wx.ID_OK:
            string = dlg.GetValue().lower() + "#"
            (width, height) = self.img.size
            gap = period * multiplier
                     
            for pos in xrange(0, len(string), 3):
                x = (((gap * (pos + 3)) / 3)) % width
                y = (((gap * (pos + 3)) / 3)) / width
                (r, g, b) = self.img.getpixel((x, y))
                (R, G, B) = (r - (r % len(self.alpha)), g - (g % len(self.alpha)), b - (b % len(self.alpha)))
                
                try:
                    R += self.alpha.index(string[pos]) + offset
                    if R > 255:
                        R -= len(self.alpha)
                except:
                    R = R
                
                try:
                    G += self.alpha.index(string[pos + 1]) + offset
                    if G > 255:
                        G -= len(self.alpha)
                except:
                    G = G
                
                try:
                    B += self.alpha.index(string[pos + 2]) + offset
                    if B > 255:
                        B -= len(self.alpha)
                except:
                    B = B
    
                self.img.putpixel( (x, y), (R, G, B))
            
            
            self.img.putpixel( (width - 1, height - 1), (offset, period, multiplier))
            self.showImage()
        dlg.Destroy()
        
################################################################################

    def openImage(self, event):
        dlg = wx.FileDialog(
            self, message="Choose a file",
            defaultDir=self.dir, 
            defaultFile="",
            wildcard=self.imgTypes,
            style=wx.OPEN
            )

        # Show the dialog and retrieve the user response. If it is the OK response, 
        # process the data.
        if dlg.ShowModal() == wx.ID_OK:
            # This returns a Python list of files that were selected.
            paths = dlg.GetPaths()
            self.img = Image.open(paths[0])
            self.showImage()

        dlg.Destroy()
        
################################################################################

    def showImage(self):
        
        self.panel.Scroll(0, 0)
        
        bmp = self.pilImageToWxBitmap(self.img)

#         width = bmp.GetWidth()
#         height = bmp.GetHeight()
#          
#         if width > height:
#             scale = self.maxSize / width
#         else:
#             scale = self.maxSize / height
#      
#         scale = 0.5
#  
#         image = wx.ImageFromBitmap(bmp)
#         image = image.Scale(width * scale, height * scale, wx.IMAGE_QUALITY_HIGH)
#         bmp = wx.BitmapFromImage(image)
        
        if self.display != None:
            self.display.Destroy()
        self.display = wx.StaticBitmap(self.panel, -1, bmp, pos=(10, 10))
        self.panel.SetVirtualSize(bmp.GetSize())
        
################################################################################
################################################################################
        
    def wxBitmapToPilImage( self, myBitmap ):
        return self.wxImageToPilImage( self.wxBitmapToWxImage( myBitmap ) )
        
################################################################################

    def wxBitmapToWxImage( self, myBitmap ):
        return wx.ImageFromBitmap( myBitmap )
        
################################################################################

    def pilImageToWxBitmap(self, myPilImage):
        return self.wxImageToWxBitmap(self.pilImageToWxImage(myPilImage))
        
################################################################################
    
    def pilImageToWxImage(self, myPilImage):
        myWxImage = wx.EmptyImage(myPilImage.size[0], myPilImage.size[1])
        myWxImage.SetData(myPilImage.convert('RGB').tostring())
        return myWxImage
        
################################################################################
    
    def wxImageToWxBitmap( self, myWxImage ):
        return myWxImage.ConvertToBitmap()
        
################################################################################
################################################################################



if __name__ == '__main__':
    app = wx.App()
    fr = Window(None, -1, 'Image encryptor')
    fr.Show()
    app.MainLoop()
