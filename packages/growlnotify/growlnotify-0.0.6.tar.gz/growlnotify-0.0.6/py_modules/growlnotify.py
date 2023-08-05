#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from platform import system
from fullpath import *
from isstring import *
from osx_only import *
from subopen import *
from public import *


@osx_only
@public
def growlnotify(title=None, message=None, app=None,
                sticky=False, icon=None, image=None, url=None):
    if title and not isstring(title):
        title = str(title)
    if not message:
        message = ""
    if message and not isstring(message):
        message = str(message)
    # if message and isstring(message):
        #message = message.encode("utf-8")
    if title and title[0] == "-":
        title = "\\" + title
    # if title and isstring(title):
        #title = title.encode("utf-8")
    if not message and not title:
        title = ""
    args = []
    if title:
        args += ["-t", title]
    if app:
        args += ["-a", app]
    if icon:
        args += ["--icon", icon]
    if image:
        args += ["--image", fullpath(image)]
    if sticky:
        args += ["-s"]
    if url:
        args += ["--url", url]
    #executable = find_executable("growlnotify")
    # if not executable:
       # err = "growlnotify executable not found"
        #raise OSError(err)
    stdin = message
    # need first growlnotify arg for correct app icon
    args = ["growlnotify"] + args
    returncode, stdout, stderr = subopen(["killall", "-s", "Growl"])
    if returncode != 0:
        returncode, stdout, stderr = subopen(["open", "-a", "Growl 2"])
        if returncode != 0:
            raise OSError(stderr)
    # known errors:
    # We failed to notify after succesfully registering
    # fix Failed to register with
    # ----
    # 1) different versions produce diffrent errors
    # 2) pirate versions contains additional errors
    # repeat few until 0 exit status
    i = 0
    while i < 50:
        returncode, stdout, stderr = subopen(args, stdin=stdin)
        if returncode == 0:
            return
        if not (stderr.find("Failed to register with") >=
                0 or stderr.find("failed to notify") >= 0):
            return
        i += 1

if __name__ == "__main__":
    # Darwin/Linux/Windows,Java
    if system() == "Darwin":
        growlnotify("title")
        growlnotify("unicode".encode("utf8"))
        growlnotify("title", message="message")
        growlnotify(
            "title",
            message="message",
            app="Finder",
            url="file://%s" %
            os.environ["HOME"])
