#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
__VERSION__ = 0.2
__default_header = """#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  Copyright (C) 2009 - Tutoo Team

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
# along with this program.  If not, see <http://www.gnu.org/licenses/>."""
__alternate_header = """#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  Copyright (C) 2009 - Tutoo Team

# This file is part of %(name)s.
# 
# %(name)s is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# 
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# %(name)s is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# 
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with %(name)s.  If not, see <http://www.gnu.org/licenses/>."""


MIN_ARGS = 1

def main(f, verbose = False, inline = False, header = False, alternate = False, destiny = False):
	"""
	Puts the gplv3 header (or a different one with the -h param) on the @FILE
	Check if the header already exists and overwrites it.
	"""
	from color import green, yellow

	origin = args[1]
	if header:
		try:
			desired_header = open(header).read()
		except:
			from sys import exit
			from color import red
			print red("Header file was unable to be read! Aborting")
			exit(1)
	elif alternate:
		desired_header = __alternate_header % {'name' : alternate,}
	else:
		desired_header = __default_header

	ori_content = open(origin).read().splitlines()
	found_header_keyword = False
	headers = ('python', 'coding', 'copyright','this program', 'this file is part of')
	for i in ori_content :
		if i.startswith('#'):
			for h in headers:
				if i.lower().find(h) != -1:
					found_header_keyword = True
			if not found_header_keyword:
				break  # ops, it's a unknown comment out of nowhere
			# else:  # ok, it's a header or it's still a header
		elif not i.strip():  # blank line
			found_header_keyword = False
		else:  # ok, we reached something
			break
	first_real_line_index = ori_content.index(i)
	if verbose: print "%s %s" % (green("First non-header line:"), ori_content[first_real_line_index])
	file_without_header = ori_content[first_real_line_index:]
	# put header + '\n' + content
	file_with_header = desired_header.splitlines() + ['',] + file_without_header
	if file_with_header[-1] is not '':
		# it's good to have a blank line at the end
		file_with_header.append('')
	if verbose:
		print "%s\n%s\n%s" % (
				green("Beggining of the new file:"),
				'\n'.join(file_with_header[:len(desired_header.splitlines())+10]),
				green('End of the beggining of the new file'),
			)

	if not destiny and inline:
		destiny = origin
	if destiny:
		destiny_file = open(destiny, 'w')
		destiny_file.write('\n'.join(file_with_header))
		destiny_file.close()
		if destiny == origin:
			print 'Successfully updated %s with the new header' % yellow(destiny)
		else:
			print 'Successfully put header from "%s" into the new file "%s"' % (yellow(origin), yellow(destiny))

if __name__ == "__main__":
	from sys import argv, exit
	from os import sep
	from optparse import OptionParser

	options = {
		# 'one_letter_option' : ['full_option_name',
			# "Help",
			# default_value],
		'v' : ['verbose',
			"Shows more info about the process",
			False],
		'i' : ['inline',
			"Changes the content of the file with this new header",
			False],
		'f' : ['header-file',
			"Change the default header to the content of this file",
			""],
		'a' : ['alternate-header',
			"Use an alternate header that includes this string as being 'part of' other product",
			""],
	}

	options_list = ' '.join(["[-%s --%s]" % (o, options[o][0]) for o in options])
	desc = main.__doc__.replace('\t','')
	parser = OptionParser("%%prog %s FILE" % options_list,
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

	main(args[1], opt.v, opt.i, opt.f, opt.a)

