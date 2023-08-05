gdbm_compat
===========


Provides a means to open a gdbm database that otherwise gives the "Bad Magic Number" error.

This can be useful when needing to support EL6 and EL7 (or CentOS 6 and CentOS 7).

It supports opening of gdbm files created with gdbm version 1.8 or 1.10. Some functionality may not work on the database, but most will, which is better than none!


The primary method of usage is to use "gdbm_compat.open_compat" in place of "gdbm.open".

For example:

	>>> import gdbm_compat

	>>> ...

	>>> mydb = gdbm_compat.open_compat('mydatabase.db', 'r')
    
    <gdbm.gdbm object at 0x7f7da47ee110>

