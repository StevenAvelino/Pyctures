# Appendix

The client asked for a new property that he wants to specify on his pictures, the property "weather".
This short documentation will explain what changes are needed to add this new property

## GUI 

For the GUI, we must add the weather field.
It will therefore be necessary to create a new label and input.
A reorganisation of the bottom part of the application will be necessary.
 
For the good functioning of the field, it is necessary to add a getter and setter method according to the definition of the functions of the application.
 
For the setter, it is necessary to link the event when the focus is out of the weather field.

## Functions

The functions in the functions files that we need to edit so we can add the metadata "weather"
 
### Search

The search function needs to add the metadata "weather" to the default search without any filters.
The JSON file also needs to include the new weather metadata on the generation of the file.

### Metadatas

First, searching for a metadata to store the property "weather" will be needed. When it's done, 3 functions will need to be changed so we can add the metadata "weather".
* Function to get the metadata
* Function to set the metadata
* Function to edit the JSON
* Rename function

Adding the metadata in the get/set metadata should be easy if we know which metadata to change.
For the JSON, adding the set metadata to the already existing structure of the function.
For the rename, just set the metadata to a default value like the other metadatas.

## Client

In order for the client's application to be updated as a result of our modifications, it will be necessary to reinstall the application with the new installer.