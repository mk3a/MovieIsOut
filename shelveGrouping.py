#!/usr/bin/env python3
# shelveGrouping.py
# Extends Shelve module by allowing a user to use a shelveFile as a collection of groups
# and then allowing modification of these groups .
# For example : This module can be used to create groups of web addresses and allow easy modification
# of these groups

# addToGroup(shelveFileName,groupname,elements)             adds to group if group already exits,otherwise creates new groupname
# removeFromGroup(shelveFileName,groupname,elements)        removes elements from group, raises exceptions if group or element not found
# listgroups(showall=False)                                 if
# showall=true shows groups and their elements,otherwise just the
# groupnames


import shelve
import pprint


def addToGroup(shelveFileName, groupname, elements):
    if len(elements) == 0:
        print('No elements in arguments')
        return

    shelfFile = shelve.open(shelveFileName)
    shelfFile.setdefault(groupname, [])
    if shelfFile[groupname] is None:
        shelfFile[groupname] = []
    shelfFile[groupname] += elements
    shelfFile[groupname] = list(set(shelfFile[groupname]))
    print(str(len(elements)) + ' elements added to Group : ' + groupname)
    shelfFile.close()


def removeFromGroup(shelveFileName, groupname, elements):
    if len(elements) == 0:
        print('No elements in arguments')
        return

    shelfFile = shelve.open(shelveFileName)
    if groupname not in shelfFile:
        print(groupname + ' not found ')
        return
    for element in elements:
        templist = shelfFile[groupname]
        try:
            templist.remove(element)
            print('Removed ' + element + ' from ' + groupname)
        except:
            print(element + ' not found')
        shelfFile[groupname] = templist
    shelfFile.close()


def listgroups(shelveFileName, showall=False):
    shelfFile = shelve.open(shelveFileName)
    if showall:
        pprint.pprint(dict(shelfFile))
    else:
        pprint.pprint(list(shelfFile.keys()))
    shelfFile.close()




