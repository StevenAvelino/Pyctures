# Conception

## GUI
For the GUI, we were inspired by Picasa, which was the application the user previously used to manage his pictures.
Since the number of functionalities for this project are clearly less than the ones in Picasa, our application will have a simpler look.

The main functions of the GUI are
* Listing of the directories in the user's images directory
* Showing the pictures contained in the selected directory
* Search function with filters
* Showing and possibility of modifying some properties of a selected picture
* Zooming on a picture if double-clicked

## Functions
For the application, we wondered if using objects would be necessary, we thought that it didn't make too much sense to do so for multiple reasons
* Application is not complex enough
* Most functions were only parsing metadatas or handling text files
* The only objects like entities in the application are pictures, but the properties were parsed and it didn't make sense to put these datas in an object logic

To make the code cleaner, we separated the GUI, functions for the GUI and other functions in 3 different files.
The GUI just calls the functions contained in the 2 other files when they are needed.

