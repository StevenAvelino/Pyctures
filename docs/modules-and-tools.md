# Modules & Tools used

## Python 2.7.x
With Python 3.x being out for a long time and being stable, it seems weird to use Python 2.7.x 
We had to use it because of the metadata module (pyexiv2) that we used was only compatible with Python 2.7.x
There is a Python 3.x version, but it isn't stable and we wanted a module that, we knew, would work without any issues.

## Tkinter
Tkinter is the default GUI module for Python.
It is extremely simple, but as we saw that the GUI for the application was going to be simple, we chose to go for the simple option.
We obviously looked for others GUIs modules, we had 2 other options in mind : PyQT and PyForms
### PyQT
QT is a well known framework for C++ used to make good looking, fast and customizable GUIs without much effort, PyQT is just a Python version of it. Even with all these qualities, QT is heavy and would have been difficult to learn in such a short time, so we scraped the idea. (For more information on the framework, go [here](https://www.qt.io))

### PyForms
PyForms is, just like PyQT, a framework to create GUIs with Python. It uses components from PyQT, OpenGL and some other libraries.
We considered to use this framework because of its simplicity and the possibility of using CSS to make the layout and put good looking styles on it. We scraped it because of the learning curve, just like PyQT and the fact it didn't work well on Windows with Python 2.7.x (For more information on PyForms, go [here](https://pyforms.readthedocs.io/en/v2.0/)

## Pyexiv2
To handle the different properties we will need to get or write on pictures, metadatas are the way to go. With python, the module that is used is pyexiv2.
It's a small, fast and easy module that does what we want.

## PIL
PIL or Pillow is a popular image handler for Python.
We need this module to handle all the operations on the pictures we're gonna use. Showing them and resizing them are the main operations we do and PIL make it really easy to do.

## PIP
PIP, or Python Package Index, is a packet manager used to download and install new modules for Python really easily.

## JSON
JSON, or JavaScript Object Notation, is an alternative to XML, which is used to store data in a text format.

## PyCharm
PyCharm is the IDE used to code the application.

## Regex
Regex, or rational expression, is a powerful tool for string validation.
It is used in the project to check if the pictures were renamed correctly.

## Git
Since we worked on a project with more than 1 person, git is mendatory to work in a team.
Before using Github, we used Bitbucket and worked for most of the project on it.

The Bitbucket repository can be found [here](https://bitbucket.org/Aiiro/projet-python-photo)