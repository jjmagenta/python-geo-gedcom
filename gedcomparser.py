"""
-------------------------------------------------------------------------------
 Name:      gedcomparser.py
 Purpose:   Python GEDCOM Parser
            This module is based on a GEDCOM parser written by
            Daniel Zappala at Brigham Young University (copyright (C) 2005) and
            was licensed under GPL v2.
            (daniel.zappala [at] gmail.com)

            Added retrieval of residence, fix for error when there is an unentered surname,
            adjusted naming conventions and syntax for pylint analysis.

            Criteria matching is not used in this instance of the parser however has been left
            in the code for the sake of completeness with the original.

 Author:    Janet Rogers
 Created:   18/07/2015
 Copyright: (c) Janet Rogers 2015
 Licence:   This work is licensed under the Creative Commons Attribution-NonCommercial 4.0
            International License. To view a copy of this license,
            visit http://creativecommons.org/licenses/by-nc/4.0/ or send a letter to
            Creative Commons, PO Box 1866, Mountain View, CA 94042, USA.
 The GEDCOM Standard Release 5.5: http://homepages.rootsweb.ancestry.com/~pmcbride/gedcom/55gcch2.htm#S1
-----------------------------------------------------------------------------

"""

# Copyright (C) 2012 Daniel Zappala (daniel.zappala [at] gmail.com)

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

__all__ = ["Gedcom", "Element", "GedcomParseError"]

# Global imports
import string

class Gedcom:
    """Gedcom parser

    This parser reads a GEDCOM file and parses it into a set of
    elements.  These elements can be accessed via a list (the order of
    the list is the same as the order of the elements in the GEDCOM
    file), or a dictionary (the key to the dictionary is a unique
    identifier that one element can use to point to another element).

    """

    def __init__(self,file):
        """Initialize a Gedcom parser. You must supply a Gedcom file."""
        self.__element_list = []
        self.__element_dict = {}
        self.__element_top = Element(-1, "", "TOP", "", self.__element_dict)
        self.__current_level = -1
        self.__current_element = self.__element_top
        self.__individuals = 0
        self.__parse(file)

    def element_list(self):
        """Return a list of all the elements in the Gedcom file.  The
        elements are in the same order as they appeared in the file.

        """
        return self.__element_list

    def element_dict(self):
        """Return a dictionary of elements from the Gedcom file.  Only
        elements identified by a pointer are listed in the dictionary.
        The key for the dictionary is the pointer.

        """
        return self.__element_dict

    # Private methods

    def __parse(self,file):
        # open file
        # go through the lines
        #f = open(file, 'r')
        #print file
        with open(file, 'r') as f:
            number = 1
            for line in f:
                # Skip over some junk that Rootsmagic puts in gedcom files.
                if number == 1 and ord(line[0]) == 239:
                    line = line[3:]
                self.__parse_line(number, line)
                number += 1
            self.__count()

    def __parse_line(self, number, line):
        """Parses line by splitting into Level, Pointer, Tage and Value"""
        parts = string.split(line)
        place = 0
        l = self.__level(number,parts,place)
        place += 1
        p = self.__pointer(number,parts,place)
        if p != '':
            place += 1
        t = self.__tag(number,parts,place)
        place += 1
        v = self.__value(number,parts,place)

        # create the element
        if l > self.__current_level + 1:
            self.__error(number, "Structure of GEDCOM file is corrupted")

        e = Element(l,p,t,v,self.element_dict())
        self.__element_list.append(e)
        if p != '':
            self.__element_dict[p] = e

        if l > self.__current_level:
            self.__current_element.add_child(e)
            e.add_parent(self.__current_element)
        else:
            # l.value <= self.__current_level:
            while (self.__current_element.level() != l - 1):
                self.__current_element = self.__current_element.parent()
            self.__current_element.add_child(e)
            e.add_parent(self.__current_element)

        # finish up
        self.__current_level = l
        self.__current_element = e

    def __level(self, number, parts, place):
        """Returns the level part of the file line if it exists"""
        if len(parts) <= place:
            self.__error(number, "Empty line")
        try:
            l = int(parts[place])
        except ValueError:
            self.__error(number, "Line must start with an integer level")

        if (l < 0):
            self.__error(number, "Line must start with a positive integer")

        return l

    def __pointer(self, number, parts, place):
        """Returns the pointer part of the file line if it exists"""
        if len(parts) <= place:
            self.__error(number, "Incomplete Line")
        p = ''
        part = parts[1]
        if part[0] == '@':
            if part[len(part)-1] == '@':
                p = part
                # could strip the pointer to remove the @ with
                # string.strip(part,'@')
                # but it may be useful to identify pointers outside this class
            else:
                self.__error(number, "Pointer element must start and end with @")
        return p

    def __tag(self, number, parts, place):
        """Returns the tag part of the file line if it exists"""

        if len(parts) <= place:
            self.__error(number, "Incomplete line")
        return parts[place]

    def __value(self, number, parts, place):
        """Returns the value part of the file line if it exists"""
        if len(parts) <= place:
            return ''
        p = self.__pointer(number,parts,place)
        if p != '':
            # rest of the line should be empty
            if len(parts) > place + 1:
                self.__error(number, "Too many elements")
            return p
        else:
            # rest of the line should be ours
            vlist = []
            while place < len(parts):
                vlist.append(parts[place])
                place += 1
            v = string.join(vlist)
            return v

    def __error(self, number, text):
        """Raises gedcom file format error"""

        error = "Gedcom format error on line " + str(number) + ': ' + text
        raise GedcomParseError, error

    def __count(self):
        """Count number of individuals"""
        self.__individuals = 0
        for e in self.__element_list:
            if e.individual():
                self.__individuals += 1

    def __print(self):
        for e in self.element_list:
            print string.join([str(e.level()),e.pointer(),e.tag(),e.value()])


class GedcomParseError(Exception):
    """Exception raised when a Gedcom parsing error occurs."""

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return `self.value`

class Element:
    """Gedcom element

    Each line in a Gedcom file is an element with the format

    level [pointer] tag [value]

    where level and tag are required, and pointer and value are
    optional.  Elements are arranged hierarchically according to their
    level, and elements with a level of zero are at the top level.
    Elements with a level greater than zero are children of their
    parent.

    A pointer has the format @pname@, where pname is any sequence of
    characters and numbers.  The pointer identifies the object being
    pointed to, so that any pointer included as the value of any
    element points back to the original object.  For example, an
    element may have a FAMS tag whose value is @F1@, meaning that this
    element points to the family record in which the associated person
    is a spouse.  Likewise, an element with a tag of FAMC has a value
    that points to a family record in which the associated person is a
    child.

    See a Gedcom file for examples of tags and their values.

    """

    def __init__(self,level,pointer,tag,value,dict):
        """Initialize an element.  You must include a level, pointer,
        tag, value, and global element dictionary.  Normally
        initialized by the Gedcom parser, not by a user.

        """
        # basic element info
        self.__level = level
        self.__pointer = pointer
        self.__tag = tag
        self.__value = value
        self.__dict = dict
        # structuring
        self.__children = []
        self.__parent = None

    def level(self):
        """Return the level of this element."""
        return self.__level

    def pointer(self):
        """Return the pointer of this element."""
        return self.__pointer

    def tag(self):
        """Return the tag of this element."""
        return self.__tag

    def value(self):
        """Return the value of this element."""
        return self.__value

    def children(self):
        """Return the child elements of this element."""
        return self.__children

    def parent(self):
        """Return the parent element of this element."""
        return self.__parent

    def add_child(self, element):
        """Add a child element to this element."""
        self.children().append(element)

    def add_parent(self, element):
        """Add a parent element to this element."""
        self.__parent = element

    def individual(self):
        """Check if this element is an individual."""
        return self.tag() == "INDI"

    def date(self):
        """Check if this element is a place."""
        return self.tag() == "DATE"

    def place(self):
        """Check if this element is a place."""
        return self.tag() == "PLAC"

    # criteria matching

    def criteria_match(self, criteria):
        """Check in this element matches all of the given criteria.
        The criteria is a colon-separated list, where each item in the

        list has the form [name]=[value]. The following criteria are supported:

        surname=[name]
             Match a person with [name] in any part of the surname.
        name=[name]
             Match a person with [name] in any part of the given name.
        birth=[year]
             Match a person whose birth year is a four-digit [year].
        birthrange=[year1-year2]
             Match a person whose birth year is in the range of years from
             [year1] to [year2], including both [year1] and [year2].
        death=[year]
        deathrange=[year1-year2]
        marriage=[year]
        marriagerange=[year1-year2]

        """
        # error checking on the criteria
        try:
            for crit in criteria.split(':'):
                key, value = crit.split('=')
        except ValueError:
            return False
        match = True
        for crit in criteria.split(':'):
            key, value = crit.split('=')
            if key == "surname" and not self.surname_match(value):
                match = False
            elif key == "name" and not self.given_match(value):
                match = False
            elif key == "birth":
                try:
                    year = int(value)
                    if not self.birth_year_match(year):
                        match = False
                except ValueError:
                    match = False
            elif key == "birthrange":
                try:
                    year1, year2 = value.split('-')
                    year1 = int(year1)
                    year2 = int(year2)
                    if not self.birth_range_match(year1, year2):
                        match = False
                except ValueError:
                    match = False
            elif key == "death":
                try:
                    year = int(value)
                    if not self.death_year_match(year):
                        match = False
                except ValueError:
                    match = False
            elif key == "deathrange":
                try:
                    year1, year2 = value.split('-')
                    year1 = int(year1)
                    year2 = int(year2)
                    if not self.death_range_match(year1, year2):
                        match = False
                except ValueError:
                    match = False
            elif key == "marriage":
                try:
                    year = int(value)
                    if not self.marriage_year_match(year):
                        match = False
                except ValueError:
                    match = False
            elif key == "marriagerange":
                try:
                    year1, year2 = value.split('-')
                    year1 = int(year1)
                    year2 = int(year2)
                    if not self.marriage_range_match(year1, year2):
                        match = False
                except ValueError:
                    match = False

        return match

    def surname_match(self, name):
        """Match a string with the surname of an individual."""
        (first, last) = self.name()
        return last.find(name) >= 0

    def given_match(self, name):
        """Match a string with the given names of an individual."""
        (first, last) = self.name()
        return first.find(name) >= 0

    def birth_year_match(self, year):
        """Match the birth year of an individual.  Year is an integer."""
        return self.birth_year() == year

    def birth_range_match(self, year1, year2):
        """Check if the birth year of an individual is in a given
        range.  Years are integers.

        """
        year = self.birth_year()
        if year >= year1 and year <= year2:
            return True
        return False

    def death_year_match(self, year):
        """Match the death year of an individual.  Year is an integer."""
        return self.death_year() == year

    def death_range_match(self, year1, year2):
        """Check if the death year of an individual is in a given range.
        Years are integers.

        """
        year = self.death_year()
        if year >= year1 and year <= year2:
            return True
        return False

    def marriage_year_match(self, year):
        """Check if one of the marriage years of an individual matches
        the supplied year.  Year is an integer.

        """
        years = self.marriage_years()
        return year in years

    def marriage_range_match(self, year1, year2):
        """Check if one of the marriage year of an individual is in a
        given range.  Years are integers.

        """
        years = self.marriage_years()
        for year in years:
            if year >= year1 and year <= year2:
                return True
        return False

    def families(self):
        """Return a list of all of the family elements of a person."""
        results = []
        for e in self.children():
            if e.tag() == "FAMS":
                f = self.__dict.get(e.value(),None)
                if f != None:
                    results.append(f)
        return results

    def name(self):
        """Return a person's names as a tuple: (first,last)."""
        first = ""
        last = ""
        if not self.individual():
            return (first, last)
        for e in self.children():
            if e.tag() == "NAME":
                # some older Gedcom files don't use child tags but instead
                # place the name in the value of the NAME tag
                if e.value() != "":
                    name = string.split(e.value(),'/')
                    first = string.strip(name[0])
                    if e.value().find('/') <> -1:
                        last = string.strip(name[1])
                    else:
                        last = 'Unknown'
                else:
                    for c in e.children():
                        if c.tag() == "GIVN":
                            first = c.value()
                        if c.tag() == "SURN":
                            last = c.value()
        return (first, last)

    def birth(self):
        """Return the birth tuple of a person as (date, place)."""
        date = ""
        place = ""
        if not self.individual():
            return (date, place)
        for e in self.children():
            if e.tag() == "BIRT":
                for c in e.children():
                    if c.tag() == "DATE":
                        date = c.value()
                    if c.tag() == "PLAC":
                        place = c.value()
        return (date, place)

    def birth_year(self):
        """Return the birth year of a person in integer format."""
        date = ""
        if not self.individual():
            return date
        for e in self.children():
            if e.tag() == "BIRT":
                for c in e.children():
                    if c.tag() == "DATE":
                        datel = string.split(c.value())
                        date = datel[len(datel)-1]
        if date == "":
            return -1
        try:
            return int(date)
        except ValueError:
            return -1

    def residence(self):
        """Return the residence tuple of a person as (date, place)."""
        date = ""
        place = ""
        if not self.individual():
            return (date, place)
        for elem in self.children():
            if elem.tag() == "RESI":
                for child in elem.children():
                    if child.tag() == "DATE":
                        date = child.value()
                    if child.tag() == "PLAC":
                        place = child.value()
        return (date, place)

    def residence_year(self):
        """Return the birth year of a person in integer format."""
        date = ""
        if not self.individual():
            return date
        for elem in self.children():
            if elem.tag() == "RESI":
                for child in elem.children():
                    if child.tag() == "DATE":
                        datel = string.split(child.value())
                        date = datel[len(datel)-1]
        if date == "":
            return -1
        try:
            return int(date)
        except ValueError:
            return -1

    def death(self):
        """Return the death tuple of a person as (date, place)."""
        date = ""
        place = ""
        if not self.individual():
            return (date, place)
        for e in self.children():
            if e.tag() == "DEAT":
                for c in e.children():
                    if c.tag() == "DATE":
                        date = c.value()
                    if c.tag() == "PLAC":
                        place = c.value()
        return (date, place)

    def death_year(self):
        """Return the death year of a person in integer format."""
        date = ""
        if not self.individual():
            return date
        for e in self.children():
            if e.tag() == "DEAT":
                for c in e.children():
                    if c.tag() == "DATE":
                        datel = string.split(c.value())
                        date = datel[len(datel)-1]
        if date == "":
            return -1
        try:
            return int(date)
        except ValueError:
            return -1

    def deceased(self):
        """Check if a person is deceased."""
        if not self.individual():
            return False
        for e in self.children():
            if e.tag() == "DEAT":
                return True
        return False

    def marriage(self):
        """Return a list of marriage tuples for a person, each listing
        (date, place).

        """
        date = ""
        place = ""
        if not self.individual():
            return (date, place)
        for e in self.children():
            if e.tag() == "FAMS":
                f = self._Element__dict.get(e.value(), None)
                if f == None:
                    return (date, place)
                for g in f.children():
                    if g.tag() == "MARR":
                        for h in g.children():
                            if h.tag() == "DATE":
                                date = h.value()
                            if h.tag() == "PLAC":
                                place = h.value()
        return (date, place)

    def marriage_years(self):
        """Return a list of marriage years for a person, each in integer
        format.

        """
        dates = []
        if not self.individual():
            return dates
        for e in self.children():
            if e.tag() == "FAMS":
                f = self.__dict.get(e.value(),None)
                if f == None:
                    return dates
                for g in f.children():
                    if g.tag() == "MARR":
                        for h in g.children():
                            if h.tag() == "DATE":
                                datel = string.split(h.value())
                                date = datel[len(datel)-1]
                                try:
                                    dates.append(int(date))
                                except ValueError:
                                    pass
        return dates

    def get_individual(self):
        """Return this element and all of its sub-elements."""
        result = [self]
        for e in self.children():
            result.append(e)
        return result

    def get_family(self):
        """Return this element any all elements in its families."""
        result = [self]
        for e in self.children():
            if e.tag() == "HUSB" or e.tag() == "WIFE" or e.tag() == "CHIL":
                f = self.__dict.get(e.value())
                if f != None:
                    result.append(f)
        return result

    def __str__(self):
        """Format this element as its original string."""
        result = str(self.level())
        if self.pointer() != "":
            result += ' ' + self.pointer()
        result += ' ' + self.tag()
        if self.value() != "":
            result += ' ' + self.value()
        return result
