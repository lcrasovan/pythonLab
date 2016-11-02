# Python laboratory - code here is tested with Python 2.7.1

### Environment setting

First of all copy default settings file and customize it

```shell
cp settings.default.ini settings.ini
```

Install the autopep8 

```shell
pip install autopep8
pip install pep8
```

for keeping the code up to date with the code style standards. To autocorrect code style just run:


```shell
autopep8 your_python_file.py
```

### Image quality check process: imageProcessor.py

The following problem is solved: 

Loop through all images  - get names from MySQL database   
Get image size without downloading it (they are HQ images - 4000 x 3000 pixels) from the first 1024 bytes of the file  
If image is too small, put its name in a local file for further info

### Running tests - from the console in the root folder execute 

```shell
python -m unittest discover
```

This will look for all files starting with test\* in the 'test' folder and execute them 
