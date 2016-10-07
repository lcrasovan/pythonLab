# -*- coding: utf-8 -*-
import ConfigParser
import pandas as pd
import urllib
from PIL import ImageFile
from sqlalchemy import create_engine
import os

def createFolderPath(path):
    os.makedirs(path)
    return 1

def downloadImage(uri, localPath):
    return 1
    
def storeImageInfo(filePath, imageData):
    with open(filePath, "a") as myfile:
        myfile.write(imageData)
    return 1    

def getImageSizes(uri):
    file = urllib.urlopen(uri)
    size = file.headers.get("content-length")
    if size: size = int(size)
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

config = ConfigParser.ConfigParser()
config.read("/Users/restoin/projects/pythonLab/settings.ini")

userName = config.get('MySqlSection','user')
password = config.get('MySqlSection','password')
hostname = config.get('MySqlSection','host')
database = config.get('MySqlSection','database')
charset = config.get('MySqlSection','charset')
urlAmazonS3 = config.get('AWS','urlAmazonS3')
minWidth = int(config.get('images','minWidth'))
query = config.get('Repository','findImagesByCityAndProvider')

connectionString = 'mysql+pymysql://' + userName + ':' + password + '@' + hostname + '/' + database + '?charset=' + charset  

engine = create_engine(connectionString)

dataFrame = pd.read_sql_query(query,engine)

for index, row in dataFrame[6001:8000].iterrows():
    correctedImageName = row['imageName'].encode('utf-8')
    print correctedImageName
    fileSize, dimensions = getImageSizes(urlAmazonS3 + correctedImageName)
    print fileSize, dimensions
    if dimensions and dimensions[0]: 
        if int(dimensions[0]) < minWidth:
            filePath = 'data/paris/' + row['restaurant'] + '.csv'
            if not os.path.isfile(filePath):
                header = 'ProductId,ProductName,ImageId,ImageFile' + '\r\n'
                storeImageInfo(filePath, header)    
            photoInfo = str(row['productId']) + ',' + row['productName'].encode('utf-8') + ',' + str(row['id']) + ',' + correctedImageName + '\r\n'
            storeImageInfo(filePath, photoInfo)
