gdbm_compat
===========


Provides a means to open a gdbm database that otherwise gives the "Bad Magic Number" error.

This can be useful when needing to support EL6 and EL7 (or CentOS 6 and CentOS 7).

It supports opening of gdbm files created with gdbm version 1.8 or 1.10. Some functionality may not work on the database, but most will, which is better than none!


The primary method of usage is to use "gdbm_compat.open_compat" in place of "gdbm.open".

For example:

	>>> import gdbm_compat

	>>> ...

	>>> mydb = gdbm.open('mydatabase', 'r') # Database created on different system that wont open

		Traceback (most recent call last):

		File "<stdin>", line 1, in <module>

		gdbm.error: Bad magic number


	>>> mydb = gdbm_compat.open_compat('mydatabase.db', 'r') # Force it to open
    
	<gdbm.gdbm object at 0x7f7da47ee110>



Additional Methods
------------------

Some additional methods are available. You can find the pydoc generated documentation in doc/gdbm_compat.html of the source distribution.


License
-------

gdbm_compat is licensed under Public Domain.
