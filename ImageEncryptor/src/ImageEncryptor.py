'''
Created on 13 Mar 2016

@author: Janion
'''

import wx
import Image
import os

################################################################################
################################################################################

class Window(wx.Frame):
    
    alpha = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n",
             "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", " ", "#"
             ]
    
    imgTypes = "JPEG Image (*.jpg)|*.jpg|"     \
               "Bitmap Image (*.bmp)|*.bmp|" \
               "All files (*.*)|*.*"
               
    dir = os.getcwd()
    img = None
    maxSize = 700.
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
        menuBar = wx.MenuBar()
        
        menu1 = wx.Menu()
        menu1.Append(101, "Open image")
        menu1.Append(102, "Save image")
        menu1.AppendSeparator()
        menu1.Append(103, "Quit")
        menuBar.Append(menu1, "File")
        
        menu2 = wx.Menu()
        menu2.Append(201, "Add message")
        menu2.Append(202, "Encrypt entire image")
        menu2.AppendSeparator()
        menu2.Append(203, "Reset image")
        menuBar.Append(menu2, "Encrypt")
        
        menu3 = wx.Menu()
        menu3.Append(301, "Read message")
        menu3.Append(302, "Decrypt entire image")
        menu3.AppendSeparator()
        menu3.Append(303, "Reset image")
        menuBar.Append(menu3, "Decrypt")
        
        self.SetMenuBar(menuBar)
        
        self.Bind(wx.EVT_MENU, self.openImage, id=101)
        self.Bind(wx.EVT_MENU, self.encryptMessage, id=201)
        self.Bind(wx.EVT_MENU, self.encryptImage, id=202)
        self.Bind(wx.EVT_MENU, self.decryptMessage, id=301)
        self.Bind(wx.EVT_MENU, self.decryptImage, id=302)
        
################################################################################

    def decryptImage(self, event):
        
        (width, height) = self.img.size
        
        (v, h, d) = self.img.getpixel((width - 1, height - 1))
        
        self.diagonalShift(-d)
        self.horizontalShift(-h)
        self.verticalShift(-v)
        
        self.showImage()
        
################################################################################

    def encryptImage(self, event):
        
        (width, height) = self.img.size
        
        v = 14
        h = 127
        d = 0
        
        self.verticalShift(v)
        self.horizontalShift(h)
        self.diagonalShift(d)
        
        self.img.putpixel((width - 1, height - 1), (v, h, d))
        
        self.showImage()
        
################################################################################
    
    def horizontalShift(self, shift):
        
        size = self.img.size
        newImg = Image.new('RGB', size, "black")
         
        xShift = shift
        for y in xrange(size[1]):
            for x in xrange(size[0]):
                oldColour = self.img.getpixel((x, y))
                xx = (x + xShift) % size[0]
                if xx < 0:
                    xx += size[10]
                newImg.putpixel((xx, y), oldColour)
            xShift += shift
         
        self.img = newImg
        
################################################################################
    
    def verticalShift(self, shift):
        
        size = self.img.size
        newImg = Image.new('RGB', size, "black")
          
        yShift = shift
        for x in xrange(size[0]):
            for y in xrange(size[1]):
                oldColour = self.img.getpixel((x, y))
                yy = (y + yShift) % size[1]
                if yy < 0:
                    yy += size[1]
                newImg.putpixel((x, yy), oldColour)
            yShift += shift
          
        self.img = newImg
        
################################################################################
    
    def diagonalShift(self, shift):
        
        size = self.img.size
        # TODO do the maths
        
#         diags = []
#         
#         for yy in xrange(size[1] - 1, -1, -1):
#             diag = []
#             x = 0
#             y = yy
#             while(x < size[0] and y < size[1]):
#                 diag.append((x, y))
#                 x += 1
#                 y += 1
#             diags.append(diag)
#         
#         for xx in xrange(1, size[0]):
#             diag = []
#             x = xx
#             y = 0
#             while(x < size[0] and y < size[1]):
#                 diag.append((x, y))
#                 x += 1
#                 y += 1
#             diags.append(diag)
#                 
#         newImg = Image.new('RGB', size, "black")
#           
#         for x in xrange(size[0]):
#             for y in xrange(size[1]):        
#                 oldColour = self.img.getpixel((x, y))
#                  
#                 for diag in diags:
#                     if (x, y) in diag:
#                         (xx, yy) = diag[(diag.index((x, y)) + shift) % len(diag)]
#                 
#                 newImg.putpixel((xx, yy), oldColour)
#           
#         self.img = newImg
        
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

        dlg.Destroy()
        self.showImage()
        
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
