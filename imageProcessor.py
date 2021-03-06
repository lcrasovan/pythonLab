# -*- coding: utf-8 -*-
import ConfigParser
from repository.mySqlImageRepository import MySqlImageRepository
from helpers.imageutils import ImageUtils
import os

config = ConfigParser.ConfigParser()
currentDir = os.path.abspath(os.path.dirname(__file__))
config.read(os.path.join(currentDir, 'config', 'settings.ini'))
userName = config.get('MySqlSection', 'user')
password = config.get('MySqlSection', 'password')
hostname = config.get('MySqlSection', 'host')
database = config.get('MySqlSection', 'database')
charset = config.get('MySqlSection', 'charset')
query = config.get('Repository', 'findImagesByCityAndProvider')

urlAmazonS3 = config.get('AWS', 'urlAmazonS3')
minWidth = int(config.get('images', 'minWidth'))

cityId = '2'
imageFileDestination = config.get('cities', cityId)


connectionString = 'mysql+pymysql://' + userName + ':' + password + \
    '@' + hostname + '/' + database + '?charset=' + charset

dataFrame = MySqlImageRepository(connectionString).findImagesByQuery(query)

for index, row in dataFrame[0:2000].iterrows():
    correctedImageName = row['imageName'].encode('utf-8')
    imageUrl = urlAmazonS3 + correctedImageName
    print correctedImageName
    fileSize, dimensions = ImageUtils().getImageSizes(imageUrl)
    print fileSize, dimensions
    if dimensions and dimensions[0]:
        if int(dimensions[0]) < minWidth:
            filePath = os.path.join(currentDir, imageFileDestination, row['restaurant'] + '.csv')
            correctedProductName = row['productName'].encode('utf-8')
            if not os.path.isfile(filePath):
                header = 'ProductId,ProductName,ImageId,ImageFile' + '\r\n'
                ImageUtils().storeImageInfo(filePath, header)
            id = str(row['id']) if row['id'] else ''
            productId = str(row['productId']) if row['productId'] else ''
                
            photoInfo = productId + ',' + correctedProductName + ',' + id + ',' + correctedImageName + '\r\n'
            ImageUtils().storeImageInfo(filePath, photoInfo)
