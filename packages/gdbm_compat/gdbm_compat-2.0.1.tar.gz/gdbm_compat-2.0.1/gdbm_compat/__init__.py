'''
    The following code is Public Domain.

    Written by Tim Savannah, 2016.

    The following methods allow you to use a gdbm database of a different version. It may not work in all cases, but is better than a flat-out error.
'''

import atexit
import os
import tempfile

__all__ = ('open_compat', 'convert_to_1_10', 'convert_to_1_8', 'replace_magic_number', 'get_magic_number', 'is_1_8', 'is_1_10', 'get_gdbm_module')


MAGIC_1_8 = b'\xce\x9aW\x13'
MAGIC_1_10 = b'\xcf\x9aW\x13'

__version__ = '2.0.1'

__version_tuple__ = (2, 0, 1)



def open_compat(filename, mode="r"):
    '''
        open - Allows opening a gdbm database, supporting either 1_8 or 1_10, as much as the current platform can.


            @param filename <str> - Path to gdbm file to open
            @param mode <str> - Must be "r"

            A temporary copy is created, and will be removed automatically when your program exists

        @return - gdbm.gdbm object of the database
    '''
    if mode and mode != "r":
        raise ValueError('Only "r" is supported mode in gdbm_compat.')

    # May raise ImportError if we can't find gdbm module
    gdbm = _get_gdbm_module()

    if not os.path.exists(filename) or not os.access(filename, os.R_OK):
        raise ValueError('Cannot open %s for reading.' %(filename,))


    try:
        return gdbm.open(filename, "r")
    except:
        pass


    newLoc = None
    magicNumber = get_magic_number(filename)
    if magicNumber == MAGIC_1_8:
        newLoc = convert_to_1_10(filename)
    elif magicNumber == MAGIC_1_10:
        newLoc = convert_to_1_8(filename)
    else:
        # Incase we can't repr the value..
        try:
            raise ValueError('Unknown gdbm database magic number: "%s"' %(repr(magicNumber),))
        except:
            raise ValueError('Unknown gdbm database magic number.')
    
    # Register the atexit hook to remove this temp file
    register_for_cleanup(newLoc)

    return gdbm.open(newLoc, "r")


def replace_magic_number(filename, newMagic):
    '''
        replace_magic_number - Generate a new gdbm copy of the given gdbm, which contains the provided magic number.

        <return> - Filename of new file, old contents with provided magic number. 
    '''
    with open(filename, 'rb') as f:
        contents = f.read()

    output = tempfile.NamedTemporaryFile(delete=False)
    output.write(newMagic)
    output.write(contents[4:])
    output.flush()
    output.close()

    return output.name

def convert_to_1_10(filename):
    '''
        convert_to_1_10 - Convert a gdbm database to format 1.10

        Returns a filename of the converted database.
    '''
    return replace_magic_number(filename, MAGIC_1_10)
    
def convert_to_1_8(filename):
    '''
        convert_to_1_8 - Convert a gdbm database to format 1.8

        Returns a filename of the converted database
    '''
    return replace_magic_number(filename, MAGIC_1_8)


def get_magic_number(filename):
    '''
        get_magic_number - Gets the magic number associated with the gdbm database filename provided

        @return <bytes> - Bytes of magic number
    '''
    with open(filename, 'rb') as f:
        magic = f.read(4)
    return magic
    
def is_1_10(filename):
    '''
        is_1_10 - Checks if database is in 1.10 format
    '''
    return bool(get_magic_number(filename) == MAGIC_1_10)
    
def is_1_8(filename):
    '''
        is_1_8 - Checks if database is in 1.8 format.
    '''
    return bool(get_magic_number(filename) == MAGIC_1_8)

global _opened_dbs
_opened_dbs = []

global _registered
_registered = False

def register_for_cleanup(filename):
    '''
        register_for_cleanup - Adds a filename that will be automatically removed when the program exists (for temp db copies)
    '''   
    global _opened_dbs, _registered
    if _registered is False:
        atexit.register(_atexit_hook)
        _registered = True

    _opened_dbs.append(filename)

def get_gdbm_module():
    '''
        get_gdbm_module - Returns the "gdbm" module, supporting both python2 and python3 core modules.

        @return - The module

        @raises - ImportError if cannot find under "gdbm" or "dbm.gnu"
    '''
    try:
        return __import__('gdbm')
    except ImportError:
        pass
    try:
        return __import__('dbm.gnu').gnu
    except:
        raise ImportError('Cannot find gdbm module as either "gdbm" or "dbm.gnu"')

def _atexit_hook(*args, **kwargs):
    '''
        _atexit_hook - The hook registered when gdbm_open converts a database, to clean up the temp databases.
    '''
    global _opened_dbs
    for fname in _opened_dbs:
        try:
            os.unlink(fname)
        except:
            pass

