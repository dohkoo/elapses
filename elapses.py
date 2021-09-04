#!/usr/bin/env python
# Simple unity indicator for a stop watch to track time.
# author: Stesha Doku | stesha@steshadoku.com
# Last Updated Sept 4, 2021
# Intended for Python3

import vars

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk as gtk
from gi.repository import GObject as gobject
#import gtk
gi.require_version("AppIndicator3", "0.1")
from gi.repository import AppIndicator3 as appindicator
import os
import sys
import time, datetime
from datetime import timedelta
import signal

signal.signal(signal.SIGINT, signal.SIG_DFL)

if __name__ == "__main__":

    timestart = time.time()
    saveseconds = 0
    dir_path = os.path.dirname(os.path.realpath(__file__))
    source_id = ""
    isrunning = False
    alltimes = []


    def on_timer(args=None):
        savetime = int(time.time() - timestart) + saveseconds
        ind.set_label(str(timedelta(seconds=savetime)), "Elapses")
        return True

    def finish(args=None):
        sys.exit()
        return True

    def stoptime(args=None):
        # print(source_id)
        global saveseconds, isrunning
        saveseconds += int(time.time() - timestart)
        gobject.source_remove(source_id)
        isrunning = False
        return True

    def starttime(args=None):
        global timestart
        global isrunning
        timestart = time.time()
        global source_id
        source_id = gobject.timeout_add(1000, on_timer)
        isrunning = True
        return True

    def clear(args=None):
        global saveseconds
        global isrunning, alltimes
        if isrunning == True:
            saveseconds += int(time.time() - timestart)
        timestring = str(timedelta(seconds=saveseconds))
        itemfin = gtk.MenuItem(timestring)
        itemfin.show()
        menu.append(itemfin)
        alltimes.append(timestring+"\n")

        # reset everything
        saveseconds = 0
        isrunning = False
        ind.set_label(str(timedelta(seconds=0)), "Elapses")
        gobject.source_remove(source_id)
        return True

    def exportlist(args=None):
        global saveseconds
        global isrunning, alltimes
        if isrunning == True:
            saveseconds += int(time.time() - timestart)
        print(alltimes)
        makeFolder(vars.logfolder)
        file_obj = open(vars.logfolder + "timelog_"+ datetime.datetime.now().strftime("%m%d%y_%H%M%S")+".txt", "at")
        file_obj.write(str(datetime.datetime.now().strftime("%B %d, %Y at %H:%M:%S"))+"\n")
        file_obj.write("------------------------------\n")
        file_obj.writelines(alltimes)
        file_obj.close()

    def makeFolder(folder):
        from pathlib import Path
        Path(folder).mkdir(parents=True, exist_ok=True)

    ind = appindicator.Indicator.new("simple-clock-client", os.path.abspath(dir_path+"/hourglass.svg"), appindicator.IndicatorCategory.SYSTEM_SERVICES)
    ind.set_status(appindicator.IndicatorStatus.ACTIVE)

    #ind.set_status(appindicator.STATUS_ACTIVE)
    ind.set_label("Elapses", "Elapses")
    menu = gtk.Menu()

    item2 = gtk.MenuItem("Stop")
    item2.connect("activate", stoptime)  # exit if stop added
    item2.show()
    menu.append(item2)

    item3 = gtk.MenuItem("Start")
    item3.connect("activate", starttime)  # exit if stop added
    item3.show()
    menu.append(item3)

    item5 = gtk.MenuItem("Export List")
    item5.connect("activate", exportlist)  # exit if stop added
    item5.show()
    menu.append(item5)

    item4 = gtk.MenuItem("Restart Timer")
    item4.connect("activate", clear)  # exit if stop added
    item4.show()
    menu.append(item4)

    item = gtk.MenuItem("Exit")
    item.connect("activate", finish)  # exit if stop added
    item.show()
    menu.append(item)

    item6 = gtk.MenuItem("--------------------")
    item6.show()
    menu.append(item6)

    ind.set_menu(menu)
    gtk.main()
