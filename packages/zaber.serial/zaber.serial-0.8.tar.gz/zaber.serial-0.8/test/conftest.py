# A special file for pytest fixtures. 
# All fixtures defined here are accessible to
# all test_*.py files in this directory.

import pytest, os

from deviceemulator import FakePort
from zaber.serial import AsciiSerial, BinarySerial

# We need to create fakeport here first so that 
# the slave pty can be given to the *serial fixtures.
fakeport = FakePort()

@pytest.yield_fixture(scope="module")
def asciiserial():
    with AsciiSerial(os.ttyname(fakeport.slave)) as s:
        yield s

@pytest.yield_fixture(scope="module")
def binaryserial():
    with BinarySerial(os.ttyname(fakeport.slave)) as s:
        yield s

@pytest.fixture(scope="module")
def fake():
    return fakeport
