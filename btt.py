#!/usr/bin/python
# encoding: utf-8

from __future__ import unicode_literals

import os
import sys
import glob
from workflow import Workflow3

wf = None
log = None

nothing_found_error_text = 'Nothing found'


def main(wf):

    import json

    log.info(wf.datadir)
    log.info('Workflow response complete')

    if len(wf.args):
        query = wf.args[0]
    else:
        query = "Get Gestures"
        app = "Script Debugger"


    with open("Master Preset.json", "r") as read_file:
        bttData = json.load(read_file)

    presets = bttData.get('BTTPresetContent')

    if query == "Get Apps":

        appNames = getAppNames()

        for p in presets:
            name = p.get('BTTAppName')
                                                                # TODO - Set global icon to network icon
            if name == "Finder":
                iconPath = "/System/Library/CoreServices/Finder.app"
                _icontype = "fileicon"
            elif name == "Global":
                iconPath = "images/GlobalAppIcon.icns"
                _icontype = "file"
            elif (name + ".app") in appNames:
                iconPath = "/Applications/" + name + ".app"
                _icontype = "fileicon"
            else:
                iconPath = "images/BlankAppIcon.png"
                _icontype = "file"

            wf.add_item(title=name,
                        subtitle="View gestures for '{query}'",
                        arg=name,
                        autocomplete=name,
                        valid=True,
                        icon=iconPath,
                        icontype=_icontype)


    elif query == "Get Gestures":

        # app = 'Script Debugger'
        app = os.environ['theApp']

        appfound = False
        for p in presets:
            if p.get('BTTAppName') == app:
                appfound = True
                break

        if appfound == True:
            name = p.get('BTTAppName')
            triggers = p.get('BTTTriggers')
            iconpath = getAppIcon(name)
            if name == 'Global':
                _icontype = "file"
            else:
                _icontype = "fileicon"

            for t in triggers:
                # try:
                if 'BTTGestureNotes' in t:

                    if t.get('BTTGestureNotes') != "" and "==" not in t.get(
                            'BTTGestureNotes') and "FAVORITE AVAILABLE" not in t.get('BTTGestureNotes'):
                        sub = t.get('BTTTriggerTypeDescription')

                        if 'BTTRequiredModifierKeys' in t:
                            try:
                                if t.get('BTTRequiredModifierKeys') == 524288:
                                    modKey = "⌥"
                                elif t.get('BTTRequiredModifierKeys') == 1048576:
                                    modKey = "⌘"
                                elif t.get('BTTRequiredModifierKeys') == 262144:
                                    modKey = "⌃"
                                elif t.get('BTTRequiredModifierKeys') == 8388608:
                                    modKey = "Fn"
                                else:
                                    modKey = "?"

                                sub = modKey + "\t+\t" + sub
                            except Exception:
                                pass

                        if 'BTT4FingerTapSequence' in t:
                            try:
                                tap = t.get('BTT4FingerTapSequence')
                                tap = str(tap)
                                tap = "[" + tap[1] + "][" + tap[3] + "][" + tap[5] + "][" + tap[7] + "]"

                                sub = sub + ":\t" + tap
                            except Exception:
                                pass

                        wf.add_item(title=t.get('BTTGestureNotes'),
                                    subtitle=sub,
                                    arg=t.get('BTTGestureNotes'),
                                    autocomplete=name,
                                    valid=True,
                                    icon=iconpath,
                                    icontype=_icontype)
                # except Exception:
                #     pass
        else:
            wf.add_item(title="App not found!",
                        subtitle="doodalee",
                        valid=False)

    wf.add_item(title="Update BTT Presets",
                subtitle="Choose if the presets seem old",
                arg="update presets",
                valid=True,
                icon="icon.png",
                icontype="filepath")
    return wf.send_feedback()




def getAppNames():
    p = "/Applications/"
    appNames = []
    os.chdir(p)

    for file in glob.glob("*.app"):
        appNames.append(file)

        os.chdir("/Applications/Utilities/")

    for file in glob.glob("*.app"):
        appNames.append(file)

    return appNames


def getAppIcon(name):
    if name == "Finder":
        iconPath = "/System/Library/CoreServices/Finder.app"
        _icontype = "fileicon"
    elif name == "Global":
        iconPath = "images/GlobalAppIcon.icns"
        _icontype = "file"
    elif (name + ".app") in getAppNames():
        iconPath = "/Applications/" + name + ".app"
        _icontype = "fileicon"
    else:
        iconPath = "images/BlankAppIcon.png"
        _icontype = "file"
    return iconPath


def getGestures(appName, presets):

    appfound = False
    for p in presets:
        if p.get('BTTAppName') == appName:
            appfound = True
            break

    if appfound == True:
        name = p.get('BTTAppName')
        triggers = p.get('BTTTriggers')
        iconpath = getAppIcon(name)
        _icontype = "file"

        for t in triggers:
            try:
                if t.get('BTTGestureNotes') != "" and "==" not in t.get('BTTGestureNotes') and "FAVORITE AVAILABLE" not in t.get('BTTGestureNotes'):
                    sub = t.get('BTTTriggerTypeDescription')

                    try:
                        if t.get('BTTRequiredModifierKeys') == 524288:
                            modKey = "⌥"
                        elif t.get('BTTRequiredModifierKeys') == 1048576:
                            modKey = "⌘"
                        elif t.get('BTTRequiredModifierKeys') == 262144:
                            modKey = "⌃"
                        elif t.get('BTTRequiredModifierKeys') == 8388608:
                            modKey = "Fn"
                        else:
                            modKey = "something"

                        sub = modKey + "\t\t" + sub

                    except Exception:
                        pass

                    try:
                        tap = t.get('BTT4FingerTapSequence')
                        tap = t.str(tap)
                        tap = "[" + tap[1] + "][" + tap[3] + "][" + tap[5] + "][" + tap[7] + "]"

                        sub = sub + ":\t" + tap
                    except Exception:
                        pass

                    wf.add_item(title=t.get('BTTGestureNotes'),
                                subtitle=sub,
                                arg=t.get('BTTGestureNotes'),
                                autocomplete=name,
                                valid=True,
                                icon=iconpath,
                                icontype=_icontype)
            except Exception:
                pass
    else:
        wf.add_item(title="App not found!",
                    subtitle="doodalee",
                    arg=name,
                    valid=False)


if __name__ == "__main__":
    wf = Workflow3()
    log = wf.logger
    sys.exit(wf.run(main))
