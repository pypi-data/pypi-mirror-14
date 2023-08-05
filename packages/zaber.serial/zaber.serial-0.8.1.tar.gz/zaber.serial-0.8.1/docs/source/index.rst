.. The Zaber Serial Library in Python documentation master file, created by
   sphinx-quickstart on Thu Mar 19 13:06:09 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

The Zaber Serial Library in Python
==================================

Introduction
------------

The Zaber Serial Library is a small Python library for communicating with Zaber
devices over a serial port. It is built on top of `PySerial`_.

The library is compatible with Python 2.7 and 3.4. It is released under the
`Apache License`_.

.. _`PySerial`: https://github.com/pyserial/pyserial
.. _`Apache License`: http://apache.org/licenses/LICENSE-2.0

Contents
--------

.. toctree::
   :maxdepth: 3
   
   getting-started
   examples
   API reference <zaber.serial>
   advanced-topics

Installation
------------

The Zaber Serial Library can be installed from the `Python Package Index`_
using ``pip``::

    pip install zaber.serial

Once the installation finishes, you can use the library by importing it in any
Python file::
    
    import zaber.serial

Or directly import just the classes you want::
    
    from zaber.serial import AsciiSerial, AsciiDevice, AsciiCommand

.. _`Python Package Index`: https://pypi.python.org/pypi


Known Issues
------------

- AsciiSerial and BinarySerial constructors fail when used with pyserial versions later than 2.7, because of `this bug`_, which looks like it may be fixed in the next release after 3.0.1. Until then we recommend manually installing pyserial 2.7::

    pip uninstall pyserial
    pip install pyserial==2.7

.. _`this bug`: https://github.com/pyserial/pyserial/issues/59
  


Release Notes
-------------

v0.8.1:
  - Fixed a Python 3 specific problem with passing strings to BinarySerial.write()

v0.8: 
  - Fixed AsciiReply failure to correctly parse some valid ASCII info messages.
  - Allow passing URLs as well as port names to the AsciiSerial and BinarySerial constructors.
  - Made API documentation link more prominent in help landing page.
  - Added a Change Log section to README and help langing page.
  - Fixed help landing page link for PySerial to point to current version.
  - Clarified which TimeoutError implementation can be thrown by the serial port classes' read methods - it's zaber.serial.TimeoutError and not either of the builtin ones.
  - Added a type check to the AsciiSerial constructor to make sure the port argument is a string. The BinarySerial constructor already had the same.
  - Exposed inter-character timeout via optional arguments to the AsciiSerial and BinarySerial constructors. This allows increasing the timeout to avoid spurious errors on overloaded computers.
  - Set the AsciiReply.reply_flag attribute to None in the cases of info and alert messages. It wasn't being defined at all before, which was inconsistent.
  - Added debug-level logging of receive timeouts.
  - BinaryDevice.send() will now return replies with message IDs if the commands passed in have message IDs.
  - BinaryReply will now sign-extend 24 bits of data to 32 bits if message IDs are enabled. This will still produce incorrect data if the actual value requires more than 24 bits, but it will now correctly handle negative numbers that fit in 24 bits.
  - BinarySerial.write() will now work if passed a string, as indicated by its documentation.
  - Added flush() methods to the AsciiSerial and BinarySerial classes. These just call the flush() method of the underlying serial ports.
  - Added more complete example scripts to the online documentation.
     
v0.7: 
  - Fixed AsciiReply raising StopIterationError instead of ValueError when parsing incomplete strings.
  - Fixed AsciiReply incorrectly rejecting single digit checksums.

v0.6: 
  - Added message logging.
  - Fixed a bytes vs. string issue in Python 3.
  - Added module index to documentation.

v0.5: 
  - Assorted documentation and packaging improvements.

up to v0.4: Initial internal development.

Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

