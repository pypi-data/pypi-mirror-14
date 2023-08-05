# :coding: utf-8
# :copyright: Copyright (c) 2016 Martin Pengelly-Phillips

import sys

from . import entry_point


if __name__ == '__main__':
    if '__main__.py' in sys.argv[0]:
        sys.argv[0] = 'ringfencer'

    entry_point.main(sys.argv[1:])
