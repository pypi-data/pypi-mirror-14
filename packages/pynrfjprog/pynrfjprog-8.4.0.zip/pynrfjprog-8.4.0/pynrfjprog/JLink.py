
from __future__ import division
from __future__ import print_function

from builtins import int

import os
import sys
import os.path
import fnmatch


if sys.platform.lower().startswith('win'):
    _DEFAULT_SEGGER_ROOT_PATH = r'C:\Program Files (x86)\SEGGER'
elif sys.platform.lower().startswith('linux'):
    _DEFAULT_SEGGER_ROOT_PATH = r'/opt/SEGGER/JLink'
elif sys.platform.lower().startswith('dar'):
    _DEFAULT_SEGGER_ROOT_PATH = r'/Applications/SEGGER/JLink'


def find_latest_dll():

    if sys.platform.lower().startswith('win'):
        jlink_software_pack_list = _win_return_jlink_software_packs_in_directory()
        if len(jlink_software_pack_list) == 0:
            return None

        return _win_return_latest_jlinkarm_dll(jlink_software_pack_list)
    
    elif sys.platform.lower().startswith('linux'):
        for filename in os.listdir(_DEFAULT_SEGGER_ROOT_PATH):
            if fnmatch.fnmatch(filename, '*.so.*.*'):
                return os.path.join(_DEFAULT_SEGGER_ROOT_PATH, filename)

    elif sys.platform.lower().startswith('dar'):
        for filename in os.listdir(_DEFAULT_SEGGER_ROOT_PATH):
            if fnmatch.fnmatch(filename, '*.dylib'):
                return os.path.join(_DEFAULT_SEGGER_ROOT_PATH, filename)        


def _win_return_jlink_software_packs_in_directory():
    """
    Return all JLink software packs within the default SEGGER root directory.
    A folder in the directory is determined as a valid JLink software pack if it contains a JLinkArm.dll in its top level.
    """

    jlink_software_pack_list = []
    for jlink_software_pack in os.listdir(_DEFAULT_SEGGER_ROOT_PATH):
        temp = os.path.join(_DEFAULT_SEGGER_ROOT_PATH, jlink_software_pack)
        if os.path.isdir(temp):
            for filename in os.listdir(temp):
                if filename == 'JLinkARM.dll':
                    jlink_software_pack_list.append(jlink_software_pack)

    return jlink_software_pack_list

def _win_return_latest_jlinkarm_dll(jlink_software_pack_list):
    """
    Given a list of all valid JLink software packs within default directory this function will return the full path to the newest released JLinkArm.dll.
    This is determined by the JLink software pack's version number that is assumed to come directly after "_V" in the folder name.
    """

    greatest_version = '0'
    latest_jlink_software_pack = None

    jlink_version_number_identifier = '_V'
    for jlink_software_pack in jlink_software_pack_list:
        version_index = jlink_software_pack.index(jlink_version_number_identifier) + 2
        version = jlink_software_pack[version_index : ]
        if version > greatest_version:
            greatest_version = version
            latest_jlink_software_pack = jlink_software_pack

    return os.path.join(_DEFAULT_SEGGER_ROOT_PATH, latest_jlink_software_pack, 'JLinkARM.dll')
