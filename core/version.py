VERSION = "v0.0.1"
VERSION_SHORT = "v0.1"

def get_version(short=False):
    return VERSION_SHORT if short else VERSION
