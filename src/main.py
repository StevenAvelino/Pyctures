import functions
from Tkinter import *
from PIL import Image, ImageTk
import os
import tkFont
import threading
import getpass

#Resize image for max 200x200
def resizeImage(image, maxsize):
    try:
        r1 = image.size[0]/maxsize # width ratio
        r2 = image.size[1]/maxsize # height ratio
        ratio = max(r1, r2)
        newsize = (int(image.size[0]/ratio), int(image.size[1]/ratio))
        image = image.resize(newsize, Image.ANTIALIAS)
    except:
        print("resize error !")
    return image

# Change the icon of the search bar(enabled, disabled)
def changeImageEna(element, stat, enable, disable):
    global filterStat
    if(filterStat[stat]==True):
        element.config(image=disable)
        filterStat[stat]=False
    elif(filterStat[stat]==False):
        element.config(image=enable)
        filterStat[stat] = True
    print("Per:"+str(filterStat[0])+" Favo:"+str(filterStat[1])+" Loc:"+str(filterStat[2]))

#When we click on the list of file
def fileSelection(self):
    global listPhotos, pathPhotos
    w = self.widget
    value = self.widget.get(int(w.curselection()[0]))
    global currentphotofolderPath
    currentphotofolderPath=photofolderPath+value+"/"
    listPhotos = []
    pathPhotos = []
    previousbutton.config(state="disabled")
    actualImageRange = 0
    loadImage(actualImageRange, actualImageRange + 9)

    t = threading.Thread(target=createImageGallery(actualImageRange, actualImageRange + 9))
    t.start()

#get properties of an image and display it
def getProperties(path):
    global sizeInfoLabel, dateInfoLabel, persInfoLabel, favoInfoLabel, dimInfoLabel, tagsInfoLabel, locaInfoLabel, propertyLabel, actualImage
    actualImage=path

    propertyLabel.config(text="Proprietes de : "+path)

    size = functions.getFileSize(path)
    size = float(size)/1048576
    sizeInfoLabel.config(text=str(round(size, 2))+" MB")

    date = functions.getPhotoTime(path)
    dateInfoLabel.config(text=str(date))

    people = StringVar()
    if((functions.getProperty("people", path)).encode('utf-8')=="None"):people.set("")
    else:people.set(functions.getProperty("people", path))
    persInfoEntry.config(textvariable=people)

    favorite = StringVar()
    if ((functions.getProperty("favorite", path)).encode('utf-8') == "None"): favorite.set("")
    else:favorite.set(functions.getProperty("favorite", path))
    favoInfoEntry.config(textvariable=favorite)

    dim = functions.getDimensions(path)
    dimInfoLabel.config(text=str(dim))

    tags = StringVar()
    if ((functions.getProperty("tags", path)).encode('utf-8') == "None"): tags.set("")
    else:tags.set(functions.getProperty("tags", path))
    tagsInfoEntry.config(textvariable=tags)

    location = StringVar()
    if ((functions.getProperty("location", path)).encode('utf-8') == "None"): location.set("")
    else:location.set(functions.getProperty("location", path))
    locaInfoEntry.config(textvariable=location)

    comment = StringVar()
    if ((functions.getProperty("comment", path)).encode('utf-8') == "None"): comment.set("")
    else:comment.set(functions.getProperty("comment", path))
    commInfoEntry.config(textvariable=comment)

#save property of an image
def saveProperty(element, property):
    global actualImage
    functions.setProperty(property, element.get(), actualImage, photofolderPath)

#functions where the image load -> not work actually
def load():
    global Img
    #panel = Label(photoCanvas, text="Chargement ...", borderwidth=0, height=300, width=300)
    #panel.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")

#when we double click on an image, display only one image bigger
def showOneImage(path):
    global photoCanvas
    photoCanvas.delete("all")
    for widget in photoCanvas.winfo_children():
        widget.destroy()

    global Img
    originalImg = Image.open(path)

    if photoFrame.winfo_height()>photoFrame.winfo_width():size=photoFrame.winfo_width()
    else:size=photoFrame.winfo_height()

    orImg = resizeImage(originalImg, size)
    Img = ImageTk.PhotoImage(orImg)
    panel = Label(photoCanvas, image=Img, borderwidth=0, height=size, width=size)
    panel.grid(row=1, column=1, padx=0, pady=0, sticky="nsew")
    photoCanvas.grid_rowconfigure(2, weight=1)
    photoCanvas.grid_columnconfigure(2, weight=1)


def loadImage(start, end, paths=1):
    global listPhotos, pathPhotos
    fullpath=False
    if paths==1:
        files = os.listdir(currentphotofolderPath)
    else:
        fullpath = True
        files = paths


    if len(files) < start:
        return
    if len(files)<end:
        end1=len(files)
    else:
        end1 = end

    for i in  range(start, end1, 1):
        if files[i].lower().endswith(('.png', '.PNG', '.jpg', '.JGP', '.jpeg', '.JPEG')):
            if fullpath:
                pathPhotos.append(files[i])
                originalImg = Image.open(files[i])
            else:
                pathPhotos.append(currentphotofolderPath + files[i])
                originalImg = Image.open(currentphotofolderPath + files[i])
            orImg = resizeImage(originalImg, 220)
            img = ImageTk.PhotoImage(orImg)
            listPhotos.append(img)
# create the gallery image in the canvas
def createImageGallery(start, end):
    place = {0:"nw", 1:"n", 2:"ne", 3:"w", 4:"nswe", 5:"e", 6:"sw", 7:"s", 8:"se"}
    global photoCanvas, listPhotos
    photoCanvas.delete("all")
    for widget in photoCanvas.winfo_children():
        widget.destroy()

    rowPhoto = 0
    columnPhoto = 0
    it = 0
    if len(listPhotos) < start:
        return
    if len(listPhotos) < end:
        end1 = len(listPhotos)
    else:
        end1 = end

    for i in range(start, end1, 1):
        global element, Photos
        Photos = []
        element = Button(photoCanvas, image=listPhotos[i], borderwidth=0, height=220, width=220)

        photoCanvas.grid_rowconfigure(rowPhoto, weight=1)
        photoCanvas.grid_columnconfigure(columnPhoto, weight=1)
        element.bind('<Button-1>', lambda event, path=pathPhotos[i]: getProperties(path))
        element.bind('<Double-Button-1>', lambda event, path=pathPhotos[i]: showOneImage(path))
        element.grid(row=rowPhoto, column=columnPhoto, padx=5, pady=5, sticky=place[it])

        it += 1
        if columnPhoto < 2:
            columnPhoto += 1
        else:
            rowPhoto += 1
            columnPhoto = 0
    root.geometry(str(root.winfo_width() - 1) + "x" + str(root.winfo_height() - 1))
    root.geometry(str(root.winfo_width()) + "x" + str(root.winfo_height()))

def treeviewslect(self):
    global searchDisplay
    searchDisplay = False
    w = self.widget
    curItem = w.focus()
    path = w.item(curItem)["tags"]
    formatpath = str(path).split("'",2)[1]
    getProperties(formatpath)

def nextClic():
    global actualImageRange
    nbPages = 0
    nbElement = len(os.listdir(currentphotofolderPath))
    if (nbElement/9.0).is_integer():
        nbPages = nbElement / 9
    else:
        nbPages = (nbElement / 9) + 1

    if nbPages*9<actualImageRange+18:return
    actualImageRange += 9
    createImageGallery(actualImageRange, actualImageRange + 9)
    previousbutton.config(state="normal")
    thread = threading.Thread(target=loadImage(actualImageRange+9, actualImageRange+18))
    thread.start()

def previousClic():
    global actualImageRange
    if actualImageRange == 0: return
    actualImageRange -= 9
    print(actualImageRange)
    createImageGallery(actualImageRange, actualImageRange + 9)
    if actualImageRange==0 : previousbutton.config(state="disabled")

def searchClic():
    global photofolderPath, filterStat, actualImageRange, listPhotos, pathPhotos, searchDisplay
    searchDisplay = True
    listPhotos = []
    pathPhotos = []
    actualImageRange = 0
    pathPhotos = functions.searchFunction(photofolderPath ,searchentry.get(), filterStat)
    loadImage(0, 9, pathPhotos)
    createImageGallery(actualImageRange, actualImageRange + 9)


###########################################################################################################################




#functions.generateJson(photofolderPath)



root = Tk()

root.geometry('{}x{}'.format(700, 910))
root.minsize(width=950, height=910)
root.iconbitmap('P:/Pycture/projet-python-photo/Documentations/logo/logo.ico')
root.title("Pyctures")

photofolderPath = "C:/Users/"+getpass.getuser()+"/Pictures/"
#rename = functions.createListPhotos(photofolderPath)
#functions.renamePhotos(rename, photofolderPath)
functions.generateJson(photofolderPath)


listPhotos = []
pathPhotos = []
icoPath = "P:/Pycture/projet-python-photo/Downloads/MyIcons/"
actualImage=""
actualImageRange = 0
dirs = [d for d in os.listdir(photofolderPath) if os.path.isdir(os.path.join(photofolderPath, d))]
currentphotofolderPath = photofolderPath+dirs[0]+"/"
searchDisplay = False




#Open all icons
locaIcoDis = Image.open(icoPath+"locaDis.png")
locaIcoDis = ImageTk.PhotoImage(locaIcoDis)
locaIcoEna = Image.open(icoPath+"locaEna.png")
locaIcoEna = ImageTk.PhotoImage(locaIcoEna)
favoIcoEna = Image.open(icoPath+"favoEna.png")
favoIcoEna = ImageTk.PhotoImage(favoIcoEna)
favoIcoDis = Image.open(icoPath+"favoDis.png")
favoIcoDis = ImageTk.PhotoImage(favoIcoDis)
userIcoEna = Image.open(icoPath+"userEna.png")
userIcoEna = ImageTk.PhotoImage(userIcoEna)
userIcoDis = Image.open(icoPath+"userDis.png")
userIcoDis = ImageTk.PhotoImage(userIcoDis)
searchIco = Image.open(icoPath+"search.png").convert("RGBA")
searchIco = ImageTk.PhotoImage(searchIco)

#define main frame
searchFrame = Frame(root, width=200, height=100, bg="#0071B9")
centerFrame = Frame(root, width=450, height=40)
botttomFrame = Frame(root, width=450, height=120, bg="#0071B9")

#define sticky frame
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)

#place on grid
searchFrame.grid(row=0, sticky="ew")
centerFrame.grid(row=1, sticky="nsew")
botttomFrame.grid(row=2, sticky="ew")

###########################################################################################
#
#Define the frame of root Tk
###########################################################################################
centerFrame.grid_rowconfigure(0, weight=1)
centerFrame.grid_columnconfigure(1, weight=1)

# define menu and center frame
menuFrame = Frame(centerFrame, width=200, height=220, bg="#005992")  # 2A2440
photoFrame = Frame(centerFrame, width=250, height=190)

# place on grid
menuFrame.grid(row=0, column=0, sticky="ns")
photoFrame.grid(row=0, column=1, sticky="nsew")

# photocanvas is for draw iamge in frame
photoCanvas = Canvas(photoFrame)
canvasFrame = Frame(photoFrame)

photoCanvas.grid(row=0, column=0, sticky="nsew")

photoFrame.grid_rowconfigure(0, weight=1)
photoFrame.grid_columnconfigure(0, weight=1)

###########################################################################################
#
# Set search frame
###########################################################################################
searchFrame.grid_rowconfigure(1, weight=1)
searchFrame.grid_columnconfigure(2, weight=1)

#Open the logo of pyctures app
oriLogo = Image.open(icoPath+"logo.png")
orLogo = resizeImage(oriLogo, 60)
logoImage = ImageTk.PhotoImage(orLogo)
logoLabel = Label(searchFrame, image=logoImage, borderwidth=0, bg="#0071B9")

#font for pycture app name
logoFont = tkFont.Font(size=25, weight=tkFont.BOLD)

pictureLogo = Label(searchFrame, text="PYCTURES", bg="#0071B9", fg="#ffffff", font=logoFont)



#the state of search filter
filterStat = [False, False, False]

#define buttons
favoButt = Button(searchFrame, relief="flat", image=favoIcoDis, bd=0, bg="#0071B9")
favoButt.bind('<Button-1>', lambda event, stat=1, element=favoButt, enable=favoIcoEna, disable=favoIcoDis: changeImageEna(element, stat, enable, disable))

userButt = Button(searchFrame, relief="flat", image=userIcoDis, bd=0, bg="#0071B9")
userButt.bind('<Button-1>', lambda event, stat=0, element=userButt, enable=userIcoEna, disable=userIcoDis: changeImageEna(element, stat, enable, disable))

locaButt = Button(searchFrame, relief="flat", image=locaIcoDis, bd=0, bg="#0071B9")
locaButt.bind('<Button-1>', lambda event, stat=2, element=locaButt, enable=locaIcoEna, disable=locaIcoDis: changeImageEna(element, stat, enable, disable))

#histScal = Scale(searchFrame, length=75, orient=HORIZONTAL, showvalue=0, bg="#0071B9")

searchentry = Entry(searchFrame, width=60)
searchbuton = Button(searchFrame, image=searchIco, relief=FLAT, bg="#0071B9")
searchbuton.bind('<Button-1>', lambda event: searchClic())


logoLabel.grid(column=0, row=1, sticky="w", padx=(5, 0), pady=5)
pictureLogo.grid(column=1, row=1, sticky="w")
userButt.grid(column=2, row=1, sticky="e", padx=5, pady=10)
favoButt.grid(column=3, row=1, sticky="e", padx=5)
locaButt.grid(column=4, row=1, sticky="e", padx=5)
#histScal.grid(column=5, row=1, sticky="e", padx=10)
searchentry.grid(column=6, row=1, columnspan=2, sticky="e", padx=10)
searchbuton.grid(column=9, row=1, sticky="e", padx=10)
###########################################################################################
#
# Set the menu frame, with folder
###########################################################################################
menuFrame.grid_rowconfigure(0, weight=1)
menuFrame.grid_columnconfigure(0, weight=1)

menufont = tkFont.Font(size=15)

#define a scrollbar
menuscrollbar = Scrollbar(menuFrame, orient=VERTICAL, bg="#2A2440")

#define list
dosslist = Listbox(menuFrame, font=menufont, bg="#005992", fg="#ffffff", borderwidth=0, highlightthickness=0, selectmode=SINGLE, relief=FLAT)

# get folder of current path
for item in dirs:
    dosslist.insert(END, item)

dosslist.config(yscrollcommand=menuscrollbar.set)
menuscrollbar.config(command=dosslist.yview)



# associate with func
dosslist.bind("<<ListboxSelect>>", fileSelection)

dosslist.grid(column=0, row=0, sticky="nsew", padx=(10, 0), pady=(10, 0))
menuscrollbar.grid(column=1, row=0, sticky="nsew")
###########################################################################################
#
# Set bottom frame with properties of photos
###########################################################################################
botttomFrame.grid_rowconfigure(0, weight=1)
botttomFrame.grid_columnconfigure(0, weight=1)

bold = tkFont.Font(size=10, weight=tkFont.BOLD)

previousbutton = Button(botttomFrame, fg="#0071B9", text="Precedent", state=DISABLED, width=20, relief=FLAT, font=bold)
previousbutton.bind("<Button-1>", lambda event, range=actualImageRange: previousClic())

nextbutton = Button(botttomFrame, fg="#0071B9", text="Suivant", width=20, relief=FLAT, font=bold)
nextbutton.bind("<Button-1>", lambda event, range=actualImageRange: nextClic())


propertyLabel = Label(botttomFrame, text="", bg="#0071B9", fg="#ffffff")

underline = tkFont.Font()
underline.configure(underline=True)

#Define property fields and texts
sizeTitleLabel = Label(botttomFrame, text="Taille fichier", font=underline, bg="#0071B9", fg="#ffffff")
sizeInfoLabel = Label(botttomFrame, text="", bg="#0071B9", fg="#ffffff")

dateTitleLabel = Label(botttomFrame, text="Date de prise de vue", font=underline, bg="#0071B9", fg="#ffffff")
dateInfoLabel = Label(botttomFrame, text="", bg="#0071B9", relief=FLAT, justify=CENTER, fg="#ffffff")

persTitleLabel = Label(botttomFrame, text="Personne", font=underline, bg="#0071B9", fg="#ffffff")
persInfoEntry = Entry(botttomFrame, text="", bg="#0071B9", relief=FLAT, justify=CENTER, fg="#ffffff")
persInfoEntry.bind('<FocusOut>', lambda event, element=persInfoEntry, property="people", text=persInfoEntry.get(): saveProperty(element, property))

favoTitleLabel = Label(botttomFrame, text="Favori", font=underline, bg="#0071B9", fg="#ffffff")
favoInfoEntry = Entry(botttomFrame, text="", bg="#0071B9", relief=FLAT, justify=CENTER, fg="#ffffff")
favoInfoEntry.bind('<FocusOut>', lambda event, element=favoInfoEntry, property="favorite", text=favoInfoEntry.get(): saveProperty(element, property))

dimTitleLabel = Label(botttomFrame, text="Dimensions", font=underline, bg="#0071B9", fg="#ffffff")
dimInfoLabel = Label(botttomFrame, text="", bg="#0071B9", relief=FLAT, justify=CENTER, fg="#ffffff")

tagsTitleLabel = Label(botttomFrame, text="Tags", font=underline, bg="#0071B9", fg="#ffffff")
tagsInfoEntry = Entry(botttomFrame, text="", bg="#0071B9", relief=FLAT, justify=CENTER, fg="#ffffff")
tagsInfoEntry.bind('<FocusOut>', lambda event, element=tagsInfoEntry, property="tags", text=tagsInfoEntry.get(): saveProperty(element, property))

locaTitleLabel = Label(botttomFrame, text="Lieu", font=underline, bg="#0071B9", fg="#ffffff")
locaInfoEntry = Entry(botttomFrame, text="", bg="#0071B9", relief=FLAT, justify=CENTER, fg="#ffffff")
locaInfoEntry.bind('<FocusOut>', lambda event, element=locaInfoEntry, property="location", text=locaInfoEntry.get(): saveProperty(element, property))

commTitleLabel = Label(botttomFrame, text="Commentaire", font=underline, bg="#0071B9", fg="#ffffff")
commInfoEntry = Entry(botttomFrame, text="", bg="#0071B9", relief=FLAT, justify=CENTER, fg="#ffffff")
commInfoEntry.bind('<FocusOut>', lambda event, element=commInfoEntry, property="comment", text=commInfoEntry.get(): saveProperty(element, property))


#place all on grid
previousbutton.grid(column=2, row=0, pady=5)
nextbutton.grid(column=3, row=0, pady=5)
propertyLabel.grid(column=0, row=1, sticky="e", columnspan=4, pady=5)
sizeTitleLabel.grid(column=1, row=2, sticky="ew", padx=60)
sizeInfoLabel.grid(column=1, row=3, sticky="ew")
dateTitleLabel.grid(column=2, row=2, sticky="ew", padx=60)
dateInfoLabel.grid(column=2, row=3, sticky="ew")
persTitleLabel.grid(column=3, row=2, sticky="ew", padx=60)
persInfoEntry.grid(column=3, row=3, sticky="ew")
favoTitleLabel.grid(column=4, row=2, sticky="ew", padx=60)
favoInfoEntry.grid(column=4, row=3, sticky="ew")
dimTitleLabel.grid(column=1, row=4, sticky="ew")
dimInfoLabel.grid(column=1, row=5, sticky="ew")
tagsTitleLabel.grid(column=2, row=4, sticky="ew")
tagsInfoEntry.grid(column=2, row=5, sticky="ew")
locaTitleLabel.grid(column=3, row=4, sticky="ew")
locaInfoEntry.grid(column=3, row=5, sticky="ew")
commTitleLabel.grid(column=4, row=4, sticky="ew")
commInfoEntry.grid(column=4, row=5, sticky="ew")



###########################################################################################
#
# Create the image gallery with a thread
###########################################################################################

#photoCanvas.create_window(0, 0, window=canvasFrame, anchor='nw')

# create a thread for not block windows and start it and create imagegallery
loadImage(actualImageRange, actualImageRange+9)
createImageGallery(actualImageRange, actualImageRange+9)

loadImage(actualImageRange+9, actualImageRange+18)
#firstThread = threading.Thread(name='GetImage', target=loadImage(actualImageRange+9, actualImageRange+18))
#firstThread.start()


###########################################################################################
#
# Set root properties
###########################################################################################


root.mainloop()

