'''
    Functions script for Pyctures application
    Authors: Steven Avelino & Kevin Jordil
    Last updated date: 24th November 2017

    This script contains all functions to handle the pictures and their datas for the application
'''

'''
    Modules
        os : os is the module to interact with the default functions of the OS we're using to launch the application
        pyexiv2 : This is the module that enables the different metadatas functions
        PIL : PIL is the module that handles the images, such as opening them
        re : Module to use for Regex
        json : Module for Json functions
        codecs : Module used for the generation of the Json file for the search function. Used to put the data in the Json file with the right codecs
'''

import os
import pyexiv2
from PIL import Image
import re
import json
import codecs

'''
    Function to edit the Json file.
    When the user modifies a property on a photo, the metadatas will be modified.
    As the search function uses a Json file, the datas in this file must also be updated.
    That's the purpose of this function.
    
    Paramaters explanation : 
    photo : The file name of the photo that will get edited
    folderPath : The full path of the image folder. It will will be used to search the json file to edit
    type : Which metadata is going to be edited
    property : The new value of the metadata
'''
def editJson(photo, folderPath, type, property):
    # Get only the file name of the photo
    photoPathSplit = photo.split("/")
    jsonNode = photoPathSplit[len(photoPathSplit)-2]
    dirsList = []

    '''
        The function is going to open the json file first.
        Take the nodes needed to look for the property that's gonna get edited.
        Then change the property with the new value
    '''
    with open(folderPath + 'search.json') as jsonFile:
        data = json.load(jsonFile)
    for dirs, photos in data.items():
        dirsList.append(dirs)
    for jsonDirs in dirsList:
        if jsonDirs == jsonNode:
            for p in data[jsonDirs]:
                if p['path'] == photo:
                    p[type] = property
    with open(folderPath + 'search.json', "w") as jsonFile:
        json.dump(data, jsonFile)


'''
    Function that will create a list of all the photos in the root image folder and its children
'''
def createListPhotos(folderPath):
    listPath = []

    # For loop that will walk through all the directories in the root folder
    for root, dirs, files in os.walk(folderPath):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                tmpString = os.path.join(root, file)
                tmpString2 = tmpString.replace('\\', '/')
                listPath.append(tmpString2)
    # Return a list of all the paths
    return listPath

'''
    This function is to rename the photos that are in the root folder and its children
    The functions renames the files with this structure : 'FileDirectoryName_DateTime'
    To check if the file was already renamed, the function uses a regex
    
    Parameters explanation
    listPhotos : List that that was created by the 'createListPhotos' function to check all the photos
    folderPath : The root directory to rename the photos with the system functions (need absolute path) 
'''
def renamePhotos(listPhotos, folderPath):
    '''
        This regex was made to cover the most possibilties of directory names
    '''
    regex = re.compile('([a-zA-Z\-\_]+_\d{15}.\w+)')
    for photo in listPhotos:
        # Split the path of the photo to get the different required elements
        photoPathSplit = photo.split("/")
        # Get the extension since the new file name will be split and we need to rebuild it
        extension = photo.split(".")
        # Check if the regex didn't match to know if we need to rename the file
        if not regex.match(photoPathSplit[len(photoPathSplit) -1]):
            # Put the default metadata properties
            setProperty("comment", "", photo, folderPath)
            setProperty("people", "", photo, folderPath)
            setProperty("location", "", photo, folderPath)
            setProperty("tags", "", photo, folderPath)
            setProperty("favorite", "0", photo, folderPath)
            '''
                The file name we want as a result of this function, needs to take the date of the picture we're gonna rename.
                For that, we'll need to read the metatdatas and extract the date from there.
                We use the pyexiv2 module to parse the metadatas that are returned as a dictionary.
                We'll loop trough this dictionary with a for loop, take the key we want to read and then take the value
                We'll take the directory name and reassemble all of the parts, then rename the file itself
            '''
            metadata = pyexiv2.ImageMetadata(photo)
            metadata.read()
            for key in metadata.exif_keys:
                tag = metadata[key]
                if key == "Exif.Image.DateTime":
                    dateTime = tag.value
                    dateTime = str(dateTime)
                    if dateTime == "":
                        fileName = photoPathSplit[(len(photoPathSplit) - 2)] + "_"
                        photoPathSplit[len(photoPathSplit) - 1] = fileName
                        finalName = "/"
                        finalName = finalName.join(photoPathSplit)
                        finalName.encode('utf-8')
                        if (os.path.exists(finalName + extension[len(extension) - 1])):
                            os.rename(photo, finalName + "2" + "." + extension[len(extension) - 1])
                        else:
                            os.rename(photo, finalName + "1" + "." + extension[len(extension) - 1])
                    else:
                        dateTime = dateTime.replace(":", "")
                        dateTime = dateTime.replace("-", "")
                        dateTime = dateTime.replace(" ", "")
                        fileName = photoPathSplit[len(photoPathSplit) - 2] + "_" + dateTime
                        photoPathSplit[len(photoPathSplit) - 1] = fileName
                        finalName = "/"
                        finalName = finalName.join(photoPathSplit)
                        finalName.encode('utf-8')
                        if (os.path.exists(finalName + extension[len(extension) - 1])):
                            os.rename(photo, finalName + "2" + "." + extension[len(extension) - 1])
                        else:
                            os.rename(photo, finalName + "1" + "." + extension[len(extension) - 1])

'''
    Function to set the metadata properties on a picture
'''
def setProperty(type, property, photo, folderPath):
    metadata = pyexiv2.ImageMetadata(photo)
    metadata.read()
    metadata.modified = True
    metadata.writable = os.access(photo, os.W_OK)
    if type == "comment":
        key = 'Exif.Photo.UserComment'
    elif type == "people":
        key = 'Exif.Image.ImageID'
    elif type == "location":
        key = 'Exif.Image.SecurityClassification'
    elif type == "tags":
        key = 'Exif.Photo.CameraOwnerName'
    elif type == "favorite":
        key = 'Exif.Photo.BodySerialNumber'
    metadata[key] = pyexiv2.ExifTag(key, property)
    metadata.write()
    if(os.path.exists(folderPath + "search.json")):
        editJson(photo, folderPath, type, property)

def getDimensions(photo):
    im = Image.open(photo)
    width, height = im.size
    dimension = str(width)+"x"+str(height)
    return dimension

def getFileSize(photo):
    file = os.path.getsize(photo)
    return file

def getPhotoTime(photo):
    metadata = pyexiv2.ImageMetadata(photo)
    metadata.read()

    for key in metadata.exif_keys:
        tag = metadata[key]
        if key == "Exif.Photo.DateTimeOriginal":
            dateTime = tag.value
            dateTime = str(dateTime)
            return dateTime

def getProperty(type, photo):
    metadata = pyexiv2.ImageMetadata(photo)
    metadata.read()
    propertyKey = ""

    for key in metadata.exif_keys:
        tag = metadata[key]
        if type == "comment":
            if key == "Exif.Photo.UserComment":
                propertyKey = tag.value
        elif type == "people":
            if key == "Exif.Image.ImageID":
                propertyKey = tag.value
        elif type == "location":
            if key == "Exif.Image.SecurityClassification":
                propertyKey = tag.value
        elif type == "tags":
            if key =="Exif.Photo.CameraOwnerName":
                propertyKey = tag.value
        elif type == "favorite":
            if key == "Exif.Photo.BodySerialNumber":
                propertyKey = tag.value
    propertyKey = str(propertyKey)
    return propertyKey

'''
    Function to search for files
    The application uses filters (People, Location and Favorites), the function has to adapt to all the possible cases of a search
    To search faster, we'll use the Json file we generated to get the paths of the files we want to return
    The function returns a list of all the paths of pictures that complied with what the user searched for
'''
def searchFunction(folderPath ,search, filter):
    returnList = []
    dirsList = []

    with open(folderPath + 'search.json') as json_file:
        data = json.load(json_file)
        for dirs, photos in data.items():
            dirsList.append(dirs)
        for jsonDirs in dirsList:
            if filter[0] == False and filter[1] == False and filter[2] == False:
                if search in jsonDirs:
                    for p in data[jsonDirs]:
                        returnList.append(p['path'])
                else:
                    for p in data[jsonDirs]:
                        if search in p['tags'] or search in p['people'] or search in p['location'] or p['comment']:
                            returnList.append(p['path'])
            elif filter[0] == True and filter[1] == False and filter[2] == False:
                for p in data[jsonDirs]:
                    if p['people'] is not None:
                        if search in p['people']:
                            returnList.append(p['path'])
            elif filter[0] == False and filter[1] == True and filter[2] == False:
                if search == "":
                    for p in data[jsonDirs]:
                        if p['favorite'] == "1" :
                            returnList.append(p['path'])
                else:
                    if search in jsonDirs:
                        for p in data[jsonDirs]:
                            if p['favorite'] == "1":
                                returnList.append(p['path'])
                    else:
                        for p in data[jsonDirs]:
                            if search in p['tags'] or search in p['people'] or search in p['location'] or p['comment']:
                                if p['favorite'] == "1":
                                    returnList.append(p['path'])
            elif filter[0] == False and filter[1] == False and filter[2] == True:
                for p in data[jsonDirs]:
                    if p['location'] is not None:
                        if search in p['location']:
                            returnList.append(p['path'])
            elif filter[0] == True and filter[1] == True and filter[2] == False:
                for p in data[jsonDirs]:
                    if p['people'] is not None and p['location'] is not None:
                        if search in p['people'] and search in p['location']:
                            returnList.append(p['path'])
            elif filter[0] == True and filter[1] == False and filter[2] == True:
                for p in data[jsonDirs]:
                    if p['people'] is not None and p['favorite'] is not None:
                        if search in p['people']:
                            returnList.append(p['path'])
            elif filter[0] == False and filter[1] == True and filter[2] == True:
                for p in data[jsonDirs]:
                    if p['location'] is not None and p['favorite'] is not None:
                        if search in p['location']:
                            returnList.append(p['path'])
            elif filter[0] == True and filter[1] == True and filter[2] == True:
                for p in data[jsonDirs]:
                    if p['location'] is not None and p['favorite'] is not None and p['people'] is not None:
                        if search in p['location'] and search in p['people']:
                            returnList.append(p['path'])
    return returnList


'''
    Function to generate the Json file
    For the search function to be faster, we generate a Json file with all the paths and properties of all pictures
    If the file already exists, the function will compare the existing directories and the nodes in the Json file
'''
def generateJson(folderPath):
    if not (os.path.exists(folderPath + "search.json")):
        data = {}
        regex = re.compile('([a-zA-Z\-\_]+_\d{15}.\w+)')

        for root, dirs, files in os.walk(folderPath):
            for dir in dirs:
                data[dir] = []
            for file in files:
                if regex.match(file):
                    fileDir = file.split("_")
                    data[fileDir[0]].append({
                        'path': folderPath + fileDir[0] + "/" + str(file),
                        'comment': getProperty("comment",folderPath + fileDir[0] + "/" + str(file)),
                        'people': getProperty("people",folderPath + fileDir[0] + "/" + str(file)),
                        'location': getProperty("location",folderPath + fileDir[0] + "/" + str(file)),
                        'tags': getProperty("tags",folderPath + fileDir[0] + "/" + str(file)),
                        'favorite': getProperty("favorite",folderPath + fileDir[0] + "/" + str(file))
                    }
                    )

        with open(folderPath + 'search.json', 'wb') as jsonFile:
            json.dump(data, codecs.getwriter('utf-8')(jsonFile), ensure_ascii=False)
    else:
        nodesList = []
        dirsList = []

        with open(folderPath + 'search.json') as jsonFile:
            data = json.load(jsonFile)
        for dirs, photos in data.items():
                nodesList.append(dirs)
        for root, dirs, files in os.walk(folderPath):
            for dir in dirs:
                dirsList.append(dir)
            for dirs in dirsList:
                if not dirs in nodesList:
                    data[dirs] = []
                    for file in files:
                        data[dirs].append({
                            'path': folderPath + dirs + "/" + str(file),
                            'comment': getProperty("comment", folderPath + dirs + "/" + str(file)),
                            'people': getProperty("people", folderPath + dirs + "/" + str(file)),
                            'location': getProperty("location", folderPath + dirs + "/" + str(file)),
                            'tags': getProperty("tags", folderPath + dirs + "/" + str(file)),
                            'favorite': getProperty("favorite", folderPath + dirs + "/" + str(file))
                        }
                        )

        json.dump(data, codecs.getwriter('utf-8')(jsonFile), ensure_ascii=False)
