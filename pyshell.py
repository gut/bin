#!/bin/env python

# GPLv3 License
# Developed by Joao Sebastiao Bueno (gwidion@gmail.com)

import os

class CommandException(Exception):
    pass

class _Command(object):
    def __init__(self, name):
        self.command = name
        object.__init__(self)

    def __call__(self, command_line=""):
        process = os.popen("%s %s" % (self.command, command_line))
        text = process.read()
        code = process.close()
        if code:
            raise CommandException("%s exited with code %d" % (self.command, code))
        return text

class C(object):
    def __getattribute__(self, name):
        return _Command(name)

c = C()