"""
-------------------------------------------------------------------------------
 Name:      geocodeplacepy
 Purpose:   A module to handle the geocoding of place names

 Author:    Janet Rogers

 Created:   18/07/2015
 Copyright: (c) Janet Rogers 2015
 Licence:   This work is licensed under the Creative Commons Attribution-NonCommercial 4.0
            International License. To view a copy of this license,
            visit http://creativecommons.org/licenses/by-nc/4.0/ or send a letter to
            Creative Commons, PO Box 1866, Mountain View, CA 94042, USA.
------------------------------------------------------------------------------
"""
class GEOCODEPLAC(object):
    """A class to open the requested geolocator and handle the geocoding
    of place names."""

    qgeolocator = None

    def __init__(self, locator):
        """Initialises the Locator"""
        if locator == "ArcGIS":
            from geopy.geocoders import ArcGIS
            print "ArcGIS"
            self.qgeolocator = ArcGIS(username='*****', password='*****', referer=None)
        if locator == "Google":
            from geopy.geocoders import GoogleV3
            print "Google V3"
            self.qgeolocator = GoogleV3()
        if locator == "Bing":
            from geopy.geocoders import Bing
            print "Bing"
            self.qgeolocator = Bing
            ('*****')
        if locator == "GeoNames":
            from geopy.geocoders import GeoNames
            print "GeoNames"
            self.qgeolocator = GeoNames(username='*****')
        if locator == "OSM":
            from geopy.geocoders import Nominatim
            print "Nominatim"
        if locator == "OpenCage":
            from geopy.geocoders import OpenCage
            print "OpenCage"
            self.qgeolocator = OpenCage('*****')
        if locator == "OpenMapQuest":
            from geopy.geocoders import OpenMapQuest
            print "OpenMapQuest"
            self.qgeolocator = OpenMapQuest()

    def geocode(self, place, flag):
        """Call the Locator for geocoding."""
        if flag == 'False':
            return(0,0)
        else:
            location = self.qgeolocator.geocode(place, timeout=10)
            if location is None:
                return(0, 0)
            else:
                return(location.latitude, location.longitude)

def main():
    """Main function."""
    pass

if __name__ == '__main__':
    main()
