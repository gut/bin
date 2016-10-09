#!/usr/bin/env python2
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
__VERSION__ = 0.1

__colorDict = {
	'grey' : 30,
	'red' : 31,
	'green' : 32,
	'yellow' : 33,
	'blue' : 34,
	'rose' : 35,
	'cyan' : 36,
	'white' : 37,
	'crimson' : 38,
	'bgRed' : 41,
	'bgGreen' : 42,
	'bgBrown' : 43,
	'bgBlue' : 44,
	'bgRose' : 45,
	'bgCyan' : 46,
	'bgGrey' : 47,
	'bgCrimson' : 48,
}

for __color in __colorDict:
	exec("%s = lambda txt: '\033[1;%dm%%s\033[1;m' %% txt" % (__color, __colorDict[__color]))

if __name__ == "__main__":
	for color in sorted(__colorDict.keys()):
		print eval("%(c)s('Hello from function %%s!' %% '%(c)s')" % {'c' : color})
