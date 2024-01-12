# Program to test file_cycler
# Go through the specified directory and look for
# files with the specified file type.
# print the next file name every 2 seconds

import argparse
import sys
import time
import traceback

from file_cycler import get_next_file

parser = argparse.ArgumentParser(
    description="Program to test the file_cycler module"
    ,epilog="More information and source code at https://github.com/makeralchemy/slow-movie-player-python"
    )
parser.add_argument("directory" 
    ,default="."
    ,help="Look in this directory"
    )
parser.add_argument("-t", "--file-type"
    ,default=None
    ,help="Only list files with this type"
    )

args = parser.parse_args()    
directory = args.directory
file_type = args.file_type

if file_type:
    print(f"Scanning directory '{directory}' for '{file_type}' files.")
else:
    print(f"Scanning for all files in directory '{directory}'")

next_file_function = get_next_file(directory,filetype=file_type)

try:
    while True:
        file_returned = next_file_function()
        if file_returned: 
            print(file_returned) # Get first file
            time.sleep(1)
        else:
            if file_type:
                print(f"No files in with type '{file_type}' in directory '{directory}' or directory '{directory}' does not exist")
            else:
                print(f"No files in directory '{directory}' or directory '{directory}' does not exist")
            break

except KeyboardInterrupt:
    print("\n")

except Exception as e:
    print(f"Unexpected exception!\n{traceback.format_exc()}")
    # print(traceback.format_exc())

