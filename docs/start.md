# Start

Each time the application starts, it will control the naming of your photos.
If they do not correspond to our norm, they will be renamed as follows: "NameFolder_YYYYMMDDhhmmss1"For example "Venice_201711291607031". The last digit is by default 1 but if two images were taken exactly at the same time, the second image will have the number 2.
You must also delete the image sample folder from Windows.

## Issue

Currently there is a bug, if you move a photo of Venice in the Rome folder and you delete the folder Venice, the program will make a mistake at startup.
To avoid this bug, simply rename the image to "img123" for example. 