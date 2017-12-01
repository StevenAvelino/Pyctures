import os
from Tkinter import *
import json
import pyexiv2
import functions
import operator


def testJson(folderPath, file):
    data = {}
    fileDir = folderPath.split("/")
    data[fileDir[5]] = []

    data[fileDir[5]].append({
        'path': folderPath + file,
        'comment': functions.getComment(folderPath + file),
        'people': functions.getPeople(folderPath + file),
        'location': functions.getLocation(folderPath + file),
        'tags': functions.getTags(folderPath + file),
        'favorite': functions.getFavorite(folderPath + file)
    })

    with open(folderPath + 'test.json', 'w') as outfile:
        json.dump(data, outfile)

def testParseJson(folderPath):
    data = {}

    for root, dirs, files in os.walk(folderPath):
        for dir in dirs:
            data[dir] = []
            print dir
        for file in files:
            fileDir = file.split("_")
            data[fileDir[0]].append( {
                'path': folderPath + fileDir[0] + "/" + str(file),
                'comment': functions.getProperty("comment",folderPath + fileDir[0] + "/" + str(file)),
                'people': functions.getProperty("people",folderPath + fileDir[0] + "/" + str(file)),
                'location': functions.getProperty("location",folderPath + fileDir[0] + "/" + str(file)),
                'tags': functions.getProperty("tags",folderPath + fileDir[0] + "/" + str(file)),
                'favorite': functions.getProperty("favorite",folderPath + fileDir[0] + "/" + str(file))
            }
            )
            print data[fileDir[0]]

# --- Search function ---



window = Tk()
window.title("Pyctures")
window.geometry("1200x1200")

folderPath = "P:/projet-python-photo/Sources/Scripts/Images/"
listPhotos = []
listLabel = []
listPath = []
filters = [False, False, False]
regex = re.compile('([A-Za-z\-_ ]+_[0-9]{14})')
rowPhoto = 0
columnPhoto = 1

photoFrame = Frame(window)
photoFrame.config(height=900, width=900)
photoFrame.grid(row=0,column=0)

#functions.getLocation(folderPath + "/Venise/Venise_8_20090312134839.jpg")
#startup(folderPath)
#functions.setComment(folderPath + "/Venise/Venise_3_20090312134818.jpg", "test")
#testJson("P:/projet-python-photo/Sources/Scripts/Images/Venise/" ,"Venise_3_20090312134818.jpg")
#testParseJson("P:/projet-python-photo/Sources/Scripts/Images/Venise/" ,"Venise_3_20090312134818.jpg")
#generateJson(folderPath)
#testParseJson(folderPath, "Venise")
functions.searchFunction(folderPath, "test", filters)
#functions.getFileSize(folderPath + "/Venise/Venise_3_20090312134818.jpg")
#functions.setProperty("location", "Veni", folderPath + "/Venise/Venise_1_20090312134642.jpg", folderPath)
#print functions.getLocation(folderPath + "/Venise/Venise_1_20090312134642.jpg")
#renamePhotos(listPath)
#generateJson(folderPath)
#searchFunction(folderPath,"Venise","")
#print functions.getPhotoTime(folderPath+"/Venise/Venise_1_20090312134828.jpg")
#functions.renamePhotos(functions.createListPhotos(folderPath), folderPath)
#functions.editJson(folderPath + "/Venise/Venise_1_20090312134642.jpg", folderPath, "location", "Venise")
#print functions.getProperty("location", folderPath + "/Venise/Venise_3_20090312134818.jpg")
#functions.setProperty("location","Test",folderPath + "/Venise/Venise_3_20090312134818.jpg", folderPath)
#functions.generateJson(folderPath)
#testParseJson(folderPath)
#print functions.createListPhotos(folderPath)

"""for file in os.listdir(folderPath):
    if file.lower().endswith(('.png', '.jpg', '.jpeg')):
        originalImg = Image.open(folderPath + file)
        originalImg2 = originalImg.resize((200, 200), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(originalImg2)

        listPhotos.append(img)

for photo in listPhotos:
    panel = Button(photoFrame, image = photo, borderwidth=0)
    panel.grid(row=rowPhoto, column=columnPhoto)
    if columnPhoto < 3:
        columnPhoto += 1
    else:
        rowPhoto += 1
        columnPhoto = 1

window.mainloop()"""