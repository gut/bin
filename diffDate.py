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
__VERSION__ = "0.1"


import re
from datetime import date

_RE_THIS_YEAR = re.compile(r"^(?P<Day>\d{1,2})/(?P<Month>\d{1,2})$")
_RE_SPECIFIC_YEAR = re.compile(r"^(?P<Day>\d{1,2})/(?P<Month>\d{1,2})/(?P<Year>(\d{2}|\d{4}))$")
_RE_ELEMENTS = ('Day', 'Month', 'Year',)

def diffDays(target_date):
    """Calculates days that differs from today to
    the asked @target_date"""
    found_another_year = _RE_SPECIFIC_YEAR.match(target_date)
    found_current_year = _RE_THIS_YEAR.match(target_date)

    matched = found_another_year if found_another_year else found_current_year
    if not matched:
        # found_current_year also didn't work
        raise ValueError, "> Parsing error"

    matched_dict = matched.groupdict()
    target_dict = dict.fromkeys(_RE_ELEMENTS)

    # in case it's this year, don't leave this key without value
    target_dict['Year'] = date.today().year
    for param in matched_dict:
        target_dict[param] = int(matched_dict[param])

    target_date = date(target_dict['Year'], target_dict['Month'], target_dict['Day'])

    diff = target_date - date.today()
    return diff.days


if __name__ == "__main__":
    this_year = date.today().year
    print "Which calendar day you want? (dd/mm/yyyy or dd/mm for year %s)" % this_year
    str_date = raw_input()
    try:
        days = diffDays(str_date.strip())
        print "\nFrom today until %s it'll take %d days" % (str_date, days)
        DAYS_IN_THE_YEAR = 365 if days > 0 else -365
        if abs(days) > abs(DAYS_IN_THE_YEAR):
            years = days / abs(DAYS_IN_THE_YEAR)  # abs so it stays negative
            rest_days = days % DAYS_IN_THE_YEAR
            print "or %s years and %d days" % (years, rest_days)
    except ValueError as exp:
        print exp
    print "\nPress enter to close"
    raw_input()

