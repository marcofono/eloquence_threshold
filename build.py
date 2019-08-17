#!/usr/bin/python

import os,re,sys
if (sys.version_info < (3, 0)):
    raise Exception("Python 3 required")
import urllib.request
import shutil
import tempfile
import zipfile

ORIGINAL_FILE_NAME = "eloquence_original.nvda-addon"
FILE_NAME = "eloquence.nvda-addon"

def updateZip(zipname, filename, filedata):
    # generate a temp file
    tmpfd, tmpname = tempfile.mkstemp(dir=os.path.dirname(zipname))
    os.close(tmpfd)

    # create a temp copy of the archive without filename            
    with zipfile.ZipFile(zipname, 'r') as zin:
        with zipfile.ZipFile(tmpname, 'w') as zout:
            zout.comment = zin.comment # preserve the comment
            for item in zin.infolist():
                if item.filename != filename:
                    zout.writestr(item, zin.read(item.filename))

    # replace with the temp archive
    os.remove(zipname)
    os.rename(tmpname, zipname)

    # now add filename with its new data
    with zipfile.ZipFile(zipname, mode='a', compression=zipfile.ZIP_DEFLATED) as zf:
        zf.write(filedata, filename)


if not os.path.exists(ORIGINAL_FILE_NAME):
    with urllib.request.urlopen('https://jeff.tdrealms.com/Add-Ons/Eloquence.nvda-addon') as response:
        with open(ORIGINAL_FILE_NAME, "wb") as f:
            shutil.copyfileobj(response, f)
shutil.copyfile(ORIGINAL_FILE_NAME, FILE_NAME)
updateZip(FILE_NAME, "synthDrivers/eloquence.py", "eloquence.py")
updateZip(FILE_NAME, "synthDrivers/_eloquence.py", "_eloquence.py")
updateZip(FILE_NAME, "manifest.ini", "manifest.ini")
print(f"Created {FILE_NAME}")
