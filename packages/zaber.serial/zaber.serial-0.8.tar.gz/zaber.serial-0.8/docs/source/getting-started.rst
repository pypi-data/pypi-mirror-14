Getting Started
===============

ASCII or Binary?
----------------

The Zaber library is split into ASCII and Binary halves. Depending on
your device, you may need to use one or the other. If your device is
capable of communicating using the ASCII protocol, it is recommended
that you use the ASCII protocol.

It is a good idea to familiarize yourself with the manual for your
protocol of choice before trying to interact with your device. Links
are provided below.

`ASCII Protocol Manual`_

`Binary Protocol Manual`_

Once you have chosen your protocol, you only need to focus your
attention on either the :ref:`ascii-module` or the :ref:`binary-module`.

.. _ASCII Protocol Manual: http://www.zaber.com/wiki/Manuals/ASCII_Proto
    col_Manual
.. _Binary Protocol Manual: http://www.zaber.com/wiki/Manuals/Binary_Pro
    tocol_Manual

Library Structure
-----------------

Regardless of the protocol you choose, the structure of the part of the
library you work with will be essentially the same. There exist the
following four basic structures:

* *Serial*
* *Device*
* *Command*
* *Reply*

Serial
^^^^^^

The *Serial* classes, `AsciiSerial` and `BinarySerial`, are the core
of the library. They are used to communicate with the serial port, and
other classes in the library take them as constructor arguments.

To create a new ``BinarySerial``, you only need to give a valid port
name. In Windows this will be something like ``COM1``, and in Linux and
Mac OS X it will be a path to a file in ``/dev``, like so::

    ser = BinarySerial("/dev/ttyUSB0")

Device
^^^^^^

The *Device* classes are used to represent individual Zaber devices.
A *Device* allows you to interact with Zaber devices directly in your
code. For example, to home a device in the ASCII protocol using an
`AsciiDevice` object called ``device``, you can use the provided
``home()`` function like so::

    device.home()

Only the most common commands are provided as functions. To send more
uncommon commands, the ``send()`` function is provided. For example,
the following code will perform an operation equivalent to the last
example::

    device.send("home")

The `BinaryDevice` class also has ``home()`` and ``send()`` functions
which work just like the ASCII variants shown above.

AsciiAxis
~~~~~~~~~

Only the ASCII half of the library has an `AsciiAxis` class. Zaber's
Binary Protocol does not differentiate between axes and devices, so
there is no ``BinaryAxis`` class. 

An ``AsciiAxis`` can be treated almost identically to an
``AsciiDevice``. Like ``AsciiDevice``, ``AsciiAxis`` provides simple
"sugar" functions to perform common operations like homing and moving
devices, as well as the universal ``send()`` function.

``AsciiDevice`` has a convenient ``axis()`` function which will return
an ``AsciiAxis``::

    # Create a new AsciiAxis with axis number 1, then home axis 1.
    axis = device.axis(1)
    axis.home()
 
Command 
^^^^^^^

The *Command* classes represent commands to be sent to devices. They
provide programmatic access to the different parts of commands, and can
properly encode the data they contain into valid ASCII or Binary 
commands.

The `BinaryCommand` class allows you to create a new ``BinaryCommand``
with the device number, command number, and data value as arguments. The
following code will create a ``BinaryCommand`` to move device number 1
forward by 1000 microsteps::

    # Command 21 is the "Move Relative" command.
    moverel_cmd = BinaryCommand(1, 21, 1000)

ASCII commands, as their name suggests, are comprised entirely of ASCII
text, but the `AsciiCommand` constructor can be used almost identically
to the ``BinaryCommand`` constructor. For example, a "move relative"
command sent to device 1 with a data value of 1000 can be constructed
like so::

    # It is OK to pass integers or strings to the constructor.
    moverel_cmd = AsciiCommand(1, "move rel", 1000)

A single string can also be used to create a new ``AsciiCommand``::

    # This will create an object identical to the last example.
    moverel_cmd2 = AsciiCommand("1 move rel 1000")

Once you have created your *Command* object, you can pass it to either
a *Serial* object to be transmitted::

    # Using the ASCII Protocol, on Windows:
    port = AsciiSerial("COM1")
    moverel_cmd = AsciiCommand(1, "move rel 1000")
    port.write(moverel_cmd)
    
Or you can pass it to a *Device*::

    # Using the Binary Protocol, on Linux:
    port = BinarySerial("/dev/ttyUSB0")
    device = BinaryDevice(port, 1)
    moverel_cmd = BinaryCommand(1, 21, 1000)
    device.send(moverel_cmd)

Reply
^^^^^

The *Reply* classes represent replies received from Zaber devices. It is
rare to ever need to create an instance of a *Reply* class yourself, but
many functions in this library return `AsciiReply` or `BinaryReply`
objects.

For example, say we received an reply from an ASCII device and we want
to check the "warning flag" field to ensure that no errors occurred in
the device. If our ``AsciiReply`` is called ``reply``, then the
following code can be used to check if any warning flag is present::

    # "--" indicates that there are no warnings or errors.
    # If there are any errors, raise the example exception, "MyError".
    if reply.warning_flag != "--":
        raise MyError("Oh no!")

Most attributes of the ``AsciiReply`` class are strings, with the
exception of the ``device_address``, ``axis_number``, and ``message_id``
attributes, which will always be integers.

Next Steps
----------

Continue on to the `examples` page to see some longer example of how to
use this library.
