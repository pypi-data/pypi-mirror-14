__version__ = "0.1.1"

import sys

class awesome_module:
    def __init__(self):
        if len(sys.argv) > 1:
            if sys.argv[1] == 'tax_evasion':
                print('tax evasion')
        else:
            print('No function called ')