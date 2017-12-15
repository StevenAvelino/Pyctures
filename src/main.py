import functions                # Import the other functions
from Tkinter import *           # Import tkinter graphic library
from PIL import Image, ImageTk  # Import PIL for display image
import os                       # Import os for get the image in folder
import tkFont                   # Import tkfont for change font
import threading                # import threading for create thread
import getpass                  # Import getpass for get windows username



# First part is for functions the second part for display the application


#This function get image and maxsize and return a resized image
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

# This function change the icon of filter and updae the array filterStat
def changeImageEna(element, stat, enable, disable):
    global filterStat
    if(filterStat[stat]==True):
        element.config(image=disable)
        filterStat[stat]=False
    elif(filterStat[stat]==False):
        element.config(image=enable)
        filterStat[stat] = True

# This function is called when we change folder by the menu. Update display pohots
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
    thread = threading.Thread(target=loadImage(actualImageRange + 9, actualImageRange + 18))
    thread.start()

# This function get properties of an image and display it
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

#This function save a property of an image
def saveProperty(element, property):
    global actualImage
    functions.setProperty(property, element.get(), actualImage, photofolderPath)


#this function display only one image bigger, call when we double click on image
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

# This function load image
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

# this function create the gallery image in the canvas
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

# This function display the next elements, call when we click on next button
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

# This function display the previous elements, call when we click on previous button
def previousClic():
    global actualImageRange
    if actualImageRange == 0: return
    actualImageRange -= 9
    createImageGallery(actualImageRange, actualImageRange + 9)
    if actualImageRange==0 : previousbutton.config(state="disabled")

# This function search the image and display the image
def searchClic():
    global photofolderPath, filterStat, actualImageRange, listPhotos, pathPhotos
    listPhotos = []
    pathPhotos = []
    actualImageRange = 0
    pathPhotos = functions.searchFunction(photofolderPath ,searchentry.get(), filterStat)
    loadImage(0, 9, pathPhotos)
    createImageGallery(actualImageRange, actualImageRange + 9)


###########################################################################################################################
# This is the second part here, we create the display application


root = Tk()

# Configure the main frame
root.geometry('{}x{}'.format(700, 910))
root.minsize(width=950, height=910)
root.iconbitmap(os.path.dirname(sys.argv[0])+'/assets/logo.ico')
root.title("Pyctures")

# Get the photo path
photofolderPath = "C:/Users/"+getpass.getuser()+"/Pictures/"

# Rename photo and generate json
rename = functions.createListPhotos(photofolderPath)
functions.renamePhotos(rename, photofolderPath)
functions.generateJson(photofolderPath)

# Define the variable i need in my program
listPhotos = []
pathPhotos = []
icoPath = os.path.dirname(sys.argv[0])+'/assets/' # Get the icopath of app folder
actualImage=""
actualImageRange = 0
dirs = [d for d in os.listdir(photofolderPath) if os.path.isdir(os.path.join(photofolderPath, d))] # get list of directory in image folder
currentphotofolderPath = photofolderPath+dirs[0]+"/"



# Open all icons
# For open image we need path and wit PIL we can load it in a variable
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

# define main frame
# For defin an element we declare a vriable name and after it we specifie the type and type need properties like parent, size, color, ...)
searchFrame = Frame(root, width=200, height=100, bg="#0071B9")
centerFrame = Frame(root, width=450, height=40)
botttomFrame = Frame(root, width=450, height=120, bg="#0071B9")

# With this we specifie what frame grow when we grow app
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)

# The grid is a table and we put element with .grid, column number, row number and sticky is for where the element is fix in the cell
searchFrame.grid(row=0, sticky="ew")
centerFrame.grid(row=1, sticky="nsew")
botttomFrame.grid(row=2, sticky="ew")

###########################################################################################
#
# Define the center frame
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
# bind is for call a function when we do an action on a element, here is a simple click
favoButt.bind('<Button-1>', lambda event, stat=1, element=favoButt, enable=favoIcoEna, disable=favoIcoDis: changeImageEna(element, stat, enable, disable))

userButt = Button(searchFrame, relief="flat", image=userIcoDis, bd=0, bg="#0071B9")
userButt.bind('<Button-1>', lambda event, stat=0, element=userButt, enable=userIcoEna, disable=userIcoDis: changeImageEna(element, stat, enable, disable))

locaButt = Button(searchFrame, relief="flat", image=locaIcoDis, bd=0, bg="#0071B9")
locaButt.bind('<Button-1>', lambda event, stat=2, element=locaButt, enable=locaIcoEna, disable=locaIcoDis: changeImageEna(element, stat, enable, disable))

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
# Create the first image gallery
###########################################################################################


loadImage(actualImageRange, actualImageRange+9)
createImageGallery(actualImageRange, actualImageRange+9)

loadImage(actualImageRange+9, actualImageRange+18)


root.mainloop()

