# encoding: utf-8, division
from __future__ import print_function, division

import os

def guess_path_to_msconvert():

    try:
        import _winreg
    except ImportError:
        return None
    try:
        key = _winreg.OpenKeyEx(_winreg.HKEY_CLASSES_ROOT, "*\\shell\\Open with MSConvertGUI\\command")
    except WindowsError:
        return None
    value = _winreg.QueryValue(key, None)
    l, __, __ = value.partition('" ')
    path = l.lstrip('"')

    path = os.path.abspath(path)
    folder = os.path.dirname(path)
    path_to_msconvert = os.path.join(folder, "msconvert.exe")

    return path_to_msconvert if os.path.exists(path_to_msconvert) else None

