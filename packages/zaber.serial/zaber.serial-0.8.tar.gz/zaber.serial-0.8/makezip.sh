#!/usr/bin/env zsh

VERSION=`awk '/version/ { print substr($3, 2, 3) }' setup.py`

zip -r zaber-core-serial-python-v${VERSION}.zip . --include README.rst DESCRIPTION.rst LICENSE.txt setup.py zaber/\* --exclude \*/.svn/\* \*/__pycache__/\*
