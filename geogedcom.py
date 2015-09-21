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
import kmlgedcom

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
                            '-c','--filename', required=False, help="Name of Gedcom file",
                            default="C:\Python27\ArcGIS10.3\GEDCOMS\The Rogers Family Tree.ged", dest='filename')
        parser.add_argument(
                            '-a', '--appflag', required=False, choices=['KML','Feature Class'], help="Flags whether Feature Class or KML is to be produced.",
                            default = 'KML', dest='appflag')
        group = parser.add_mutually_exclusive_group()

        group.add_argument(
                                '-f', '--FCseedfilename', required=False,choices=['C:\\Python27\\ArcGIS10.3\\Lib\\Genealogy.gdb\\TestFeatureClass',
                                'D:\\KMLFile'], help="Pattern name of output data. Numerical suffixes will be added.",
                                default='C:\\Python27\\ArcGIS10.3\\Lib\\Genealogy.gdb\\TestFeatureClass', dest = 'FCseedfilename')
        group.add_argument(
                                '-k', '--KMLseedfilename', required=False, help="Pattern name of output KML. Numerical suffixes will be added.",
                                default='D:\\KMLFile.kml', dest = 'KMLseedfilename')

        parser.add_argument(
                            '-p', '--projectionfile', required=False, help="PRJ file to be used for Feature Class projection",
                            default='C:\\Python27\\ArcGIS10.3\\Lib\pyGeoGEDCOM\\wgs84.prj', dest='spatialref')
        parser.add_argument(
                            '-l', '--locatorname', required=False, help="Geocoding Locator",
                            default = 'Google', dest='locator')
        parser.add_argument(
                            '-g', '--geocodeflag', required=False, help="If flag is false, actual geocoding is skipped.",
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
        count1 = 0
        count2 = 0
        self.info = info
        indilist = []
        family = ''
        #Get the standard gedcom codes
        codedict = codesdict.KeyCodes()
        codedict.readcodes()

        #Get the source codes and titles
        sourcedict = self.createsoucedictionary()

        #Set up a dictionary for places and coordinates to reduce the amount of geocoding required
        placedict = codesdict.PlaceCodes()

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

                #Get the events and dates associated with the gedcom file line
                for elem2 in elem.children():
                    indidate = ''
                    indievent = ''
                    indiyear = 0
                    inditag = ""
                    indiplace = ""
                    indisource = ""
                    ll = ()
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
                            #Check the Places Dictionary to see if it has already been looked-up
                            indiplace = elem3.value()
                            coords = placedict.lookupplace(indiplace)
                            if cmp(coords, [0,0]):
                                count1 += 1
                                #Place not found,  Coords 0,0 returned. Geocode for the longitude and Latitude
                                position = locator.geocode(indiplace, geocodeflag)
                                latitude = position[0]
                                longitude = position[1]
                                #Store in the dictionary
                                placedict.addcode(indiplace, [latitude,longitude])

                            else:
                                #Place already in dictionary
                                count2 += 1
                                latitude,longitude = coords

                            #Get the event code
                            event = str(elem3.parent()).split(' ')[1]
                            indievent = codedict.lookupcode(event).split(" ",1)[1]

                        if elem3.source():
                            indisource = sourcedict.get(elem3.value(), "Unknown")

                            ##famsortorder = elem.family().replace('F','').zfill(5)
                            indisortorder = elem.indi().replace('P','').zfill(5)
                            sortorder = int(codedict.lookupcode(event).split(" ")[0])
                            if indiplace <> "":
                                indilist.append(tuple([longitude, latitude, elem.indi(), elem.name()[0], elem.name()[1], family, indidate, indiyear, indiplace, indievent, indisource, longitude, latitude, indisortorder, sortorder]))

        pass
        print count1
        print count2
        self.indiplacelist = indilist

    def createsoucedictionary(self):
                #Read souce codes and titles into dictionary
        sourcedict ={}
        for elem in self.g.element_list():
            if elem.source() and elem.level() == 0:
                x = elem.source()
                if not sourcedict.has_key(elem.value):
                    for elem2 in elem.children():
                        if elem2.title():
                            sourcedict[elem.pointer()] = elem2.value().decode('ascii', 'ignore')
        return sourcedict

def createfilename(seedname, appflag):
    """Module that creates a unique sequential file name for the Output file/KML."""
    foldername = os.path.dirname(seedname)  #d:\\  ...gdb
    basefile = os.path.basename(seedname)  # KMLFile.kml  -TestFeatureClass
    extension = seedname.split(os.extsep, 1)[1]  #kml   breaks at the 10.3 dot
    filename = os.path.splitext(basefile)[0]  #KMLFile  same as basefile

    inc = 0
    if appflag == "Feature Class":
        resultname = os.path.join(foldername, filename + "_" + str(inc))
        while arcpy.Exists(resultname):
            inc = inc+1
            resultname = os.path.join(foldername, filename + "_" + str(inc))
        return resultname
    else:  #KML
        resultname = os.path.join(foldername, filename + "_" + str(inc) + os.extsep + extension)
        while os.path.exists(resultname):
            inc = inc + 1
            resultname = os.path.join(foldername, filename + "_" + str(inc) + os.extsep +extension)
        return resultname

def initlocator(locatorname):
    """Initialise the locator."""
    locator = geocodeplace.GEOCODEPLAC(locatorname)
    return locator

def writetofc(fcname, outputlist, headingslist, spatialref, appflag):
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
    inarray.sort(order=['IndiSortOrder', 'Year', 'YearSortOrder'])
    if appflag == 'Feature Class':
    #arcpy.da.NumPyArrayToTable(inarray, fcname)
        arcpy.da.NumPyArrayToFeatureClass(inarray, fcname, ("Long", "Lat"), spatialref)
    else:
        kmlgedcom.writekml(inarray, fcname)
    return

def headings():
    """Formats headings for Feature Class."""
    myheadings = []
    myheadings.append("Long")
    myheadings.append("Lat")
    myheadings.append("Individual")
    myheadings.append("GivenNames")
    myheadings.append("FamilyName")
    myheadings.append("Family")
    myheadings.append("Date")
    myheadings.append("Year")
    myheadings.append("Place")
    myheadings.append("Event")
    myheadings.append("Source")
    myheadings.append("Longitude")
    myheadings.append("Latitude")
    myheadings.append("IndiSortOrder")
    myheadings.append("YearSortOrder")
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

    #Get a unique filename for the output.
    if individuals.appflag == "Feature Class":
        seedfilename = individuals.FCseedfilename
    else:
        seedfilename = individuals.KMLseedfilename
    address = createfilename(seedfilename, individuals.appflag)

    #Write the ArcGIS Feature Class
    writetofc(address, individuals.indiplacelist, headings(), individuals.spatialref, individuals.appflag)


if __name__ == '__main__':
    main()
