import tkinter
from tkinter import filedialog
from LibraryCollection import iPhoto, Photos
from Helper import Helper

# iPhoto Library
# iphoto = iPhoto('imageFilePath.csv','/Volumes/Pictures/iPhoto/2008 - 2015')
# helper = Helper(iphoto.image_path, "/Volumes/Pictures/iphoto-photo-importer/iphoto.csv")
# helper.drillDownFolders(helper.destination)

# Photos Library
# photos = Photos('/Volumes/Pictures/iphoto-photo-importer/photos1.csv', '/Volumes/Pictures/iPhoto/2015')
# helper = Helper(photos.image_path, photos.csv_path)
# helper.drillDownFolders(helper.destination)

# tkinter UI
root = tkinter.Tk()
root.withdraw()

print('Please select the source ... ')

file_source_path = filedialog.askdirectory()

str_destination = '/Volumes/Pictures/Photos'
bool_destination = input('Sending images to ' + str_destination + ' Should I proceed? [yes,no]: \t')

if bool_destination == 'yes':
    print(file_source_path, str_destination)

do_copy_image = input('Proceed with transeferring process? [yes,no]: \t')

if do_copy_image == 'yes':
    print('Initiate printing protocol')

helper = Helper(file_source_path, destination_directory = '/Volumes/Pictures/Photos')
helper.drillDownFolders(helper.source_directory)
