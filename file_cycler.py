import os

def get_next_file(directory, filetype=None):
    """
    Module used to get the names of files in a directory.
    File names are returned in sorted order and the code handles
    the situation where files are added or deleted between calls.
    After retrieving the last file in the directory, the next call
    will got back to the top of the directory and return the first
    file name.
    
    You can optionally specify a specific file type and only those
    files will be returned.    
    
    Example usage:
    	from file_cycler import get_next_file
    	next_file_function = get_next_file("/path/to/directory")
    	print(next_file_function()) # Get first file
    	print(next_file_function()) # Get second file
    	# ... and so on
    """
    last_file = None
    
    def next_file():
        nonlocal last_file
        
        # Make sure the directory exists, if not return None
        if not(os.path.exists(directory)):
            return None       
        
        # Get the current list of files
        files = sorted(os.listdir(directory))
        
        # if a file type was specified, only look at those files
        if filetype:
             files = [f for f in files if f.endswith("." + filetype)]    
        
        if not files:
            # Return None if the directory is empty
            return None
            
        if last_file in files:
            # Find the index of the last file returned
            last_index = files.index(last_file)
            # Calculate the index of the next file
            next_index = (last_index + 1) % len(files)
        else:
        	   next_index = 0
        	   
        # Update last_file
        last_file = files[next_index]
        return last_file
        
    return next_file
