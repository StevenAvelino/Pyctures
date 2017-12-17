# How tools were used

## Pyexiv2
This module is used to parse the metadatas of images, as said previously.

We can parse the existing values and modify them. Pyexiv2 is based on the Exif format that a lot of images format are based on (jpg for example).
A list of all the standards Exif tags can be found [here](http://www.exiv2.org/tags.html).

In our application, we wanted to take already existing data from a picture, but also modify them.
The metadata we want to extract is the datetime of the picture, that will be used to rename the picture and also to show it as a property on the GUI.
To modify metadatas, we have to refer to the list of standard Exif tags list.

The issue we encountered was the fact that we couldn't insert string in tag that wasn't an ASCII. Some properties that we wanted to put, like a comment, had a standard tag for it that were in ASCII, but most of the properties didn't have that. The only solution we found, was to use different tags that weren't coherent, but had the ASCII type.

## JSON
We used JSON in the application to help speed up the search function
The application generates a JSON file at the root of the user's Images directory. It puts all the directories in the Images directories as nodes.
Each nodes will contain all the files with
* Path
* Comment
* Location
* People
* Tags
* Favorite

The properties are parsed in the metadatas and then written in the JSON file.
When the user modifies a property of a picture in the application, it will save the new property in the metadatas and in the JSON file, so the search function will work instantly.

## Regex
A regex was used in the application to check the file names of the pictures in the Images directory.
The regex is simple but cover most cases of file names.

```
([a-zA-Z\-\_]+_\d{15}.\w+)
```
The application renames the pictures with this pattern : dirname_datetime

## PIP
PIP is a packet manager for Python. most popular modules can be found with PIP and installed easily with a simple command.
Obviously, for it to work, it requires for the module we want to install to have been added to PIP.

## PIL
PIL or Pillow is the module used to manage the pictures.
The application uses it to open them and resize them. PIL is popular with a lot of documentation and help available.
PIL is a package available on PIP, which makes it really easy to install.


