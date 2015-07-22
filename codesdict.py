"""
-------------------------------------------------------------------------------
 Name:      codesdict.py
 Purpose:   Module to create dictionaries for GEDCOM Codes, Individual Codes and Family Codes.

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


import pprint

class KeyCodes(object):
    """Class to read standard codes from the GEDCOM Definition and
       associate them with explanatory text."""

    def __init__(self):
        """Create dictionary"""
        self.dictcodes = {}

    def readcodes(self):
        """Read GEDCOM codes."""
        self.dictcodes['ADDR'] = 'Address, usually mailing address'
        self.dictcodes['ADR1'] = 'First line of an address'
        self.dictcodes['ADR2'] = 'Second line of an address'
        self.dictcodes['ADOP'] = 'Adoption'
        self.dictcodes['AFN'] = 'Ancestral File number (LDS)'
        self.dictcodes['AGE'] = 'Age at time of event'
        self.dictcodes['ALIA'] = 'Alias'
        self.dictcodes['ANUL'] = 'Annulment'
        self.dictcodes['ARVL'] = 'Arrival'
        self.dictcodes['AUTH'] = 'Author of the information'
        self.dictcodes['BAPL'] = 'LDS baptism'
        self.dictcodes['BAPM'] = 'Baptism'
        self.dictcodes['BARM'] = 'Bar Mitzvah'
        self.dictcodes['BASM'] = 'Bas (or Bat) Mitzvah'
        self.dictcodes['BIRT'] = 'Birth'
        self.dictcodes['CAST'] = 'Caste'
        self.dictcodes['CAUS'] = 'Cause of event, such as death'
        self.dictcodes['CENS'] = 'Census'
        self.dictcodes['CHIL'] = 'Child -- natural or adopted'
        self.dictcodes['CHR'] = 'Christening'
        self.dictcodes['CHRA'] = 'Adult Christening'
        self.dictcodes['CITY'] = 'City'
        self.dictcodes['CONC'] = 'Continue with the previous text; do not leave spaces'
        self.dictcodes['CONF'] = 'Confirmation'
        self.dictcodes['CONL'] = 'LDS Confirmation'
        self.dictcodes['CTRY'] = 'Country (name or code)'
        self.dictcodes['DATE'] = 'Date'
        self.dictcodes['DEAT'] = 'Death'
        self.dictcodes['DESC'] = 'Descendants'
        self.dictcodes['DIV'] = 'Divorce'
        self.dictcodes['DIVF'] = 'Divorce filed'
        self.dictcodes['DSCR'] = 'Physical description of a person, place, or thing'
        self.dictcodes['EDUC'] = 'Education'
        self.dictcodes['EMIG'] = 'Emigration'
        self.dictcodes['ENDL'] = 'Endowment (LDS)'
        self.dictcodes['ENGA'] = 'Engagement'
        self.dictcodes['EVEN'] = 'Event (noteworthy event)'
        self.dictcodes['EVENT1-13     '] = '_Fa1 through _Fa13 (FTW fact fields in FTM)'
        self.dictcodes['FCOM'] = 'First Communion'
        self.dictcodes['FOST'] = 'Foster'
        self.dictcodes['GIVN'] = 'Given name'
        self.dictcodes['GRAD'] = 'Graduation'
        self.dictcodes['HUSB'] = 'Husband'
        self.dictcodes['ILLE'] = 'Illegitimate'
        self.dictcodes['IMMI'] = 'Immigration'
        self.dictcodes['INDI'] = 'Individual'
        self.dictcodes['LANG'] = 'Language'
        self.dictcodes['LEGA'] = 'Legatee'
        self.dictcodes['LVG'] = 'Living'
        self.dictcodes['MARB'] = 'Marriage banns'
        self.dictcodes['MARC'] = 'Marriage contract'
        self.dictcodes['MARL'] = 'Marriage license'
        self.dictcodes['MARR'] = 'Marriage'
        self.dictcodes['MARS'] = 'Marriage settlement'
        self.dictcodes['MISC'] = 'Miscellaneous'
        self.dictcodes['NAME'] = 'Name'
        self.dictcodes['NATI'] = 'Nationality'
        self.dictcodes['NATU'] = 'Naturalization'
        self.dictcodes['NICK'] = 'Nickname'
        self.dictcodes['NOTE'] = 'Additional information'
        self.dictcodes['NPFX'] = 'Name prefix'
        self.dictcodes['NSFX'] = 'Name suffix (Jr. or Sr., for example)'
        self.dictcodes['OCCU'] = 'Occupation'
        self.dictcodes['ORDI'] = 'Ordinance (religious)'
        self.dictcodes['ORDL'] = 'Ordination (LDS)'
        self.dictcodes['ORDN'] = 'Ordination (non-LDS)'
        self.dictcodes['PHON'] = 'Phone number'
        self.dictcodes['PLAC'] = 'Place'
        self.dictcodes['POST'] = 'Postal code'
        self.dictcodes['PRIV'] = 'Private'
        self.dictcodes['PROB'] = 'Probate'
        self.dictcodes['RACE'] = 'Race'
        self.dictcodes['RELI'] = 'Religion (denomination)'
        self.dictcodes['RESI'] = 'Residence'
        self.dictcodes['RETI'] = 'Retirement'
        self.dictcodes['SEX'] = 'Sex (male or female)'
        self.dictcodes['SLGC'] = 'Sealing of a child (LDS)'
        self.dictcodes['SLGS'] = 'Sealing of a spouse (LDS)'
        self.dictcodes['SOUR'] = 'Source'
        self.dictcodes['SPFX'] = 'Surname prefix'
        self.dictcodes['SSN'] = 'Social Security number'
        self.dictcodes['STAE'] = 'State'
        self.dictcodes['STIL'] = 'Stillborn'
        self.dictcodes['SUBM'] = 'Submitter'
        self.dictcodes['SURN'] = 'Surname'
        self.dictcodes['TEL'] = 'Telephone Number'
        self.dictcodes['TEMP'] = 'Temple (LDS)'
        self.dictcodes['TIME'] = 'Time'
        self.dictcodes['TITL'] = 'Title'
        self.dictcodes['WIFE'] = 'Wife'
        self.dictcodes['WILL'] = 'Will'
        self.dictcodes['_CIRC'] = 'Circumscision'
        self.dictcodes['_DEG'] = 'Degree'
        self.dictcodes['_DEST'] = 'Destination'
        self.dictcodes['_DNA'] = 'DNA Markers'
        self.dictcodes['_ELEC'] = 'Elected'
        self.dictcodes['_EMPLOY'] = 'Employment'
        self.dictcodes['_EXCM'] = 'Excommunication'
        self.dictcodes['_FUN'] = 'Funeral'
        self.dictcodes['_HEIG'] = 'Height'
        self.dictcodes['_INIT'] = 'Initiatory (LDS)'
        self.dictcodes['_MDCL'] = 'Medical Condition'
        self.dictcodes['_MILT'] = 'Military Service Desc'
        self.dictcodes['_MILTID'] = 'Military Serial Number'
        self.dictcodes['_MISN'] = 'Mission (LDS)'
        self.dictcodes['_NAMS'] = 'Namesake'
        self.dictcodes['_ORDI'] = 'Ordinance'
        self.dictcodes['_ORIG'] = 'Origin'
        self.dictcodes['_SEPR'] = 'Separation'
        self.dictcodes['_WEIG'] = 'Weight'
        self.dictcodes['BURI'] = 'Burial'
        return

    def lookupcode(self, code):
        """Return an explanatory text for a code, or if the code doesn't exist, return 'Unknown' """
        return self.dictcodes.get(code, 'Unknown')

    def __str__(self):
        """Return the fomatted codes and explanatory text"""
        return pprint.pformat(self.dictcodes)

class IndividualCodes(object):
    """Class to associated Individual codes @Px@ with a formatted name. """

    def __init__(self):
        """Creat Dictionary"""
        self.indicode = {}

    def readindi(self, filename):
        """Read each line of file for ones containing individual name."""
        fname = open(filename)
        for line in fname:
            if line.find("@ INDI") > -1:
                tag = line.split('@')[1]
            if  line.find("1 NAME") > -1:
                name = self.validatename(line.split('1 NAME ')[1]).replace('\n', '')
                if len(tag) > 0 and len(name) > 0:
                    self.indicode[tag] = name
                    tag = ''
                    name = ''
        return



    def fullname(self, tag):
        """Return complete name without formatting."""
        indiname = self.indicode.get(tag, 'Unknown')
        if indiname == 'Unknown':
            return indiname
        else:
            return str(indiname.replace('/', ' ').strip())

    def givenname(self, tag):
        """Returns formatted given name."""
        indiname = self.indicode.get(tag, 'Unknown')
        if indiname == 'Unknown':
            return indiname
        else:
            return indiname.split('/')[0].split(' ')[0]

    def givennames(self, tag):
        """Returns formatted given names."""
        indiname = self.indicode.get(tag, 'Unknown')
        if indiname == 'Unknown':
            return indiname
        else:
            return (indiname.split('/')[0]).strip()

    def familyname(self, tag):
        """Returns family name."""
        indiname = self.indicode.get(tag, 'Unknown')
        if indiname == 'Unknown':
            return indiname
        else:
            return (indiname.split('/')[1]).strip()

    def validatename(self, name):
        """Validates that name has given and family name sections
           or returns a suitable Unknown holder"""
        gname = 'Unknown'
        fname = 'Unknown'
        nameparts = name.split('/')
        #Check for presence of family name
        if len(nameparts) == 3:
            if nameparts[1] <> '':
                fname = nameparts[1].strip()
        if len(nameparts) > 0:
            if nameparts[0] <> '':
                gname = nameparts[0].strip()
        return gname + '/' + fname

    def __str__(self):
        """Return the fomatted codes and explanatory text"""
        return pprint.pformat(self.indicode)


class FamilyCodes(object):
    """Class to associate individuals @Px@ to Families @Fx@ and vice versa. """
    def __init__(self):
        self.famcode = {}

    def readfam(self, filename):
        """Reverse reads GEDCOM file for Places associated with Families. Events
           appear associated with husband and or wife and are read on that
           basis."""
        familynames = []
        for line in reversed(open(filename).readlines()):
            if  line.find("WIFE @P") > -1:
                tag = line.split('@')[1] + ' WIFE'
                familynames.append(tag)
            if  line.find("HUSB @P") > -1:
                tag = line.split('@')[1] +' HUSB'
                familynames.append(tag)
            if  line.find("CHIL @P") > -1:
                tag = line.split('@')[1] +' CHIL'
                familynames.append(tag)
            if line.find('@ FAM') > -1:
                ftag = line.split('@')[1]
                self.famcode[ftag] = familynames
                familynames = []
        return

    def reverse_dict(self, dictionary):
        """Invert the family dictionary so that Individuals become keys and Family, the value."""
        reverse_dict = {}
        for key, value in dictionary.iteritems():
            if not isinstance(value, (list, tuple)):
                value = [value]
            for val in value:
                reverse_dict[val] = reverse_dict.get(val, [])
                reverse_dict[val].append(key)
        for key, value in reverse_dict.iteritems():
            if len(value) == 1:
                reverse_dict[key] = value[0]
        return reverse_dict

    def __str__(self):
        """Return the fomatted codes and explanatory text"""
        return pprint.pformat(self.famcode)

class ALLDICT(object):
    """Class to hold all dictionaries in order to pass to functions."""
    def __init__(self, codes, people, families, invfamilies):
        """Init"""
        self.codes = codes
        self.people = people
        self.families = families
        self.invfamilies = invfamilies

    def getcodes(self):
        """Get Code Dict"""
        return self.codes

    def getpeople(self):
        """Get People Dict"""
        return self.people

    def getfamilies(self):
        """Get Families Dict"""
        return self.families

    def getinvfamilies(self):
        """Get reversed Family Dict."""
        return self.invfamilies


def main():
    """Main function."""
    pass

if __name__ == '__main__':
    main()

