#!/usr/bin/env python
import os
from plistlib import *
# me
from public import *


@public
def webloc_get(path):
    plist = readPlist(path)
    return plist.URL  # UPPERCASE


@public
def webloc_set(path, url):
    rootObject = dict(URL=str(url))  # UPPERCASE
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
        os.makedirs(dir)
    writePlist(rootObject, path)

if __name__ == "__main__":
    import os
    path = __file__ + ".plist"
    url = "http://www.google.com"
    webloc_set(path, url)
    print(webloc_get(path))
    os.unlink(path)
