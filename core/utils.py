import sys
import os

def resource_path(relative_path):
    # Get a relative path for resource
    base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))

    return os.path.join(base_path, relative_path)