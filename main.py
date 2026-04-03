import ctypes
import sys

from PySide6.QtWidgets import QApplication

from core.version import get_version
from ui.pages.home_page import HomePage

if __name__ == '__main__':
    print(f"LazyShutdown {get_version()} has been launched.")

    # Creating app
    app = QApplication(sys.argv)

    # Setting new(main) window
    window = HomePage()
    window.show() # Showing this window (what a dumb writing this comm)

    # Trying to set window icon
    try:
        appid = 'RED-IGLA.LazyShutdown'
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(appid)
    except AttributeError:
        pass

    # Endless app cycle
    sys.exit(app.exec())