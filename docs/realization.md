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
The next/previous buttons work in the simple explorer, but when you search for pictures, 
## Issues resolved


Bouton suivant fonctionne pas recherche
Plus d'image selectionnée possiblité changer proprietes
Démarrage attention pas changer de dossier et ensuite le supprimer
Double clic image, non optimisé
9 images pas trop responsive en grand

