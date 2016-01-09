#!/usr/bin/env python

#@DESC
'''
This module writes and reads/parses level data in the format defined
below:

OBJECT-TYPE
    X-COORD Y-COORD SPECIAL_ATTRIB

The data reside in a list called item_d


'''

import pickle as p
from const2 import *

def sanitise(string):
    """
    sanitises level data
    """
    ns = ''
    wspace = 0

    for each in string:
        if each != '\n' and each != ' ':
            ns += each
            wspace = 0

        if each == '\n':
            ns += ' '

        if each == ' ' and wspace == 0:
            ns += each
            wspace = 1

    liste = ns.split(' ')
    liste = [each for each in liste if each != '']

    return liste


def write_level():
    """
    Writes the level data
    """
    with open(itemDictFile, 'r') as myFile:
        itemDict = p.load(myFile)

    dumpString = ""

    for itemType in itemDict.keys():
        if itemType != "LEVELWIDTH":
            for item_d in itemDict[itemType]:
                dumpString += itemType + "\n"
                dumpString += "    " + str(item_d[0]) + " " + str(item_d[1]) + \
                              " " + str(item_d[2]) +"\n"

    dumpString += "SCREENSIZE\n"
    dumpString += "    " + str(SCREEN_W) + " " + str(SCREEN_H - PANEL_H) + "\n"
    dumpString += "LEVELWIDTH\n"
    dumpString += "    " + str(itemDict["LEVELWIDTH"]) + "\n"

    with open(levelFile, 'w') as lFile:
        lFile.write(dumpString)


def read_level_file(levelFileName):
    """
    Read level files into the editor for editing saved files.
    By default, level_dump.lvf is read.
    """

    with open(levelFileName, 'r') as lfile:
        
        object_data = lfile.read()
        return sanitise(object_data)



# TO BE USED ONLY BY THE MAIN PROGRAM
def parse_level():
    """
    parses level dump data to create a level
    """

    with open(levelFile, 'r') as lFile:
        dat = lFile.read()

    return sanitise(dat)
