# Build

After we develop Pyctures software with Python 2.7, we have some .py files.
But the client works on Windows, so it requires to deliver an .exe file.

## How to build it ?

To build our application to an exe file you need to have Python 2.7.
In our case Python is installed in C:\Python27.
After that you need CX Freeze, you can easily intall it with pip like this :

```bash
C:\Python27\Python.exe -m pip install cx_freeze
```

Once it's done, go in the directory where the .py files are with your favorite command prompt.
In the folder you need to have the setup.py and icon.ico.

```bash
C:\Python27\python.exe setup.py build
```

Python create with cx_freeze a folder named "build", in this folder you have main.exe.
If you want to move the application you need all the folder build.

## Installer

To create the installer, you need to download InnoSetup. Once installed, the wizard asks what you want to put in the installer and how you want to do it. For our part, it installs the files in Program Files in a folder named Pyctures.