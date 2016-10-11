# -*- coding: utf-8 -*-
import ConfigParser
import urllib
from PIL import ImageFile
from repository.mySqlImageRepository import MySqlImageRepository

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

config = ConfigParser.ConfigParser()
config.read(os.path.join(os.path.abspath(
    os.path.dirname(__file__)), 'config', 'settings.ini'))
userName = config.get('MySqlSection', 'user')
password = config.get('MySqlSection', 'password')
hostname = config.get('MySqlSection', 'host')
database = config.get('MySqlSection', 'database')
charset = config.get('MySqlSection', 'charset')
query = config.get('Repository', 'findImagesByCityAndProvider')

urlAmazonS3 = config.get('AWS', 'urlAmazonS3')
minWidth = int(config.get('images', 'minWidth'))

connectionString = 'mysql+pymysql://' + userName + ':' + password + \
    '@' + hostname + '/' + database + '?charset=' + charset

dataFrame = MySqlImageRepository(connectionString).findImagesByQuery(query)

for index, row in dataFrame[0:2000].iterrows():
    correctedImageName = row['imageName'].encode('utf-8')
    print correctedImageName
    fileSize, dimensions = getImageSizes(urlAmazonS3 + correctedImageName)
    print fileSize, dimensions
    if dimensions and dimensions[0]:
        if int(dimensions[0]) < minWidth:
            filePath = 'data/barcelona/' + row['restaurant'] + '.csv'
            if not os.path.isfile(filePath):
                header = 'ProductId,ProductName,ImageId,ImageFile' + '\r\n'
                storeImageInfo(filePath, header)
            photoInfo = str(row['productId']) + ',' + row['productName'].encode(
                'utf-8') + ',' + str(row['id']) + ',' + correctedImageName + '\r\n'
            storeImageInfo(filePath, photoInfo)
