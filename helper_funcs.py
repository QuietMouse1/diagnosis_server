import os
import collections 

# scandir_out is the output of os.scandir 
# scandir output gives a list of string with 'DirEntry <file_name>' this func removes Dir entry from the list
def format_scandir_output(scandir_out):
    dir_list = []
    file_list = []
    for entry in scandir_out :
        if entry.is_dir():
            dir_list.append(entry.name)
        if entry.is_file():
            file_list.append(entry.name)

    scandir_out.close()
    return dir_list, file_list

def get_latest_dir(scandir_out):
    dir_list = []
    file_list = []
    for entry in scandir_out :
        if entry.is_dir():
            dir_list.append(entry.name)
        if entry.is_file():
            file_list.append(entry.name)

    scandir_out.close()
    return dir_list, file_list

def sortandlist_os_scandir(out):
    dirs_dct = {}
    files_dct = {}
    for entry in out:
        if entry.is_dir():
            dirs_dct[os.path.getctime(entry)] = entry.name # sorting by key is easier (?) than sorting by values
            print (os.path.getctime(entry), entry.name)
        if entry.is_file():
            files_dct[os.path.getctime(entry)] = entry.name # sorting by key is easier (?) than sorting by values
            print (os.path.getctime(entry), entry.name)

    
    sorted_dirs_dct = collections.OrderedDict(sorted(dirs_dct.items())) # sort them using ordered dict
    sorted_dirs_list = list(sorted_dirs_dct.values())
    sorted_file_dct = collections.OrderedDict(sorted(files_dct.items())) # sort them using ordered dict
    sorted_file_list = list(sorted_file_dct.values())

    return sorted_dirs_list, sorted_file_list
