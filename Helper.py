import os
import time
import datetime
from SpreadSheet import SpreadSheet


class Helper:
    def __init__(self, source_directory='', **kwargs):
        self.parent_directory = kwargs['app_directory']
        self.source_directory = source_directory
        self.CSV_file = self.create_csv_file()
        self.destination_directory = source_directory
        if kwargs['destination_directory']:
            self.destination_directory = kwargs['destination_directory']

    def create_file_path(self, tuple_date, origin_file_path):
        # Generates File Paths using date convention

        __destination = self.destination_directory
        __file_name = os.path.basename(origin_file_path)
        __directory_path = None

        for item in tuple_date:
            __destination += "/" + str(item)
        
        __directory_path = __destination
        __destination += "/" + __file_name

        return __directory_path, __destination

    def create_csv_file(self):
        # Creates CSV Files
        __parent_directory = self.parent_directory + '/spreadsheet/'
        __date_str = datetime.datetime.now().strftime("Image-Collections-%Y-%m-%d")
        __file_extension = '.csv'

        return __parent_directory + __date_str + __file_extension

    @staticmethod
    def get_birth_date(file_path):
        # Gets Created Date then converted into Tuple (only tested on Mac OS)
        stat = os.stat(file_path)
        time_tuple = None
        try:
            # Checks for File creation date
            time_tuple = time.gmtime(stat.st_birthtime)
        except AttributeError:
            # Get Modified date if creation date can't be found
            print('Attribute Error: ', file_path)
            time_tuple = time.gmtime(stat.st_mtime)
        # Returns Year, Month, Day 
        return time_tuple[:2]

    def drill_down_folders(self, directory):

        # Recursive dryRun Function to reach end of the file path

        _folders = []
        _files = []
        _tupleDate = None
        _fileStat = None

        for entry in os.scandir(directory):
            if entry.is_dir():
                _folders.append(entry.path)
                print("[drillDownFolders] Drilling Folders -- " + entry.path)
            elif entry.is_file():
                if self.file_is_image(entry.name):
                    _tupleDate = self.get_birth_date(entry.path)
                    _fileStat = self.create_file_path(_tupleDate, entry.path)
                    _files.append(
                        {
                            'file_path': entry.path,
                            'created_in': _tupleDate,
                            'destination': _fileStat[1],
                            'destination_path': _fileStat[0]
                        }
                    )
        
        spread_sheet = SpreadSheet(self.CSV_file)
        spread_sheet.store_into_csv(_files)
        
        if _folders:
            for subDirectory in _folders:
                self.drill_down_folders(subDirectory)

    @staticmethod
    def file_is_image(entry_name):

        # Validate if file is image
        _return_boolean = True
        # File Extension eg. .NEF .JPG
        _file_extension = entry_name[-3:]
        # Hidden Files eg. ._hidden.JPG
        _file_prefix = entry_name[:2]

        # Checks if file has image extension and not have hidden file prefix
        if _file_extension not in ['NEF','JPG','JPEG'] or _file_prefix == '._':
            _return_boolean = False        
        else:
            print('[FileIsImage] File ', entry_name, 'is an Image')            
        
        return _return_boolean

