# Appendix

The client asked for a new property that he wants to specify on his pictures, the property "weather".
This short documentation will explain what changes are needed to add this new property

## GUI

### Input

### Search

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
