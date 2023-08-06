doppel
======

**doppel** copies files or directories to a destination directory,
similar to `*install(1)* <http://linux.die.net/man/1/install>`__.

Usage
-----

To copy files or directories, just list the sources as arguments
followed by the destination: ``doppel src1 src2 dst``. By default, if
only one source is specified, it is copied *onto* the destination; if
multiple sources are specified, they are copied *into* the destination.
This default can be explicitly specified with ``-o/--onto`` or
``-i/--into``, respectively.

If you wish to create any parent directories as needed, pass
``-p/--parents``. You can also set the file mode by passing an octal
mode with ``-m/--mode``.

License
-------

This project is licensed under the BSD 3-clause license.


