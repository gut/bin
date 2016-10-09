#!/usr/bin/env python2
# -*- coding: utf-8 -*-

#  Copyright (C) 2010 - Gustavo Serra Scalet <gsscalet@gmail.com>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

__AUTHOR__ = "Gustavo Serra Scalet <gsscalet@gmail.com>"
from os import path, listdir

line_break = lambda level: "\n%s" % ('    ' * level)

class File:
    """Access @filename and @tags for desired information"""
    tags = {}
    def __init__(self, _filename):
        self.filename = _filename
        self.basename = path.basename(_filename)
    def __repr__(self):
        return self.printable(0)
    def printable(self, level):
        return "%s   filename: %s" % (line_break(level), self.basename,)

class Directory:
    """Group of File from the same directory. Check @basename and
    run the iterator for data. The iterator returns first the directories and
    then the files of @basename"""
    directories = []
    files = []

    def __init__(self, _dirname):
        print '__init has %s ' %_dirname
        self.dirname = _dirname
        self.basename = path.basename(_dirname)
        print  '  getting f %s' % listdir(self.dirname)
        for f in listdir(self.dirname):
            fullpath = path.join(self.dirname, f)
            print fullpath
            if path.isfile(fullpath):
                print 'file is %s' % f
                self.addFile(fullpath)
            elif path.isdir(fullpath):
                print 'directory is %s' % f
                self.addDirectory(fullpath)

    def __repr__(self):
        print self.directories
        return self.printable(0)
    def printable(self, level):
        entries = ["\nDirectory: %s" % self.basename,]
        for d in self.directories:
            entries.append(" directories inside: %s" % d.printable(level+1))
        for f in self.files:
            entries.append(" files inside: %s" % f.printable(level+1))
        return line_break(level).join(entries)

    def __len__(self):
        return len(self.files)
    def totalLength(self):
        this_length = len(self)
        for d in self.directories:
            this_length += d.totalLength()
        return this_length

    def addFile(self, new_file):
        to_add = new_file
        if not isinstance(to_add, File):
            to_add = File(to_add)
        self.files.append(to_add)

    def addDirectory(self, new_dir):
        to_add = new_dir
        print 'adding %s' % to_add
        if not isinstance(to_add, Directory):
            print ' creating %s' % to_add
            to_add = Directory(to_add)
        self.directories.append(to_add)

    # iteration properties
    __last_index = 0
    def __iter__(self):
        return self
    def next(self):
        ret = None
        if self.__last_index < len(self.directories):  # get the directory
            ret = self.directories[self.__last_index]
        elif self.__last_index < len(self.directories) + len(self.files):  # get the file
            ret = self.files[self.__last_index - len(self.directories)]
        else:  # ready to reset
            self.__last_index = 0
            raise StopIteration

        self.__last_index += 1
        return ret

