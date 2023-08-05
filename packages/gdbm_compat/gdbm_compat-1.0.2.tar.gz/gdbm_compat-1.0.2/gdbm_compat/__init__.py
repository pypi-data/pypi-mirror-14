'''
    The following code is Public Domain.

    Written by Tim Savannah, 2016.

    The following methods allow you to use a gdbm database of a different version. It may not work in all cases, but is better than a flat-out error.
'''

import atexit
import os
import tempfile

__all__ = ('convert_to_1_10', 'convert_to_1_8', 'replace_magic_number', 'get_magic_number', 'is_1_8', 'is_1_10', 'open_compat')


MAGIC_1_8 = b'\xce\x9aW\x13'
MAGIC_1_10 = b'\xcf\x9aW\x13'

__version__ = '1.0.2'

__version_tuple__ = (1, 0, 2)



def open_compat(filename, mode="r"):
    '''
        open - Allows opening a gdbm database, supporting either 1_8 or 1_10, as much as the current platform can.

            A temporary copy is created, and will be removed when your program exists.

        @return - gdbm.gdbm object of the database
    '''
    if mode and mode != "r":
        raise ValueError('Only "r" is supported mode in gdbm_compat.')

    try:
        import gdbm
    except ImportError:
        raise ImportError('gdbm module not found.')

    if not os.path.exists(filename) or not os.access(filename, os.R_OK):
        raise ValueError('Cannot open %s for reading.' %(filename,))

    global _opened_dbs, _registered

    if _registered is False:
        atexit.register(_atexit_hook)
        _registered = True

    ret = None
    newLoc = None
    try:
        return gdbm.open(filename, "r")
    except:
        pass

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
        
    _opened_dbs.append(newLoc)
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

