# Build

After we developp Pyctures software with Python 2.7, we have some .py files.<br>
But the client work on Windows so he need to have an .exe file.

## How build it ?

for build our application to exe file you need to have Python 2.7.<br>
In our case Python is install in C:\Python27.<br>
After that you need CX Freeze, you can easily intall it with pip like this :

```bash
C:\Python27\Python.exe -m pip install cx_freeze
```

Once done, go in the directory, where the .py files are, with your favorite command prompt.
In the folder you need to have the setup.py and icon.ico.

```bash
C:\Python27\python.exe setup.py build
```

Python create with cx_freeze a folder named "build", in this folder you have main.exe.
If you want to move the application you need all the folder build.