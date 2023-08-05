#!/usr/bin/env python3
import os
import sys
import subprocess
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from IptcEditor.src import gui_gtk_glade as gui

# ensure exiv2 is installed on system
try:
    examine = subprocess.Popen(['exiv2', '--version'], stdout=subprocess.PIPE, shell=False)
    output, error = examine.communicate()
except FileNotFoundError:
    print('Exiv2 does not appear to be installed on your host system! Please install it before typing again.')
    sys.exit(1)

if __name__ == '__main__':
    gui.GuiGtkGlade()