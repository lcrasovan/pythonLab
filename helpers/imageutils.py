# -*- coding: utf-8 -*-
import urllib
from PIL import ImageFile, Image, ImageOps
import os

class ImageUtils:
    
    def getImageSizes(slf, uri):
        file = urllib.urlopen(uri)
        size = file.headers.get("content-length")
        if size:
            size = int(size)
        p = ImageFile.Parser()
        while 1:
            data = file.read(1024)
            if not data:
                break
            p.feed(data)
            if p.image:
                return size, p.image.size
                break
        file.close()
        return size, None
        
    def downloadImage(slf, uri, filePath):
        with open(filePath,'wb') as file:
            file.write(urllib.urlopen(uri).read())
            return 1
        
    def storeImageInfo(self, filePath, imageData):
        with open(filePath, "a") as myfile:
            myfile.write(imageData)
            return 1
            
    def createCrop(self, srcImagePath, destImagePath, zoomLevel, width, height):
        originalImg = Image.open(srcImagePath)
        halfOriginaWidth = originalImg.size[0] / 2
        halfOriginalHeight = originalImg.size[1] / 2
        tempImage = originalImg.crop((halfOriginaWidth - width/2 * zoomLevel, halfOriginalHeight - height/2 * zoomLevel, halfOriginaWidth + width/2 * zoomLevel, halfOriginalHeight + height/2 * zoomLevel))
        thumbnail = ImageOps.fit(tempImage,(width, height),Image.ANTIALIAS)
        thumbnail.save(destImagePath)
        return 1
       
    def createZoomedImages(self, rootDir, srcImagePath):
        for x in xrange(1,5):
            zoomLevel = x
            imageName = os.path.basename(srcImagePath)
            destImagePath = rootDir + '/images/zoom' + str(zoomLevel) + '/' + imageName 
            self.createCrop(srcImagePath, destImagePath, zoomLevel, 280, 186) 
        return 1      