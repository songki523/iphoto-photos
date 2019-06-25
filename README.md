# Photo Export Application
## Interactive Commandline Application design to extract exisitng photos from iPhoto packages into folder based structures to standerized platform agnostics. 
## NOTE: only been tested in mac environment. 
## In Progress
- Create a interactive commandline interface
- Read and extract data from iPhoto package
- Read and extract data from apple Photos package
- Add parameter to runCopyImage()
- Create task steps. 1. Create .csv file 2. Iterate csv then copy files
## Completed
- Read and extract data from SD card
- Add Progress Bar
## Steps
1. Instianciate helper class (image path, csv file name, destination if path is different) `helper = Helper('/Volumes/NIKON D3300', './test0522.csv', destination_directory = '/Volumes/Pictures/Photos')`
2. Create a csv file `helper.drillDownFolders(helper.source_directory)`
3. Validate csv file
4. Copy over image files `python -c 'import PhotoExport; PhotoExport.runCopyImage()'`
### version-1.0 is current branch