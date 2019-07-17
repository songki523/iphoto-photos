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

# tkinter UI
root = tkinter.Tk()
root.withdraw()

print('Please select the source ... ')

file_source_path = filedialog.askdirectory()

str_destination = '/Volumes/Pictures/Photos'

## Ask User to Collect image file path to csv file
bool_destination = input('Sending images to ' + str_destination + ' Should I proceed? [yes,no]: \t')

if bool_destination == 'yes':
    print(file_source_path, str_destination)

    helper = Helper(file_source_path, destination_directory = '/Volumes/Pictures/Photos')
    helper.drillDownFolders(helper.source_directory)

    print('image paths saved into csv file.')
    os.system('open ./spreadsheet')

elif bool_destination == 'no':
    print('Skipping CSV transffer process ...')

else:
    print('Invalid Response')

## Ask User to Transfer the image
prompt = 'Copying images referencing from ' + helper.CSV_file + '... \n Proceed with transeferring process? [yes,no]: '
do_copy_image = input(prompt)

if do_copy_image == 'yes':
    #start print process
    print('Initiate printing protocol')
    runCopyImage(helper.CSV_file)

elif do_copy_image == 'no':
    #stop
    print('Please select the spreadsheet ... ')
    file_source_path = filedialog.askdirectory()
    print(file_source_path)
else:
    print('Stop printing process')