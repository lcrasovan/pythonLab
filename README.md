# Python laboratory - code here is tested with Python 2.7.1

### Environment setting

First of all copy default settings file and customize it

```shell
cp settings.default.ini settings.ini
```

### Image quality check process: imageProcessor.py

The following problem is solved: 

Loop through all images  - get names from MySQL database   
Get image size without downloading it (they are HQ images - 4000 x 3000 pixels) from the first 1024 bytes of the file  
If image is too small, put its name in a local file for further info

