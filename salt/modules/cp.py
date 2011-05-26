'''
Minion side functions for salt-cp
'''
# Import python libs
import os

# Import salt libs
import salt.minion

# Import Third Party Libs
import zmq

def recv(files, dest):
    '''
    Used with salt-cp, pass the files dict, and the destination.

    This function recieves small fast copy files from the master via salt-cp
    '''
    ret = {}
    for path, data in files.items():
        final = ''
        if os.path.basename(path) == os.path.basename(dest)\
                and not os.path.isdir(dest):
            final = dest
        elif os.path.isdir(dest):
            final = os.path.join(dest, os.path.basename(path))
        elif os.path.isdir(os.path.dirname(dest)):
            final = dest
        else:
            return 'Destination unavailable'

        try:
            open(final, 'w+').write(data)
            ret[final] = True
        except IOError:
            ret[final] = False

    return ret

def get_file(path, dest):
    '''
    Used to get a single file from the salt master
    '''
    client = salt.minion.FileClient(__opts__)
    return client.get_file(path, dest)

def cache_files(paths):
    '''
    Used to gather many files from the master, the gathered files will be
    saved in the minion cachedir reflective to the paths retrived from the
    master.
    '''
    client = salt.minion.FileClient(__opts__)
    return client.cache_files(paths)

def cache_file(path):
    '''
    Used to cache a single file in the local salt-master file cache.
    '''
    client = salt.minion.FileClient(__opts__)
    return client.cache_file(path)

def hash_file(path):
    '''
    Return the hash of a file, to get the hash of a file on the
    salt master file server prepend the path with salt://<file on server>
    otherwise, prepend the file with / for a local file.

    CLI Example:
    '''
    client = salt.minion.FileClient(__opts__)
    return client.hash_file(path)
