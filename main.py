import sys
from gui import main as gui_main
from cli import main as cli_main

if len(sys.argv) > 1:
    # If arguments are provided, assume CLI mode.
    cli_main()
else:
    # If no arguments, launch the GUI.
    gui_main()
