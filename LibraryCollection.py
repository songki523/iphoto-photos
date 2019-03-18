import os
import shutil
import csv

class LibraryCollection:

    def isNotDSstore(self, directoryName):
        return directoryName != ".DS_Store"

    def copyImageFiles(self, file_path, destination ,destination_path):

        _output = {}
        #create destination directory
        try:
            os.makedirs(destination_path)
        except OSError as e:
            print(e)    
        #copy files
        try:
            shutil.copy(file_path, destination)
            _output["Completed"] = file_path
        except IOError as e:
            print(e)
            _output["Failed"] = file_path + ":" + e

        #Debug
        #init["debugging_log"]["copyImageFiles"] = _output

    def iterateCSVRows(self):
        #Read a CSV File then copy over image files

        _output = {}
        with open('imageFilePath.csv') as _csvFile:
            reader = csv.DictReader(_csvFile)
            for row in reader:
                _output["file_path"] = row['file_path']
                _output["destination"] = row['destination']
                self.copyImageFiles(row['file_path'], row['destination'], row['destination_path'])
        
        # Debug
        #init["debugging_log"]["processCSVFiles"] = _output

class iPhoto(LibraryCollection):
    def __init__(self, source_path):
        self.source_path = source_path
        self.collection_name = 'iphoto External.photolibrary'
        self.image_path = self.source_path + "/" + self.collection_name  + "/Masters"

class Photos(LibraryCollection):
    def __init__(self, source_path):
        self.source_path = source_path
        self.collection_name = 'Photos Library.photoslibrary'
        self.image_path = self.source_path + "/" + self.collection_name  + "/Masters"