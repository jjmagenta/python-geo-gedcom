"""
-------------------------------------------------------------------------------
 Name:      geogedcom.py
 Purpose:   Module to control reading and parsing of gedcom file, georeferencing
            and writing to an ESRI shapefile.

 Author:    Janet Rogers

 Created:   18/07/2015
 Copyright: (c) Janet Rogers 2015
 Licence:   This work is licensed under the Creative Commons Attribution-NonCommercial 4.0
            International License. To view a copy of this license,
            visit http://creativecommons.org/licenses/by-nc/4.0/ or send a letter to
            Creative Commons, PO Box 1866, Mountain View, CA 94042, USA.
 The GEDCOM Standard Release 5.5: http://homepages.rootsweb.ancestry.com/~pmcbride/gedcom/55gcch2.htm#S1
------------------------------------------------------------------------------
"""
#Standard Modules
import argparse
import arcpy
import os
import numpy
import re
#Project Modules
import codesdict
import geocodeplace
import gedcomparser

class MyFamily:
    """Reader and formatter for the Gedcom parser."""

    def __init__(self):
        """ Initialize test class."""
        self.parse_options()
        self.g = gedcomparser.Gedcom(self.filename)
        self.info = 'names'
        self.indiplacelist = []

    def parse_options(self):
        """ Parse command-line options."""
        #http://prschmid.blogspot.com.au/2013/07/parsing-arguments-in-python-with.html
        parser = argparse.ArgumentParser(description="Input for python-geogedcom.")
##        'C:\Python27\ArcGIS10.3\GEDCOMS\The Rogers Family Tree Short.ged'
##        'C:\Python27\ArcGIS10.3\GEDCOMS\BROSKEEP.ged'
##        'C:\Python27\ArcGIS10.3\GEDCOMS\paf.ged'
##        'C:\Python27\ArcGIS10.3\GEDCOMS\FamilyTreeBuilder.ged'
##        'C:\Python27\ArcGIS10.3\GEDCOMS\rootsmagic2.ged'
##        'C:\Python27\ArcGIS10.3\GEDCOMS\rootsmagic.ged'
##        'C:\Python27\ArcGIS10.3\GEDCOMS\ftm.GED'
##        'C:\Python27\ArcGIS10.3\GEDCOMS\genopro.ged'
##        'C:\Python27\ArcGIS10.3\GEDCOMS\ancquest.ged'
##        parser.add_argument(
##                            '-g','--filename', required=False, help="Name of Gedcom file",
##                            default='C:\\Python27\\ArcGIS10.3\\GEDCOMS\\ancquest.ged', dest='filename')
        parser.add_argument(
                            '-g','--filename', required=False, help="Name of Gedcom file",
                            default="C:\Python27\ArcGIS10.3\GEDCOMS\The Rogers Family Tree.ged", dest='filename')
        parser.add_argument(
                            '-s', '--seedfilename', required=False, help="Pattern name of output Feature Class. Numerical suffixes will be added.",
                            default='C:\\Python27\\ArcGIS10.3\\Lib\\Genealogy.gdb\\TestFeatureClass', dest = 'seedfilename')
        parser.add_argument(
                            '-p', '--projectionfile', required=False, help="PRJ file to be used for Feature Class projection",
                            default='C:\\Python27\\ArcGIS10.3\\Lib\pyGeoGEDCOM\\wgs84.prj', dest='spatialref')
        parser.add_argument(
                            '-l', '--locatorname', required=False, help="Geocoding Locator",
                            default = 'Google', dest='locator')
        parser.add_argument(
                            '-f', '--geocodeflag', required=False, help="If flag is false, actual geocoding is skipped.",
                            default = 'True', dest='geocodeflag')
        parser.parse_args(namespace=self)


    def print_record(self, elem):
        """Print an element."""
        if self.info == 'names':
            (first, last) = elem.name()
            print first, last
        elif self.info == 'gedcom':
            print elem.get_individual()

    def readindividuals(self, locatorname, geocodeflag, info='names'):
        """Read and format the data for a Place for one Individual."""
        self.info = info
        indilist = []
        family = ''
        #Get the standard gedcom codes
        codedict = codesdict.KeyCodes()
        codedict.readcodes()
        #Initialise the selected geocoding locator
        locator = initlocator(locatorname)
        for elem in self.g.element_list():
            if elem.individual():
                #Get read all the families into a string
                family = ''
                for fam in elem.families():
                    family = family + str(fam)
                #Regular Expression for Family tag
                srchobj = re.search(r'F(\d{1,5})', family, flags=0)
                if srchobj:
                    family = (srchobj.group())
                else:
                    family = ''

                #Get the events and dates associate with the family section of the gedcom file
                for elem2 in elem.children():
                    indidate = ''
                    indievent = ''
                    indiyear = 0
                    for elem3 in elem2.children():
                        if elem3.date():
                            indidate = elem3.value()
                            #Get the year
                            srchobj = re.search(r'\d{4}', indidate, flags=0)
                            if srchobj:
                                indiyear = int(srchobj.group())
                            else:
                                indiyear = 0
                            #Get the place and geocode it
                        if elem3.place():
                            #Get the longitude and Latitude
                            position = locator.geocode(elem3.value(), geocodeflag)
                            latitude = position[0]
                            longitude = position[1]
                            #Get the event code
                            event = str(elem3.parent()).split(' ')[1]
                            indievent = codedict.lookupcode(event)
                            indilist.append(tuple([longitude, latitude, elem.name()[0], elem.name()[1], family, indidate, indiyear, elem3.value(), indievent,longitude, latitude]))
        self.indiplacelist = indilist


def createfilename(seedname):
    """Module that creates a unique sequential file name for the GIS Geodatabase data."""
    foldername = os.path.dirname(seedname)
    basefile = os.path.basename(seedname)
    filename = os.path.splitext(basefile)[0]
    inc = 0
    resultname = os.path.join(foldername, filename + "_" + str(inc))
    while arcpy.Exists(resultname):
        inc = inc+1
        resultname = os.path.join(foldername, filename + "_" + str(inc))
    return resultname

def initlocator(locatorname):
    """Initialise the locator."""
    locator = geocodeplace.GEOCODEPLAC(locatorname)
    return locator

def writetofc(fcname, outputlist, headingslist, spatialref):
    """Writes data stored as tuples to an ArcGIS Table."""
    cols = len(outputlist[0])
    dts = list()
    dtt = tuple()
    cols = len(outputlist[0])
    maxlen = maxitemlength(outputlist)

    #Format the constructed array
    for col in range(cols):
        desclist = headingslist[col]
        typlist = "|S"+str(maxlen[col])
        if desclist == 'Latitude' or desclist == 'Longitude':
            typlist = "<f8"
        elif desclist == "Year":
            typlist = numpy.int32
        dtt = desclist, typlist
        dts.append(dtt)
    inarray = numpy.array(outputlist, numpy.dtype(dts))
    #arcpy.da.NumPyArrayToTable(inarray, fcname)
    arcpy.da.NumPyArrayToFeatureClass(inarray, fcname, ("Longitude", "Latitude"), spatialref)
    return

def headings():
    """Formats headings for Feature Class."""
    myheadings = []
    myheadings.append("Longitude")
    myheadings.append("Latitude")
    myheadings.append("GivenNames")
    myheadings.append("FamilyName")
    myheadings.append("Family")
    myheadings.append("Date")
    myheadings.append("Year")
    myheadings.append("Place")
    myheadings.append("Event")
    myheadings.append("Long")
    myheadings.append("Lat")
    return myheadings

def maxitemlength(arr):
    """Determines the maximum length of columnar data for creating the attribute fields."""
    maxlenlist = []
    maxlen = 0
    rows = len(arr)
    cols = len(arr[0])
    for col in xrange(cols):
        for row in xrange(rows):
            maxlen = max(maxlen, len(str(arr[row][col])))
        maxlenlist.append(roundup(maxlen))
        maxlen = 0
    return maxlenlist

def roundup(num):
    """Returns an integer rounded up."""
    return int(math.ceil(num / 5.0)) * 5

def main():
    #parse_options()
    """Handles the reading, writing and geocoding of the GEDCOM file data."""
    individuals = MyFamily()
    individuals.readindividuals(individuals.locator, individuals.geocodeflag)

    #Get a unique filename for the Feature Class
    addressfc = createfilename(individuals.seedfilename)

    #Write the ArcGIS Feature Class
    writetofc(addressfc, individuals.indiplacelist, headings(), individuals.spatialref)

if __name__ == '__main__':
    main()
