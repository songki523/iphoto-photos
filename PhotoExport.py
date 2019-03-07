import os, time
import argparse
import csv
import shutil

"""Starts Command Line Interface

Returns:
    Void -- Starts CLI
"""
def start_CLI():
    # parser = argparse.ArgumentParser(description='Process some directory names.')
    # parser.add_argument('directory', metavar='Directory Path', nargs='+',
    #                    help='Directory Path to the Images')

    # args = parser.parse_args()
    # _directory = args.directory[0]
    pass

_directory = '/Volumes/Pictures/iPhoto'
_destination = '/Volumes/Pictures/NewPhoto'
#_csvFile = open('imageFilePath.csv', 'w+')

def isNotDSstore(directoryName):
    return directoryName != ".DS_Store"

#
# Enable when iphoto and photo collections are completed. 
#

# """Gets all the root collections

# Returns:
#     Array of collections -- List of Directories
# """
# def firstRun():
#     _directories = []
#     for fileName in os.listdir(_directory):
#         #check if it's directory else drill in until jpeg
#         if isNotDSstore(fileName):
#             _directories.append(_directory + '/' + fileName)
#     print("Root Directories: " , _directories)
    
#     return _directories

# def getPictures():
#     _root = firstRun()
#     _photoCollections = []
#     _traverseDirectory = ""
#     for fileName in _root:
#         for fileSubName in os.listdir(fileName):
#             if isNotDSstore(fileSubName):
#                 _traverseDirectory = "{0}/{1}/Masters".format(fileName, fileSubName)
#                 _photoCollections.append(_traverseDirectory)
#     print("Collections: \t", _photoCollections)

"""Generates File Paths using date convention

Returns:
    String -- File Path
"""
def createFilePath(tupleDate, origin_file_path):
    __destination = _destination
    __file_name = os.path.basename(origin_file_path)
    __directory_path = None

    for item in tupleDate:
        __destination += "/" + str(item)
    
    __directory_path = __destination
    __destination += "/" + __file_name

    return __directory_path, __destination

"""Gets Created Date then converted into Tuple

Returns:
    Tuple -- (Year, Month, Day)
"""
def getDate(filePath):
    stat = os.stat(filePath)
    timeTuple = None
    try:
        # Checks for File creation date
        timeTuple = time.gmtime(stat.st_birthtime)
    except AttributeError:
        # Get Modified date if creation date can't be found
        print('Attribute Error: ' , filePath)
        timeTuple = time.gmtime(stat.st_mtime)
    # Returns Year, Month, Day 
    return timeTuple[:2]

def storeIntoCSV(collections):
    file_exists = os.path.isfile('imageFilePath.csv')

    with open('imageFilePath.csv', 'a') as _csvFile:
        _fieldnames = ['file_path','created_in','destination','destination_path']
        writer = csv.DictWriter(_csvFile, fieldnames=_fieldnames)

        if not file_exists:
            writer.writeheader()
        writer.writerows(collections)

"""Recursive dryRun Function to reach end of the file path
"""
def dryRun(directory, iteration = 0):
    _folders = []
    _files = []
    _tupleDate = None
    _fileStat = None

    for entry in os.scandir(directory):
        if entry.is_dir():
            _folders.append(entry.path)
        elif entry.is_file():
            _tupleDate = getDate(entry.path)
            _fileStat = createFilePath(_tupleDate, entry.path)
            _files.append({'file_path' : entry.path, 'created_in' : _tupleDate, 'destination' : _fileStat[1] , 'destination_path' : _fileStat[0]})
    
    storeIntoCSV(_files)
    #print("Folders Iterations: {0} \n".format(iteration), "\n".join(_folders))
    #print("Files Iterations: {0} \n".format(iteration), "\n".join(_files))
    
    if _folders and iteration <= 4:
        for subDirectory in _folders:
            dryRun(subDirectory, iteration + 1)

"""Read a CSV File then copy over image files
"""
def processCSVFiles():
    with open('imageFilePath.csv') as _csvFile:
        reader = csv.DictReader(_csvFile)
        for row in reader:
            print(row['file_path'], row['destination'])
            copyImageFiles(row['file_path'], row['destination'], row['destination_path'])

def logErrors(error_message):
    with open('errors.log', 'a') as _logfile:
        _logfile.write(str(error_message) + "\n")

def copyImageFiles(file_path, destination ,destination_path):
    #create destination directory
    try:
        os.makedirs(destination_path)
    except OSError as e:
        logErrors(e)    
    #copy files
    try:
        shutil.copy(file_path, destination)
        print("Completed: " , file_path)
    except IOError as e:
        logErrors(e)
        print("Failed: ", file_path ,e)


# try:
#     os.remove("imageFilePath.csv")
# except:
#     pass

# dryRun2('/Volumes/Pictures/iPhoto/2008 - 2015/iPhoto External.photolibrary/Masters')

processCSVFiles()
