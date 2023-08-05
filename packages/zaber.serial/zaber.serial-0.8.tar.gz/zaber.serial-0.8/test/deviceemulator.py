import os
import tty
import time
import select
import re
import struct

from zaber.serial import BinaryCommand

class FakePort(object):
    def __init__(self):
        self._master, self.slave = os.openpty()
        tty.setraw(self._master)
        tty.setraw(self.slave)

    def expect(self, pattern, timeout = 5):
        """Block until a match is read from the master pty.

        This function will read in bytes one-at-a-time, append them to
        a buffer, then concatenate the buffer's elements into a string.
        That string will be checked against the pattern provided, and
        if a match is found then the function returns.

        By default, this function has a five-second timeout. If None is
        passed as the timeout argument, then the function will block
        forever until the expected input is read.

        Args:
            pattern: A string containing a regular expression which
                describes the expected input to be read.
            timeout: An integer representing the number of seconds to
                wait before giving up on the match. This wait is an
                inter-byte wait, not a total wait.
        """
        if isinstance(pattern, bytes):
            regex = re.compile(pattern)
        else: regex = re.compile(pattern.encode())
        buffer = bytearray()
        
        # If None is passed for timeout, omit the timeout argument to select.
        # From the docs: "When the timeout argument is omitted the function 
        # blocks until at least one file descriptor is ready."
        selectargs = ([self._master], [], [], timeout) if timeout is not None \
                else ([self._master], [], [])

        while 1:
            r, w, x = select.select(*selectargs)
            if r == []:
                print('Pattern "{0!s}" not found. Read "{1!s}".'.format(
                    pattern, bytes(buffer)))
                raise TimeoutError("Select timed out.")

            c = os.read(self._master, 1)
            buffer.append(ord(c))

            if regex.search(bytes(buffer)):
                break

            time.sleep(0.01)

    def send(self, *args):
        """Send a message from the master pty to the slave.

        Args:
            *args: Between 1 and 3 arguments. If there is only one
                argument, then the string representation (ie. the value
                returned from the object's __str__ function) of the
                argument is written to the serial port.

                If there are two or three arguments, they are assumed
                to be the device number, command number, and data value
                of a Binary command according to Zaber's Binary
                Protocol Manual.
        """
        if len(args) == 0:
            raise TypeError("send() takes at least 1 argument (0 given)")

        # Write whatever is given as a string.
        if len(args) == 1:
            if isinstance(args[0], bytes):
                os.write(self._master, args[0])
            else: os.write(self._master, args[0].encode())

        # Assume 2 or 3 arguments are binary replies and pack them.
        if len(args) == 2:
            os.write(self._master, struct.pack("<2Bl", args[0], args[1], 0))

        if len(args) == 3:
            os.write(self._master, struct.pack("<2Bl", *args))

        if len(args) > 3:
            raise TypeError("send() takes at most 3 arguments")

class TimeoutError(Exception):
    pass

