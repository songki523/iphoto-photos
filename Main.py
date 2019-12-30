import sys
import tkinter
import os
from tkinter import filedialog
from LibraryCollection import iPhoto, Photos
from Helper import Helper
from PhotoExport import runCopyImage

# iPhoto Library
# iphoto = iPhoto('imageFilePath.csv','/Volumes/Pictures/iPhoto/2008 - 2015')
# helper = Helper(iphoto.image_path, "/Volumes/Pictures/iphoto-photo-importer/iphoto.csv")
# helper.drillDownFolders(helper.destination)

# Photos Library
# photos = Photos('/Volumes/Pictures/iphoto-photo-importer/photos1.csv', '/Volumes/Pictures/iPhoto/2015')
# helper = Helper(photos.image_path, photos.csv_path)
# helper.drillDownFolders(helper.destination)

# Constant
app_destination = '/Volumes/Pictures/iphoto-photo-importer'
str_destination = '/Volumes/Pictures/Photos'
nikon_destination = '/Volumes/Pictures/Photos/Nikon D700'

# Select either Nikon or Fuji
device_choice = input('Which Camera? [nikon, fuji]:  ')
if device_choice == 'fuji':
    pass
if device_choice == 'nikon':
    str_destination = nikon_destination
if device_choice not in ['fuji','nikon']:
    sys.exit('no device selected')

# Objects
helper = Helper(destination_directory=str_destination, app_directory=app_destination)
# tkinter UI
root = tkinter.Tk()
root.withdraw()

# Ask User to Collect image file path to csv file
bool_destination = input('Sending images to ' + str_destination + ' Should I proceed? [yes,no]: \t')

if bool_destination == 'yes':
    # Asking User to select the source
    print('Please select the source ... ')
    file_source_path = filedialog.askdirectory()

    # Digging in the folders
    print(file_source_path, str_destination)
    helper.source_directory = file_source_path    
    helper.drill_down_folders(helper.source_directory)

    print('image paths saved into csv file.')
    os.system('open {}/spreadsheet'.format(app_destination))

elif bool_destination == 'no':
    print('Skipping CSV transfer process ...')

else:
    sys.exit('Invalid Response')

# Ask User to Transfer the image
prompt = 'Copying images referencing from ' + helper.CSV_file + '... \n Proceed with transeferring process? [yes,no]: '
do_copy_image = input(prompt)

if do_copy_image == 'yes':
    # start print process
    print('Initiate printing protocol')
    runCopyImage(helper.CSV_file)

elif do_copy_image == 'no':
    # stop
    print('Please select the spreadsheet ... ')
    file_source_path = filedialog.askdirectory()
    print(file_source_path)
else:
    print('Stop printing process')