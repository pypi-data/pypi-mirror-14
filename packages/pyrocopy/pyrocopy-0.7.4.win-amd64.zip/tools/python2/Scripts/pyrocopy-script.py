#!C:\tools\python2\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'pyrocopy==0.7.4','console_scripts','pyrocopy'
__requires__ = 'pyrocopy==0.7.4'
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.exit(
        load_entry_point('pyrocopy==0.7.4', 'console_scripts', 'pyrocopy')()
    )
