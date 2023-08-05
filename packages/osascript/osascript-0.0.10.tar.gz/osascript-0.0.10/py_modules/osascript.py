#!/usr/bin/env python
# -*- coding: utf-8 -*-
from os.path import *
from platform import system
from subprocess import *
from fullpath import *
from osx_only import *
from public import *
from rm import *
from subopen import *
from temp import *
from tolist import *
from write import *


@osx_only
@public
def osascript(applescript, flags=None):
    """osascript applescript code or file
    """
    args = ["osascript"]
    if applescript and isinstance(applescript, list):
        applescript = "\n".join(applescript)
    temp = programfile = None
    if applescript and exists(applescript) or exists(applescript):
        programfile = applescript
    else:
        temp = programfile = tempfile()
        write(temp, applescript)
    try:
        if flags:
            args += ["-s", flags]
        if programfile:
            args.append(programfile)
        returncode, stdout, stderr = subopen(args)
        return (returncode, stdout, stderr)
    finally:
        rm(temp)


if __name__ == "__main__":
    # Darwin/Linux/Windows,Java
    if system() == "Darwin":
        # test stdout
        returncode, stdout, stderr = osascript('return "message"')
        print(stdout)
        # test stderr
        returncode, stdout, stderr = osascript("log 1")  # log 2 stderr
        print(stderr)
        # test returncode
        returncode, stdout, stderr = osascript("ERROR")
        print(returncode, stderr)
