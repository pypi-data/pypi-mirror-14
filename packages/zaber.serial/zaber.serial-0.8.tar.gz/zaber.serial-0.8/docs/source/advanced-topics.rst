Advanced Topics
===============

This page contains info on features of the library whose documentation
does not merit its own page, and which do not fit into any other page.

Logging
-------

There is some rudimentary logging available for application and system
debugging. Whenever the library reads or writes any data to the serial
port, a debug-level logging message is emitted. 

You can turn on debug-level logging output like so::

    import logging
    logging.basicConfig(level=logging.DEBUG)

If you would like the log messages to be written to a separate file,
then you can specify the file within the ``logging.basicConfig()``
call::

    import logging
    logging.basicConfig(filename='my_log_file.log', level=logging.DEBUG)

For more info on the ``logging`` module, see the `logging HOWTO 
<python:logging-basic-tutorial>` page.
