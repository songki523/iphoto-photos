import os
import time
import datetime
from SpreadSheet import SpreadSheet

class Helper:
    def __init__(self, source_directory = '', **kwarg):
        self.source_directory = source_directory
        self.CSV_file = self.create_CSV_File()
        self.destination_directory = source_directory
        if kwarg['destination_directory']:
            self.destination_directory = kwarg['destination_directory']

    def createFilePath(self, tupleDate, origin_file_path):
        #Generates File Paths using date convention

        __destination = self.destination_directory
        __file_name = os.path.basename(origin_file_path)
        __directory_path = None

        for item in tupleDate:
            __destination += "/" + str(item)
        
        __directory_path = __destination
        __destination += "/" + __file_name

        return __directory_path, __destination


    def create_CSV_File(self):
        # Creates CSV Files
        __parent_directory = './spreadsheet/'
        __date_str = datetime.datetime.now().strftime("Image-Collections-%Y-%m-%d")
        __file_extension = '.csv'

        return __parent_directory + __date_str + __file_extension


    def getBirthDate(self, filePath):
        #Gets Created Date then converted into Tuple (only tested on Mac OS)
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

    def drillDownFolders(self, directory):
        #Recursive dryRun Function to reach end of the file path

        _folders = []
        _files = []
        _tupleDate = None
        _fileStat = None

        for entry in os.scandir(directory):
            if entry.is_dir():
                _folders.append(entry.path)
                print("[drillDownFolders] Drilling Folders -- " + entry.path)
            elif entry.is_file():
                if self.fileIsImage(entry.name):
                    _tupleDate = self.getBirthDate(entry.path)
                    _fileStat = self.createFilePath(_tupleDate, entry.path)
                    _files.append({'file_path' : entry.path, 'created_in' : _tupleDate, 'destination' : _fileStat[1] , 'destination_path' : _fileStat[0]})
        
        spread_sheet = SpreadSheet(self.CSV_file)
        spread_sheet.storeIntoCSV(_files)
        
        if _folders:
            for subDirectory in _folders:
                self.drillDownFolders(subDirectory)

    def fileIsImage(self, entry_name):
        #Validate if file is image
        _return_boolean = True
        # File Extension eg. .NEF .JPG
        _file_extension = entry_name[-3:]
        # Hidden Files eg. ._hidden.JPG
        _file_prefix = entry_name[:2]

        #Checks if file has image extension and not have hidden file prefix
        if _file_extension not in ['NEF','JPG','JPEG'] or _file_prefix == '._':
            _return_boolean = False        
        else:
            print('[FileIsImage] File ', entry_name, 'is an Image')            
        
        return _return_boolean