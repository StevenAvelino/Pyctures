for build Pycture you need to have Python 2.7
Here python is install in C:\Python27
After that you need CX Freeze, you can easily intall it with pip like this :

```bash
C:\Python27\Python.exe -m pip install cx_freeze
```

After this go in the directory with all the py files for work application with cmd
In the folder you need to have the setup.py and icon.ico after that run this command

```bash
C:\Python27\python.exe setup.py build
```

In the bluid directory you have the main.exe