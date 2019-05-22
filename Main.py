##SpreadSheet Test
#import SpreadSheet

##
##Spread sheet Tests
##

# spreadsheet = SpreadSheet.SpreadSheet("./test.csv")
# test_collection = [{"file_path":"one", "created_in":"two", "destination":"three","destination_path":"four"},{"file_path":"one", "created_in":"two", "destination":"three","destination_path":"four"}]
# spreadsheet.storeIntoCSV(test_collection)
# spreadsheet.purgeCSV()

##
##Helper Tests
##

# from Helper import Helper
# helper = Helper("/Volumes/Pictures/iPhoto/2008 - 2015/iPhoto External.photolibrary/Masters", "/Volumes/Pictures/iphoto-photo-importer/imageFilePath.csv")
# helper.drillDownFolders(helper.destination)

##
##Collection Tests
##

from LibraryCollection import iPhoto, Photos
from Helper import Helper

# iphoto = iPhoto('imageFilePath.csv','/Volumes/Pictures/iPhoto/2008 - 2015')
# helper = Helper(iphoto.image_path, "/Volumes/Pictures/iphoto-photo-importer/iphoto.csv")
# helper.drillDownFolders(helper.destination)

# photos = Photos('/Volumes/Pictures/iphoto-photo-importer/photos1.csv', '/Volumes/Pictures/iPhoto/2015')
# helper = Helper(photos.image_path, photos.csv_path)
# helper.drillDownFolders(helper.destination)

helper = Helper('/Volumes/NIKON D3300', './test0522.csv', destination_directory = '/Volumes/Pictures/Photos')
helper.drillDownFolders(helper.source_directory)
