#!/usr/bin/env python
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
__VERSION__ = "0.6"

import re, eyeD3, sys
from os import path

MIN_ARGS = 0

DESIRED_TAGS = ('Album', 'Artist', 'DiscNum', 'Genre', 'Title', 'TrackNum', 'Year')
_COMMENT = "Tagged by %s v%s from %s" % (path.basename(__file__), __VERSION__, __AUTHOR__)

__sepd = {'sep' : path.sep}
_REGEX_TEXT_DIRECTORY = r"%(sep)s(?P<Artist>[^%(sep)s]+)%(sep)s((?P<Year>\d{4}), )?(?P<Album>[^%(sep)s]+?)( (?P<DiscNum>\d{2}))?%(sep)s(?P<TrackNum>\d{2}) - (?P<Title>[^%(sep)s]+)\.[mM][pP]3$" % __sepd
# only work with the file basename: .*%(sep)s
_REGEX_TEXT_FILENAME = r".*%(sep)s(?P<Artist>[^-]+) - ((?P<Year>\d{4}), )?(?P<Album>[^-]+?)( (?P<DiscNum>\d{2}))? - (?P<TrackNum>\d{2}) - (?P<Title>[^-]+)\.[mM][pP]3$" % __sepd

def getUtf8String(d, key):
    return d[key] if key and d[key] else ""

class autoid3:
    """
    Tries to get all mp3 on current directory (without arguments, if there's
    some argument, use these files) and fill it's id3 data with its filename
    properties.
    Tries to match by the latest directories:
    .../Artist/[Year, ]Album [DiscNum]/TrackNum - Title.mp3
    Has the optional -g option to specify Genre.
    """

    def __init__(self, filename, regex):
        self.__filename = path.realpath(filename)
        self.__regex = regex

    def analyze(self, genre = ""):
        print "Analysing '%s'" % self.__filename
        if not eyeD3.isMp3File(self.__filename):
            raise Exception, "File is not a Mp3 file"
        # get __old_tags
        self.retrieveTags()
        # try to set the __new_tags
        searched = self.__regex.search(self.__filename)
        if not searched:
            # couldn't get __new_tags
            raise Exception, "Couldn't guess tags through filepath"

        d = searched.groupdict()
        # converting d to utf8 before storing in __new_tags
        self.__new_tags = {}
        for key in d.iterkeys():
            if key == 'Year':
                # if unicode the isUpdatable will fail the comparison
                self.__new_tags[key] = d[key] if d[key] else ""
            else:  # to unicode
                self.__new_tags[key] = d[key].decode("utf8") if d[key] else ""

        # but we still miss the genre
        genre_obj = eyeD3.Genre()
        # following line may throw eyeD3.GenreException. Let it be propagated
        genre_obj.parse(genre)
        self.__new_tags["Genre"] = genre  # genre must be str, not unicode (setGenre requirement)

    def getOldTag(self, key):
        return getUtf8String(self.__old_tags, key)
    def getNewTag(self, key):
        return getUtf8String(self.__new_tags, key)

    def isUpdatable(self):
        return self.__new_tags != self.__old_tags

    def deleteOldTag(self):
        if self.__tag.frames:
            # only remove something if there's something
            self.__tag.remove()

    def writeChanges(self):
        tag = self.__tag
        tag.header.setVersion(eyeD3.ID3_V2_3)
        tag.removeComments()
        tag.addComment(_COMMENT)
        for t in DESIRED_TAGS:
            # e.g: tag.setArtist(self.__new_tags['Artist'])
            tag_info = self.__new_tags[t]
            if t == 'TrackNum' or t == 'DiscNum':
                # argument is tuple (TrackNum, TotalTracks) with TotalTracks == None
                eval('tag.set%s((%s, None))' % (t, repr(tag_info)))
            elif t == 'Year':
                tag.setDate(tag_info)  # only put Year
            else:
                # only put as string when it's string
                tag_formatted = repr(tag_info) if type(tag_info) in (unicode, str) else tag_info
                eval('tag.set%s(%s)' % (t, tag_formatted))

        try:
            tag.update(eyeD3.ID3_V2_3)
        except:
            return False

        return True

    def retrieveTags(self):
        "Define self.__old_tags with tag properties from self.__filename"
        tag = self.__tag = eyeD3.Tag()
        # following line may throw exceptions. Let it be propagated
        tag.link(self.__filename)

        self.__old_tags = {}
        for t in DESIRED_TAGS:
            # e.g: self.__old_tags['Artist'] = tag.getArtist()
            if t == 'Genre':
                self.__old_tags[t] = tag.getGenre().getName() if tag.getGenre() else ""
            elif t == 'TrackNum' or t == 'DiscNum':
                number = eval('tag.get%s()' % t)[0]  # Tuple: (TrackNum, TotalTracks)
                self.__old_tags[t] = u'%02d' % number if number else ""
            else:
                self.__old_tags[t] = eval('tag.get%s()' % t)

    def dump(self):
        print "old: %s\nnew: %s" % (repr(self.__old_tags), repr(self.__new_tags))

if __name__ == "__main__":
    from sys import argv, exit
    from os import sep
    from glob import glob
    from optparse import OptionParser

    options = {
        # 'one_letter_option' : ['full_option_name',
            # "Help",
            # default_value],
        'q' : ['quiet',
            "Less verbose",
            False],
        'k' : ['keep-old',
            "Keep old tag info that's not overwritten",
            False],
        'w' : ['write',
            "Write changes to file, if applicable",
            False],
        'g' : ['genre',
            "Insert this genre on this file",
            ""],
        'f' : ['force',
            "Force tag writting even if it has the same tag already",
            False],
        'n' : ['name',
            "Get info from filename: Artist - Year, Album [Disc] - Track - Name.mp3",
            False],
    }

    options_list = ' '.join(["[-%s --%s]" % (o, options[o][0]) for o in options])
    desc = autoid3.__doc__.replace('    ','')
    parser = OptionParser("%%prog %s [file1 file2 file3 ...]" % options_list,
            description=desc,
            version="%%prog %s" % __VERSION__)

    for o in options:
        shorter = '-' + o
        longer = '--' + options[o][0]
        if type(options[o][2]) is bool:
            parser.add_option(shorter, longer, dest=o, help=options[o][1],
                action="store_true", default=options[o][2])
        elif type(options[o][2]) is str:
            parser.add_option(shorter, longer, dest=o, help=options[o][1],
                action="store", type="string", default=options[o][2])

    (opt, args) = parser.parse_args(argv)
    if len(args) < MIN_ARGS + 1:
        # not enough arguments
        print """ERROR: not enough arguments.
Try `%s --help' for more information""" % args[0].split(sep)[-1]
        exit(1)

    # ignore the argv[0]
    files = args[1:] if args[1:] else glob("*.[mM][pP]3")
    if not files:
        print "No files found"

    if not opt.n:  # get tags from directories
        r = re.compile(_REGEX_TEXT_DIRECTORY)
    else:  # get tag from filename
        r = re.compile(_REGEX_TEXT_FILENAME)

    for arg in files:
        id3 = autoid3(arg, r)
        genre = opt.g
        try:
            id3.analyze(genre)
        except:
            print "Error: ", sys.exc_info()[1]
            if not opt.q:
                print u"    Couldn't analyze the file. Quitting..."
            continue

        if not id3.isUpdatable() and not opt.f:
            if not opt.q:
                print u"    No new info to put"
            continue

        if not opt.q:
            print "    File can be updated:"
            for t in DESIRED_TAGS:
                print "     %s: %s => %s" % (t, id3.getOldTag(t), id3.getNewTag(t))

        if opt.w:
            if not opt.k:
                id3.deleteOldTag()

            if not id3.writeChanges():
                print "Writing on the file failed!"
                continue

            if not opt.q:
                print "File has been updated!"
        else:
            print " (use the --write option to write the changes)"
        print
    exit(0)

# vim: set et
