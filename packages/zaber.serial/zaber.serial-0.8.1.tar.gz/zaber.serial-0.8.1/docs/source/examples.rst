Examples
########

ASCII
=====

Setting Up an AsciiSerial and Homing All Devices
------------------------------------------------

The `AsciiSerial` class models a serial port. All of the devices
connected to this serial port are assumed to be using the Zaber ASCII
Protocol.

To send what we call a "global" command, we must send a command to
device 0. All Zaber devices will always respond to commands addressed
to device 0. The `AsciiCommand` class has a default device address of 0.
If we do not specify a device address, then the address of the command
will be set to 0.

So, in order to connect to our serial port and home all devices, we
need to create an `AsciiSerial` object, and an `AsciiCommand` object to
send::

    # Assume that our serial port can be found at /dev/ttyUSB0.
    port = AsciiSerial("/dev/ttyUSB0")
    command = AsciiCommand("home")

    port.write(command)

At this point, we have achieved our goal of homing all devices. However,
each device has sent a reply acknowledging that it received a command.
These replies are now available in the input buffer of the port. We can
use our `AsciiSerial` to read those messages::

    # Assume that we have 3 devices connected.
    ndevices = 3

    for i in range(0, ndevices):
        port.read()

In the above example, ``port.read()`` returns an `AsciiReply` containing
the reply read from a device. We discard this reply by not assigning it
to a variable. In production-quality code, it is recommended that you
always check replies for errors. This is demonstrated in the next
example.

Checking Replies for Errors
---------------------------

In the last example, we sent a global "home" command to 3 devices. We
the read and discarded the replies the devices sent. It is recommended
to always check the reply for errors. These can appear in two places in
a reply: the "Reply Flag" and "Warning Flag" fields. 

Replies read using `AsciiSerial.read()` will be returned in the form of
`AsciiReply` objects. The `AsciiReply` class provides easy access to the
reply and warning flags through its ``reply_flag`` and ``warning_flag``
attributes.

Let's first check the reply flag of our reply. The ``reply_flag``
attribute will always contain a string of length 2, whose value is
either "OK" or "RJ". A value of "RJ" indicates that the command which
caused this reply to be sent was rejected. The "data" field (accessible
through the ``data`` attribute of `AsciiReply`) will contain the reason
for the rejection. See the `Reply section of the ASCII Protocol Manual`_
for a complete list of rejection reasons. Here is an example of a simple
check for command rejection::

    # Assume that we have an AsciiSerial object called "port".
    reply = port.read()

    if reply.reply_flag == "RJ":
        print("A command was rejected! Reason: {}".format(reply.data))

The warning flag is also always a string of length 2. When there are no
warnings to display, then the field will contain ``"--"``. If not, then
the field will contain one of the 2-letter warning flags described in
the `Warning Flags section of the ASCII Protocol Manual`_. The following
code checks the ``warning_flag`` attribute for problems::

    if reply.warning_flag != "--":
        print("Warning received! Flag: {}".format(reply.warning_flag))

.. _Reply section of the ASCII Protocol Manual: http://www.zaber.com/wik
    i/Manuals/ASCII_Protocol_Manual#Replies
.. _Warning Flags section of the ASCII Protocol Manual: http://www.zaber
    .com/wiki/Manuals/ASCII_Protocol_Manual#Warning_Flags

Sending Commands Using AsciiDevice
----------------------------------

The `AsciiDevice` class is intended to represent a single Zaber device.
It provides a blocking, one-message-at-a-time method for sending
commands and receiving replies. The `AsciiDevice.send()` function will
send a command to the device, and then wait for a reply. Once it
receives that reply, it will return it in the form of an `AsciiReply`.

`AsciiDevice.send()` accepts either a string or an `AsciiCommand` as an
argument. In either case, the function will overwrite the device address
to be the address of the `AsciiDevice`. This allows you to omit the
device number when sending commands, like so::

    # Assume we have an AsciiSerial called "port".
    device = AsciiDevice(port, 1)

    # All of the following are equivalent.
    device.send("home")
    device.send("1 home")
    device.send(AsciiCommand("home"))
    device.send(AsciiCommand(1, "home"))

In rare cases, this may result in some unexpected behaviour. Consider
the following::

    # A full, properly-formatted ASCII command string,
    # specifying the "home" command, addressed to device 2.
    command_string = "/2 0 home\r\n"
    command_obj = AsciiCommand(command_string)

    # This device has an address of 1.
    device1 = AsciiDevice(port, 1)

    # What happens when a command with address 2
    # is sent by a device with address 1?
    device1.send(command_obj)

In the above example, a command created to be sent to device 2 is sent
using an `AsciiDevice` with address 1. The `AsciiDevice.send()`
function will change the address of the command to its own address 
before sending the command.

Working With Individual Axes Using AsciiAxis
--------------------------------------------

Some Zaber devices have multiple axes. Just as `AsciiDevice` models a
single Zaber device using the ASCII protocol, `AsciiAxis` models a
single axis of a Zaber device. An `AsciiAxis` must have a parent
`AsciiDevice`. A new `AsciiAxis` can be created either by using
`AsciiDevice.axis()`, or by using the `AsciiAxis` constructor.

Once you have created your `AsciiAxis`, you can send commands to it just
like you can to an `AsciiDevice`::

    # Assume we have an AsciiDevice called "device".
    axis1 = device.axis(1)
    axis2 = device.axis(2)

    axis1.send("home")

The PollUntilIdle Function
--------------------------

In the Zaber ASCII Protocol, devices respond as soon as they have
understood a command. This means that we need to poll the device to see
if it has finished executing a command. The 
`AsciiDevice.poll_until_idle()` and `AsciiAxis.poll_until_idle()`
functions are provided specifically for this purpose. They will block
code execution until the device reports itself as idle, polling the
device at a regular interval::

    # Tell the device to move a fairly large distance.
    device.send("move rel 10000")

    # Wait for the device to finish moving.
    device.poll_until_idle()

"Sugar" Functions
-----------------

`AsciiDevice` also provides some convenience functions for sending the
most common commands to the device. These include functions to home the
device, and to send the "move" commands::

    device = AsciiDevice(port, 1)

    device.home()
    device.move_rel(2000)

Note that in the above example, we do not call ``poll_until_idle()``.
The "sugar" functions will block until the device has finished moving,
with the exception of ``move_vel``, which returns immediately. The 
``move_abs``, ``move_rel``, and ``move_vel`` functions also take an
optional argument, ``blocking``, which will cause the function to return
immediately if it is set to ``False``. If set to ``True``, the function
will poll the device until it is idle.

A Longer Example
----------------

Here's an example script that you should be able to copy to a file and run::

    from zaber.serial import AsciiSerial, AsciiDevice, AsciiCommand, AsciiReply
    import time

    # Helper to check that commands succeeded.
    def check_command_succeeded(reply):
        """
        Return true if command succeeded, print reason and return false if command
        rejected
    
        param reply: AsciiReply
    
        return: boolean
        """
        if reply.reply_flag != "OK": # If command not accepted (received "RJ") 
            print ("Danger! Command rejected because: {}".format(reply.data))
            return False
        else: # Command was accepted
            return True


    # Open a serial port. You may need to edit this section for your particular
    # hardware and OS setup.        
    port = AsciiSerial("/dev/ttyUSB0")  # Linux
    #port = AsciiSerial("COM3")         # Windows

    # Get a handle for device #1 on the serial chain. This assumes you have a
    # device already in ASCII 115,220 baud mode at address 1 on your port.
    device = AsciiDevice(port, 1) # Device number 1

    # Home the device and check the result.
    reply = device.home()
    if check_command_succeeded(reply):
        print("Device Homed.")
    else:
        print("Device home failed.")
        exit(1)

    # Make the device has finished its previous move before sending the 
    # next command. Note that this is unnecessary in this case as the 
    # AsciiDevice.home command is blocking, but this would be required if 
    # the AsciiDevice.send command is used to trigger movement.
    device.poll_until_idle()

    # Now move the device to a non-home position.
    reply = device.move_rel(2000) # move rel 2000 microsteps
    if not check_command_succeeded(reply):
        print("Device move failed.")
        exit(1)

    # Wait for the move to finish.
    device.poll_until_idle()

    # Read back what position the device thinks it's at.
    reply = device.send("get pos")
    print("Device position is now " + reply.data)

    # Clean up.
    port.close()



Binary
======

Setting Up a BinarySerial and Homing All Devices
------------------------------------------------

The `BinarySerial` class models a serial port. All of the devices
connected to this serial port are assumed to be using the Zaber Binary
Protocol.

To send a "home" command to all devices, we send a command to device
number 0. All Zaber devices will always respond to commands sent to 
device number 0.

We can use the `BinaryCommand` class to easily encode commands to be
sent using the Binary Protocol. In the Binary Protocol, "home" is
command number 1. So, we can send a "home" command (command number 1) 
to all devices (device number 0) like so::

    # Assume that our serial port can be found at /dev/ttyUSB0.
    port = BinarySerial("/dev/ttyUSB0")

    # Device number 0, command number 1.
    command = BinaryCommand(0, 1)

    port.write(command)

In the Binary Protocol, a device does not respond until it has completed
a movement. Once the devices have finished homing, they will each
respond. We can listen for these responses like so::

    # Assume that we have 3 devices connected.
    ndevices = 3

    for i in range(0, ndevices):
        port.read()

In the above example, ``port.read()`` returns a `BinaryReply` containing
the reply read from a device. We discard this reply by not assigning it
to a variable. In production-quality code, it is recommended that you
always check that the replies you receive are not error messages
indicating that something has gone wrong. This is demonstrated in the 
next example.

Checking Replies for Errors
---------------------------

In the Binary Protocol, devices may send messages at any time indicating
that they have encountered an error. Error messages always have a
command number of 255. The data field of the message will contain one of
the error codes specified in the `Error section of the Binary Protocol
Manual`_.

In order to check if a device encountered an error, we must check that
the reply's ``command_number`` attribute is not 255. If it is 255, then
we must examine the data of the reply to determine what has gone wrong.
The following example demonstrates this::

    # Assume that we have a BinarySerial object called "port".
    reply = port.read()

    if reply.command_number == 255:
        print("An error occurred in device {}. Error code: {}".format(
                reply.device_number, reply.data))

.. _Error section of the Binary Protocol Manual: http://www.zaber.com/wi
    ki/Manuals/Binary_Protocol_Manual#Error_-_Cmd_255
        
Using BinaryDevice to Send Commands
-----------------------------------

The `BinaryDevice` class serves to model a single Zaber device using the
Binary Protocol. It provides a selection of "sugar" functions to send
some of the most common commands to a device. The following example
creates a new `BinaryDevice` and sends it the "move absolute" and 
"move relative" commands::

    # Assume we have a BinarySerial object called "port".
    device = BinaryDevice(port, 1)

    device.move_abs(300)
    device.move_rel(1000)

The `BinaryDevice` class can also be used to send any command to the
device, using `BinaryDevice.send()`. `BinaryDevice.send()` accepts 
either a `BinaryCommand` object, or several integers representing a
command to be sent. For example, the "reset" command is command number
0. To send the reset command, we can do the following::

    device.send(0)

`BinaryDevice.send()` will always overwrite the device number of a
command to be sent. This can result in some unexpected behaviour in 
certain cases. Consider the following code::

    # "device2" has a device number of 2.
    device2 = BinaryDevice(port, 2)

    # "command" is addressed to device number 1.
    command = BinaryCommand(1, 21, 1000)

    # Should the command be sent to device 1, or device 2?
    device2.send(command)

In the above case, the command's ``device_number`` attribute will be
overwritten by ``device2`` to be 2. The command will be sent to device 
2, despite being originally addressed to device 1.

This edge case can be used to your advantage. Consider the following::

    command = BinaryCommand(0, 55, 1234)

    device1 = BinaryDevice(port, 1)
    device2 = BinaryDevice(port, 2)
    device3 = BinaryDevice(port, 3)

    device1.send(command)
    device2.send(command)
    device3.send(command)

One command can be sent to multiple devices easily by relying on
`BinaryDevice.send()` to properly set the device number.

A Longer Example
----------------

Here's an example script that you should be able to copy to a file and run::

    from zaber.serial import BinarySerial, BinaryDevice, BinaryCommand, BinaryReply
    import time

    # Helper to check that commands succeeded.
    def check_command_succeeded(reply):
        """
        Return true if command succeeded, print reason and return false if command
        rejected
    
        param reply: BinaryReply
    
        return: boolean
        """
        if reply.command_number == 255: # 255 is the binary error response code.
            print ("Danger! Command rejected. Error code: " + str(reply.data))
            return False
        else: # Command was accepted
            return True
        

    # Open a serial port. You may need to edit this section for your particular
    # hardware and OS setup.        
    port = BinarySerial("/dev/ttyUSB0")  # Linux
    #port = BinarySerial("COM3")         # Windows

    # Get a handle for device #1 on the serial chain. This assumes you have a
    # device already in Binary 9,600 baud mode at address 1 on your port.
    device = BinaryDevice(port, 1) # Device number 1

    # Home the device and check the result.
    reply = device.home()
    if check_command_succeeded(reply):
        print("Device Homed.")
    else:
        print("Device home failed.")
        exit(1)

    # Note that unlike the ASCII example, there is no poll_until_idle() call
    # here. This is because in the Binary protocol, device replies do not
    # arrive until after the device has completed the command.

    # Now move the device to a non-home position.
    reply = device.move_rel(2000) # move rel 2000 microsteps
    if not check_command_succeeded(reply):
        print("Device move failed.")
        exit(1)

    # Read back what position the device thinks it's at.
    reply = device.send(60, 0) # Return current position command.
    print("Device position is now " + str(reply.data))

    # Clean up.
    port.close()


What Now?
=========

If you need more info, then continue on to the `zaber.serial` API
reference pages, or check out the `advanced-topics` page.
