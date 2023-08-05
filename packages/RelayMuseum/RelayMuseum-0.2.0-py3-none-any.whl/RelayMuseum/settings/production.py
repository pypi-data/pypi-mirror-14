from __future__ import absolute_import

import sys

from .base import *

for location in CONFIG_PATH:
    filename = join(location, 'RelayMuseumConf' + '.py')
    if isfile(filename) and getsize(filename) > 0:
        sys.path.append(location)
        from RelayMuseumConf import *
