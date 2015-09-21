#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Janet
#
# Created:     25/08/2015
# Copyright:   (c) Janet 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------
from simplekml import Kml, Style
import numpy
from random import randint

def writekml(inarray, kmlfilename):
    kml = Kml()
    sharedstyle = Style()
    sharedstyle.iconstyle.icon.href = 'http://maps.google.com/mapfiles/kml/paddle/wht-blank.png'
    sharedstyle.iconstyle.color = "ffffffff"
    sharedstyle.iconstyle.ColorMode = "random"

    for indiv in numpy.nditer(inarray):
        desc = adddescription(indiv)
        lat =float(indiv[()]['Lat'])
        lon =float(indiv[()]['Long'])
        pnt = kml.newpoint(name=str(indiv[()]['GivenNames']) + " " +str(indiv[()]['FamilyName']), description=desc,
            coords = [(lon,lat)])
        pnt.style = sharedstyle
    kml.save(kmlfilename)

def adddescription(indiv):
    description =  ("<![CDATA[<html><body>"
                    "<body style='margin:0px 0px 0px 0px;overflow:auto;background:#FFFFFF;'>"
                    "<table style = 'font-family:Arial,Verdana,Times;font-size:12px;text-align:"
                    "left;width:100%;border-spacing:0px; padding:3px 3px 3px 3px'>"
                    "<tr><td>Name</td><td>" + str(indiv[()]['GivenNames']) + " "  + str(indiv[()]['FamilyName']) + "</td></tr>"
                    "<tr bgcolor='#D4E4F3'> <td>Event</td> <td>" + str(indiv[()]['Event']) + "</td></tr>"
                    "<tr><td>Date</td> <td>" + str(indiv[()]['Date']) + "</td></tr>"
                    "<tr><td>Place</td> <td>" + str(indiv[()]['Place']) + "</td></tr>"
                    "<tr><td>Source</td> <td>" + str(indiv[()]['Source']) + "</td></tr>"
                    "</table>"
                    "</body>"
                    "</html>]]>")
    return description


def main():
    pass

if __name__ == '__main__':
    main()
