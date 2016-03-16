'''
Created on 16 Mar 2016

@author: Janion
'''

import Image
import numpy as np
from scipy.misc import fromimage
from scipy.misc import toimage
from time import time as now

filename = "C:\\Users\\Janion\\Downloads\\26137_384168686572_4355361_n (2).jpg"
filename = "C:\\Users\\Janion\\Downloads\\26137_384168686572_4355361_n.jpg"

if __name__ == '__main__':
    im = Image.open(filename)
    data = fromimage(im)
    
    size = im.size
    
    t1 = now()
    
    for z in xrange(20):
        dummy = np.zeros((size[0], size[1], 3))
        for x in xrange(size[1]):
            for y in xrange(size[0]):
                dummy[y, x] = data[x, y]
        newImg = toimage(dummy)
    
    print "Numpy", now() - t1
    
    t1 = now()
    
    for z in xrange(20):
        dummy = []
        for x in xrange(size[1]):
            for y in xrange(size[0]):
                dummy.append(im.getpixel((y, x)))
    
        newImg = Image.new("RGB", (size[0]*3, size[1]*3), "black")
        newImg.putdata(dummy)
    print "putdata", now() - t1
    
    t1 = now()
    
    for z in xrange(20):
        newImg = Image.new("RGB", (size[0]*3, size[1]*3), "black")
        for x in xrange(size[1]):
            for y in xrange(size[0]):
                newImg.putpixel((y, x), im.getpixel((y, x)))
    print "putpixel", now() - t1
    
    t1 = now()
    
    for z in xrange(20):
        dummy =[[0] * size[1]] * size[0]
        for x in xrange(size[1]):
            for y in xrange(size[0]):
                dummy[y][x] = data[x, y]
        newImg = toimage(dummy)
    
    print "Tuple", now() - t1
    
    
    
    
    
    
    
    
    
    
    
    
    