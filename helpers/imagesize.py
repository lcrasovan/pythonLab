# -*- coding: utf-8 -*-
import urllib
from PIL import ImageFile

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
        
        
    def storeImageInfo(self, filePath, imageData):
        with open(filePath, "a") as myfile:
            myfile.write(imageData)
            return 1