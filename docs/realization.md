# Realization

## Issues
As in most first releases, the application still has some issues.
### Rename
While the rename functions works in a simple use case, if we use it in some cases, it can cause for the application to stop.
In a simple case, the user will create a new folder and put his pictures in the folder, then lunch the application. In this case, the application will work perfectly.
However, if the user deletes a folder that was opened in the application and just copy/paste the pictures to another folder without renaming them to something else or replace the folder name to the new one manually, the app will crash due to the fact that the JSON generation function won't create a node for the supposed folder contained in the names of the pictures.
#### Possible solution
Currently, the rename function won't do any operations to a picture that has a filename that the will match with the regex.
The solution would be to still check if the filename of the picture matches with the folder name.
### JSON File Generation
Currently, the application generates a JSON file every time it opens.
It works without much issues and doesn't take much time to generate, but it could be possible to just check if there is any difference between the JSON file and the files/folders.
#### Possible solution
The solution would be to check if the files and folders still exist in the Images folder and do the operations necessary.
### Time filter
We initially wanted to make a time filter for the search function.
The issue is that we didn't have the time to implement it.
#### Possible solution
Implement it.
### Next/Previous buttons in search function
The next/previous buttons work in the simple explorer, but when you search for pictures, only a page of 9 pictures will be shown.
The buttons work, but if you click on the next button, nothing will get shown, but you can go back to the first page.
####Possible solution

Kévin

### Properties of selected image can still be changed after selecting a new folder
When You select a picture, the properties will be shown like it should. However, if the user chooses to open a new folder, the properties of the last picture will still get shown.
It doesn't break anything, but it is still a bit weird to see as a user.
#### Possible solution

Kévin

### Image double-click
It isn't an application breaking issue, but when we double-click on a picture, the application will open it and display in the middle of the application.
Issue is that it doesn't always show the full picture depending on the size of the window of the application.
#### Possible solution

Kévin

### Responsive layout
Tkinter not being a really powerful GUI tool, it wasn't really made to do responsive GUIs.
The application is somewhat responsive, but the most noticeable issue is how the pictures are displayed when the application is full screen.
The pictures are displayed really far away from each other.
#### Possible solution

Kévin

### Favorite
Currently, to make a picture as a favorite, you need to set the property to 1.
It was a quick fix, so the filter could work in time.
However, initially, the favorite should have been a true/false choice or an icon like the favorite filter icon.
#### Possible solution
## Issues resolved
### Displaying pictures
Initially, we wanted to display the pictures in the middle of the application with all the pictures in the folder or returned by a search and use a scrollbar to go through the pictures.
The issue was to make this scrollbar works.

Kévin

### Search function
The first version of the search function was just to go through all the pictures and check the metadatas + the filename.
It worked, but it took a long time to search when the application handles a lot of pictures.
To speed up the search function, we decided to create a JSON file that will contain all the pictures with their paths and metadatas.
The application will generate the JSON file after renaming the pictures and when the user changes the property of a picture, the JSON file will get updated as well as the metadata.
### Metadatas
In itself, handle the metadatas is easy with the pyexiv2 module. However, the issue was the Exif tags to use.
Exif tags follows standard naming, which means that most properties didn't have a tag with a similar name. And the other issue was the type of data we could put in these Exif tags.
The application returns the properties as a string, which only Exif tags with they the datatype "ASCII" could store.
So to solve the issue, we used tags that were rarely used and that used the "ASCII" datatype to store the properties.



