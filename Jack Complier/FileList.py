"""
    Given a directory, or file name, FileReader will return 
"""

import os


def list_of_valid_files(file_or_directory_name: str, extension: str):
    """
        If a directory name is provided, check that the directory exisits and return
        a list of all files with a given extension
        If a file name is provided, check the file extension and return in list
        if the file exists.
    """

    resultsList = []

    # check if a directory has been pased
    if os.path.isdir(file_or_directory_name):
        for files in os.listdir(file_or_directory_name):
            if files.split(".")[-1] == extension:
                resultsList.append(file_or_directory_name + "/" + files)
    elif os.path.exists(file_or_directory_name):
        if file_or_directory_name.split(".")[-1] == extension:
            resultsList.append(file_or_directory_name)
    
    return resultsList

if __name__ == "__main__":
    cwd = os.getcwd()
    print(list_of_valid_files(cwd + '/Test Folder', "txt"))
    print(list_of_valid_files(cwd + '/Test Folder/test3.hack', "jack"))