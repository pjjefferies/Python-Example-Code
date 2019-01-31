# -*- coding: utf-8 -*-
"""
Created on Tue Nov 10 21:58:19 2015

@author: PaulJ
"""

"""
from importlib import reload

from PIL import Image
reload(Image)

image_tiff = Image.open('a_image.tif')
#image_tiff = Image.open('574360 Rev. 06 Sheet 01 - Honda GX 8-Way Power Track.tif')

print(type(image_tiff))

#image_tiff.show() # opens the tiff image. this rainbow color tiff

#import numpy as np
#imarray = np.array(image_tiff)
#print(len(imarray), "x", len(imarray[0]))
#print(imarray)
"""

import wx
import time

def readImage(filename):
    img = wx.Image(filename)
    w = img.GetWidth()
    h = img.GetHeight()
    value = img.GetGreen(w - 10, h - 10)
    return value


#image = "a_image.tif"
image = "574360 Rev. 06 Sheet 01 - Honda GX 8-Way Power Track.tif"
#image = "D:\\horizLines1g4.tif"

t0 = time.clock()
value = readImage(image)
print(time.clock() - t0, "seconds process time")
print("The value in the lower right hand corner is %i" % value)