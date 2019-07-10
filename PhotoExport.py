from tqdm import tqdm
import os, time
import datetime
import argparse
import csv
import shutil
import json


##########################
#   Initial Variables    #
##########################
init = {
    "debugging"             : True,
    "debugging_log"         : {},
    "error_log"             : "/Volumes/Pictures/iphoto-photo-importer/errors.log",
    "debugger_path"         : "/Volumes/Pictures/iPhoto-photo-importer/debuggerLog.json",
    "library_collection"    : "/Volumes/Pictures/iPhoto/2008 - 2015/iPhoto External.photolibrary/Masters",
    "destination"           : "/Volumes/Pictures/NewPhoto",
    "image_file_path"       : "/Volumes/Pictures/iphoto-photo-importer/imageFilePath.csv"
}


def start_CLI():
    """Starts Command Line Interface

    Returns:
        Void -- Starts CLI
    """
    parser = argparse.ArgumentParser(description='Process some directory names.')
    parser.add_argument('directory', metavar='Directory Path', nargs='+',
                       help='Directory Path to the Images')

    args = parser.parse_args()
    # _directory = args.directory[0]
    print('arg parse invoked')

def handleDebug(init):
    if init["debugging"]:
        #print(init["debugging_log"])
        with open(init["debugger_path"], "w") as write_json:
            json.dump(init["debugging_log"], write_json)

def printDebug(statement):
    global init
    if init["debugging"]:
        print(str(datetime.datetime.now()) + " : " + statement)

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


def createFilePath(tupleDate, origin_file_path):
    """Generates File Paths using date convention

    Returns:
        String -- File Path, Destination
    """
    global init
    __destination = init["destination"]
    __file_name = os.path.basename(origin_file_path)
    __directory_path = None

    for item in tupleDate:
        __destination += "/" + str(item)
    
    __directory_path = __destination
    __destination += "/" + __file_name

    return __directory_path, __destination


def getDate(filePath):
    """Gets Created Date then converted into Tuple (only tested on Mac OS)

    Returns:
        Tuple -- (Year, Month, Day)
    """
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
    global init
    file_exists = os.path.isfile(init["image_file_path"])

    with open(init["image_file_path"], 'a') as _csvFile:
        _fieldnames = ['file_path','created_in','destination','destination_path']
        writer = csv.DictWriter(_csvFile, fieldnames=_fieldnames)

        if not file_exists:
            writer.writeheader()
        writer.writerows(collections)

    init["debugging_log"]["storeIntoCSV"] = "CSV Stored"

def purgeCSV(file):
    global init

    try:
        os.remove(file)
    except:
        pass

    with open(file, "w") as empty_csv:
            pass

    init["debugging_log"]["removeCSV"] = file

def drillDownFolders(directory):
    """Recursive dryRun Function to reach end of the file path
    """
    global init

    _folders = []
    _files = []
    _tupleDate = None
    _fileStat = None

    for entry in os.scandir(directory):
        if entry.is_dir():
            _folders.append(entry.path)
            printDebug("[drillDownFolders] Drilling Folders -- " + entry.path)
        elif entry.is_file():
            _tupleDate = getDate(entry.path)
            _fileStat = createFilePath(_tupleDate, entry.path)
            _files.append({'file_path' : entry.path, 'created_in' : _tupleDate, 'destination' : _fileStat[1] , 'destination_path' : _fileStat[0]})
    
    storeIntoCSV(_files)
    
    if _folders:
        for subDirectory in _folders:
            drillDownFolders(subDirectory)

def runCopyImage():
    """Read a CSV File then copy over image files
    """

    # Todo: Change CSV file dynamically

    global init
    _output = {}
    #with open('imageFilePath.csv') as _csvFile:
    csv_file_path = '/volumes/pictures/iphoto-photo-importer/spreadsheet/Image-Collections-2019-07-03.csv'
    with open(csv_file_path) as _csvFile:
        reader = csv.DictReader(_csvFile)
        _reader_rows = list(reader)
        _total_reader_rows = len(_reader_rows)
        for row in tqdm(_reader_rows, total=_total_reader_rows ,desc="Copying image in Progress..."):
            _output["file_path"] = row['file_path']
            _output["destination"] = row['destination']
            copyImageFiles(row['file_path'], row['destination'], row['destination_path'])
    init["debugging_log"]["processCSVFiles"] = _output
    print('Run Copy Image: ',_output)

def logErrors(error_message):
    with open('errors.log', 'a') as _logfile:
        _logfile.write(str(error_message) + "\n")

def copyImageFiles(file_path, destination ,destination_path):
    global init
    _output = {}
    #create destination directory
    try:
        os.makedirs(destination_path)
    except OSError as e:
        logErrors(e)    
    #copy files
    try:
        shutil.copy(file_path, destination)
        _output["Completed"] = file_path
    except IOError as e:
        logErrors(e)
        _output["Failed"] = file_path + ":" + e

    init["debugging_log"]["copyImageFiles"] = _output

def createTransferCatelog():
    global init
    purgeCSV(init["image_file_path"])
    drillDownFolders(init["library_collection"])

## Create Argument for Creating Catelog
#createTransferCatelog()

## Create Argument for Debug parameter
#handleDebug(init)

#start_CLI()

###
# Comment out this method for debug
###
runCopyImage()