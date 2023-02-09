#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#  Copyright (C) 2022 - Gustavo Scalet <gsscalet@gmail.com>

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

__AUTHOR__ = "Gustavo Scalet <gsscalet@gmail.com>"
__VERSION__ = "0.8"

import re, eyed3, sys, os, logging

# Suppressing warnings being printed like "Non standard genre name"
logging.getLogger("eyed3.id3").setLevel(logging.ERROR)

MIN_ARGS = 0

DESIRED_TAGS = ("album", "artist", "disc_num", "genre", "title", "track_num", "year")
_COMMENT = "Tagged by %s v%s from %s" % (os.path.basename(__file__), __VERSION__, __AUTHOR__)

_REGEX_TEXT_DIRECTORY = r"/(?P<genre>[^/]+)/(?P<artist>[^/]+)/((?P<year>\d{4}), (?P<album>[^/]+)/)?((?P<disc_num>\d)?(?P<track_num>\d{2}) )?(?P<title>[^/]+)\.[Mm][Pp]3$"
# only work with the file basename: .*/
_REGEX_TEXT_FILENAME = r".*/(?P<artist>[^-]+) - ((?P<year>\d{4}), )?(?P<album>[^-]+?) - ((?P<disc_num>\d))?(?P<track_num>\d{2}) (?P<title>[^.]+)\.[Mm][Pp]3$"
_RENAME_FILENAME_FORMAT = "{disc_num}{track_num} {title}.mp3"


class autoid3:
    """
    Tries to get all mp3 on current directory (without arguments, if there's
    some argument, use these files) and fill it's id3 data with its filename
    properties.
    Tries to match by the latest directories:
    .../[Genre]/Artist/[Year, ]Album/[DiscNum]TrackNum Title.mp3
    Has the optional -g option to specify Genre.
    Has the optional -a option to specify Artist.
    """

    def __init__(self, filename, regex, rename_format):
        self.__filename = os.path.realpath(filename)
        self.__regex = regex
        self.__rename_format = rename_format

    def analyze(self, artist="", genre="", prefix_tracknum_in_title=False):
        print("Analysing '%s'" % self.__filename)
        if not eyed3.load(self.__filename):
            raise Exception("File is not a Mp3 file")
        # get _old_tags
        self.retrieveTags()

        if self.__rename_format:
            # this mode is not meant to be changing tags
            if self._old_tags["title"] and self._old_tags["track_num"]:
                # New meaningful name
                self._new_filename = self.__rename_format.format(**self._old_tags)
            else:
                # Keep the old name, otherwise it'll be ' None.mp3'
                self._new_filename = os.path.basename(self.__filename)
            return

        # try to set the _new_tags
        searched = self.__regex.search(self.__filename)
        if not searched:
            # couldn't get _new_tags
            raise Exception("Couldn't guess tags through filepath")

        d = searched.groupdict()
        # store in _new_tags
        self._new_tags = {}
        for key in d.keys():
            # or "" is for overriding None to ""
            self._new_tags[key] = d.get(key, "") or ""

        # but we still miss the genre
        genre_obj = eyed3.id3.Genre()
        # parsing it may throw eyed3.GenreException. Let it be propagated
        if genre:
            genre_obj.parse(genre)
            # genre must be str
            self._new_tags["genre"] = genre
        else:
            genre_obj.parse(self._new_tags["genre"])
            # my genres are comma separated, fix it
            g = str(self._new_tags["genre"])
            g = g.split(", ")
            g.reverse()
            self._new_tags["genre"] = " ".join(g)

        if artist:
            self._new_tags["artist"] = artist

        if prefix_tracknum_in_title:
            tags = self._new_tags
            self._new_tags["title"] = f"{tags['track_num']} {tags['title']}"

    def getOldTag(self, key):
        return self._old_tags.get(key, "")

    def getNewTag(self, key):
        return self._new_tags.get(key, "")

    def isUpdatable(self):
        if hasattr(self, "_new_filename"):
            return os.path.basename(self.__filename) != self._new_filename

        for t in DESIRED_TAGS:
            if self._new_tags[t] != self._old_tags[t]:
                return True
        return False

    def deleteOldTag(self):
        self.__tag.remove(self.__filename)

    def writeChanges(self):
        if self.__rename_format:
            return self.__renameFile()
        elif self.__regex:
            return self.__writeTags()
        else:
            print("Nothing to do")

    def __writeTags(self):
        tag = self.__tag
        tag.header.version = eyed3.id3.ID3_V2_3
        tag.comments.set(_COMMENT)
        for t in DESIRED_TAGS:
            # e.g: tag.setArtist(self._new_tags['Artist'])
            tag_info = self._new_tags[t]
            if t == "track_num" or t == "disc_num":
                # argument is tuple (TrackNum, TotalTracks) with TotalTracks == None
                if tag_info:
                    # do not set an empty metadata
                    setattr(tag, t, (tag_info, None))
            elif t == "year" and tag_info:
                tag.recording_date = eyed3.core.Date(int(tag_info))  # only put Year
            else:
                # only put as string when it's string
                setattr(tag, t, tag_info)

        try:
            tag.save(self.__filename, version=eyed3.id3.ID3_V2_3)
        except:
            return False

        return True

    def __renameFile(self):
        if os.path.isfile(self._new_filename):
            print(f"      NOT overwritting '{self._new_filename}'")
            return False
        try:
            os.rename(self.__filename, self._new_filename)
            return True
        except IOError:
            return False

    def retrieveTags(self):
        "Define self._old_tags with tag properties from self.__filename"
        tag = self.__tag = eyed3.id3.tag.Tag()
        # following line may throw exceptions. Let it be propagated
        tag.parse(open(self.__filename, "rb"))

        self._old_tags = {}
        for t in DESIRED_TAGS:
            # e.g: self._old_tags['Artist'] = tag.getArtist()
            if t == "genre":
                self._old_tags[t] = tag.genre.name if tag.genre else ""
            elif t == "disc_num":
                number = getattr(tag, t)[0]  # Tuple: (TrackNum, TotalTracks)
                self._old_tags[t] = "%1d" % number if number else ""
            elif t == "track_num":
                number = getattr(tag, t)[0]  # Tuple: (TrackNum, TotalTracks)
                self._old_tags[t] = "%02d" % number if number else ""
            elif t == "year":
                year = tag.getBestDate().year if tag.getBestDate() else ""
                self._old_tags[t] = str(year)
            else:
                self._old_tags[t] = getattr(tag, t)

    def dump(self):
        print("old: %s\nnew: %s" % (self._old_tags, self._new_tags))


if __name__ == "__main__":
    from sys import argv, exit
    from os import sep
    from glob import glob
    from optparse import OptionParser

    options = {
        # 'one_letter_option' : ['full_option_name',
        # "Help",
        # default_value],
        "q": ["quiet", "Less verbose", False],
        "k": ["keep-old", "Keep old tag info that's not overwritten", False],
        "w": ["write", "Write changes to file, if applicable", False],
        "g": ["genre", "Insert this genre on this file", ""],
        "a": ["artist", "Insert this artist on this file", ""],
        "f": ["force", "Force tag writting even if it has the same tag already", False],
        "n": ["name", "Get info from filename: Artist - [Year, ]AlbumName - [DiscNumber]TrackNum Title.mp3", False],
        "r": ["rename", "Rename files based on the tags: [DiscNumber]TrackNum Title.mp3", False],
        "c": ["car", "Prefix the TrackNum on Title (MS Sync infotainment workaround)", False],
    }

    options_list = " ".join(["[-%s --%s]" % (o, options[o][0]) for o in options])
    desc = autoid3.__doc__.replace("    ", "")
    parser = OptionParser(
        "%%prog %s [file1 file2 file3 ...]" % options_list, description=desc, version="%%prog %s" % __VERSION__
    )

    for o in options:
        shorter = "-" + o
        longer = "--" + options[o][0]
        if type(options[o][2]) is bool:
            parser.add_option(shorter, longer, dest=o, help=options[o][1], action="store_true", default=options[o][2])
        elif type(options[o][2]) is str:
            parser.add_option(
                shorter, longer, dest=o, help=options[o][1], action="store", type="string", default=options[o][2]
            )

    (opt, args) = parser.parse_args(argv)
    if len(args) < MIN_ARGS + 1:
        # not enough arguments
        print(
            """ERROR: not enough arguments.
Try `%s --help' for more information"""
            % args[0].split(sep)[-1]
        )
        exit(1)

    # ignore the argv[0]
    files = args[1:] if args[1:] else glob("*.[mM][pP]3")
    if not files:
        print("No files found")

    if opt.r:  # get tags from files for renaming them
        regex = None
        rename_format = _RENAME_FILENAME_FORMAT
    elif not opt.n:  # get tags from directories
        regex = re.compile(_REGEX_TEXT_DIRECTORY)
        rename_format = None
    else:  # get tag from filename
        regex = re.compile(_REGEX_TEXT_FILENAME)
        rename_format = None

    for arg in files:
        id3 = autoid3(arg, regex, rename_format)
        artist = opt.a
        genre = opt.g
        prefix_tracknum_in_title = opt.c
        try:
            id3.analyze(artist, genre, prefix_tracknum_in_title)
        except KeyboardInterrupt:  # FIXME
            print("Error: ", sys.exc_info()[1])
            if not opt.q:
                print("    Couldn't analyze the file. Quitting...")
            continue

        if not id3.isUpdatable() and not opt.f:
            if not opt.q:
                print("    No change detected")
            continue

        if not opt.q:
            print("    File can be updated:")
            if opt.r:
                print("     '%s' => '%s'" % (arg, id3._new_filename))
            else:
                for t in DESIRED_TAGS:
                    print("     %s: '%s' => '%s'" % (t, id3.getOldTag(t), id3.getNewTag(t)))

        if opt.w:
            if not opt.r and not opt.k:  # opt.r does not care about tags
                id3.deleteOldTag()

            if not id3.writeChanges():
                print("Writing on the file failed!")
                continue

            if not opt.q:
                print("File has been updated!")
        else:
            print(" (use the --write option to write the changes)")
        print
    exit(0)

# vim: tabstop=4 shiftwidth=4 expandtab autoindent softtabstop=4
