import os
import time
from SpreadSheet import SpreadSheet

class Helper:
    def __init__(self, destination, new_path):
        self.destination = destination
        self.new_path = new_path

    def createFilePath(self, tupleDate, origin_file_path):
        #Generates File Paths using date convention

        __destination = self.destination
        __file_name = os.path.basename(origin_file_path)
        __directory_path = None

        for item in tupleDate:
            __destination += "/" + str(item)
        
        __directory_path = __destination
        __destination += "/" + __file_name

        return __directory_path, __destination

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
                _tupleDate = self.getBirthDate(entry.path)
                _fileStat = self.createFilePath(_tupleDate, entry.path)
                _files.append({'file_path' : entry.path, 'created_in' : _tupleDate, 'destination' : _fileStat[1] , 'destination_path' : _fileStat[0]})
        
        spread_sheet = SpreadSheet(self.new_path)
        spread_sheet.storeIntoCSV(_files)
        
        if _folders:
            for subDirectory in _folders:
                self.drillDownFolders(subDirectory)
    