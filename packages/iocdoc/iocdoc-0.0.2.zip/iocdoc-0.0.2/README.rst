IOCDOC: Document the configuration of an EPICS IOC
==================================================

*iocdoc*: Document the configuration of an EPICS IOC

:docs: http://iocdoc.readthedocs.org
:git:  https://github.com/prjemian/iocdoc/

The user will provide the directory path (absolute or relative)
to an EPICS IOC startup command file.  
The IOC startup file will specify the starting point to discover
the configuration of each IOC.

This code will parse the startup command file
and discover the commands and databases used to start the IOC.
An attempt is made to read the database files.  This program will
report if a file or database is not found.

The goal is to generate a set of WWW pages with appropriate
links to standard documentation for all the commands and other
common support.  Links will be made to any local documentation
provided in the ./documentation directory of the top level directory.
