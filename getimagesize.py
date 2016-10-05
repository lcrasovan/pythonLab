# -*- coding: utf-8 -*-
import ConfigParser
import pandas as pd
import urllib
from PIL import ImageFile
from sqlalchemy import create_engine


def createFolderPath(path):
    return 1

def downloadImage(uri, localPath):
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
config.read("/Users/restoin/projects/python/settings.ini")

userName = config.get('MySqlSection','user')
password = config.get('MySqlSection','password')
hostname = config.get('MySqlSection','host')
database = config.get('MySqlSection','database')
charset = config.get('MySqlSection','charset')
urlAmazonS3 = config.get('AWS','urlAmazonS3')
query = config.get('Repository','findImagesByCityAndProvider')

connectionString = 'mysql+pymysql://' + userName + ':' + password + '@' + hostname + '/' + database + '?charset=' + charset  

engine = create_engine(connectionString)

dataFrame = pd.read_sql_query(query,engine)

for index, row in dataFrame.head(10).iterrows():
        
    correctedImageName = row['imageName'].encode('utf-8')
    fileSize, dimensions = getImageSizes(urlAmazonS3 + correctedImageName)
    print row['restaurant'], row['id'], row['imageName'], fileSize, dimensions
