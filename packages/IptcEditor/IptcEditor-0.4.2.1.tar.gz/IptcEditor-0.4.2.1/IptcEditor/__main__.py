import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from IptcEditor.src import gui_gtk_glade as gui

if __name__ == '__main__':
    gui.GuiGtkGlade()
