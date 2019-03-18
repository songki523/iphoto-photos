import sys
import os,csv

class SpreadSheet:
    """Spread Sheet Class created for the task

    Attributes
    ----------
    file_path : str
        file paths to create SpreadSheet
    
    """
    def __init__(self, file_path):
        self.file_path = file_path

    def storeIntoCSV(self, collections):
        """Append rows into CSV Files
        
        Parameters
        ----------
        collections : dict
        
        """

        file_exists = os.path.isfile(self.file_path)

        with open(self.file_path, 'a') as _csvFile:
            _fieldnames = ['file_path','created_in','destination','destination_path']
            writer = csv.DictWriter(_csvFile, fieldnames=_fieldnames)

            if not file_exists:
                writer.writeheader()
            writer.writerows(collections)

        # Debugging
        print('Storing CSV files Completed in : ', self.file_path)

    def purgeCSV(self):
        """[void] Empty ouf the CSV file"""

        try:
            os.remove(self.file_path)
        except:
            pass

        with open(self.file_path, "w") as empty_csv:
                pass

        ## Debugging
        print('Purging CSV Files: ', self.file_path)