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
       associate them with explanatory text.
       http://homepages.rootsweb.ancestry.com/~pmcbride/gedcom/55gcappa.htm """

    def __init__(self):
        """Create dictionary"""
        self.dictcodes = {}

    def readcodes(self):
        """Read GEDCOM codes."""
        """Each GEDCOM code is preceded by a number to allow a possible logical sorting
        of events that occur in the same year eg. 10 Birth precedes 20 Baptism. Generic Codes are
        indicated by the use of 50."""
        self.dictcodes['ADDR'] = '50 Address, usually mailing address'
        self.dictcodes['ADR1'] = '50 First line of an address'
        self.dictcodes['ADR2'] = '50 Second line of an address'
        self.dictcodes['ADOP'] = '20 Adoption'
        self.dictcodes['AFN'] = '50 Ancestral File number (LDS)'
        self.dictcodes['AGE'] = '50 Age at time of event'
        self.dictcodes['ALIA'] = '50 Alias'
        self.dictcodes['ANUL'] = '50 Annulment'
        self.dictcodes['ARVL'] = '50 Arrival'
        self.dictcodes['AUTH'] = '50 Author of the information'
        self.dictcodes['BAPL'] = '50 LDS baptism'
        self.dictcodes['BAPM'] = '20 Baptism'
        self.dictcodes['BARM'] = '50 Bar Mitzvah'
        self.dictcodes['BASM'] = '50 Bas (or Bat) Mitzvah'
        self.dictcodes['BIRT'] = '10 Birth'
        self.dictcodes['CAST'] = '50 Caste'
        self.dictcodes['CAUS'] = '50 Cause of event, such as death'
        self.dictcodes['CENS'] = '50 Census'
        self.dictcodes['CHIL'] = '50 Child -- natural or adopted'
        self.dictcodes['CHR'] = '20 Christening'
        self.dictcodes['CHRA'] = '50 Adult Christening'
        self.dictcodes['CITY'] = '50 City'
        self.dictcodes['CONC'] = '50 Continue with the previous text; do not leave spaces'
        self.dictcodes['CONF'] = '50 Confirmation'
        self.dictcodes['CONL'] = '50 LDS Confirmation'
        self.dictcodes['CTRY'] = '50 Country (name or code)'
        self.dictcodes['DATE'] = '50 Date'
        self.dictcodes['DEAT'] = '80 Death'
        self.dictcodes['DESC'] = '50 Descendants'
        self.dictcodes['DIV'] = '50 Divorce'
        self.dictcodes['DIVF'] = '50 Divorce filed'
        self.dictcodes['DSCR'] = '50 Physical description of a person, place, or thing'
        self.dictcodes['EDUC'] = '50 Education'
        self.dictcodes['EMIG'] = '50 Emigration'
        self.dictcodes['ENDL'] = '50 Endowment (LDS)'
        self.dictcodes['ENGA'] = '35 Engagement'
        self.dictcodes['EVEN'] = '50 Event (noteworthy event)'
        self.dictcodes['EVENT1-13'] = '50 _Fa1 through _Fa13 (FTW fact fields in FTM)'
        self.dictcodes['FCOM'] = '50 First Communion'
        self.dictcodes['FOST'] = '30 Foster'
        self.dictcodes['GIVN'] = '50 Given name'
        self.dictcodes['GRAD'] = '50 Graduation'
        self.dictcodes['HUSB'] = '50 Husband'
        self.dictcodes['ILLE'] = '50 Illegitimate'
        self.dictcodes['IMMI'] = '50 Immigration'
        self.dictcodes['INDI'] = '50 Individual'
        self.dictcodes['LANG'] = '50 Language'
        self.dictcodes['LEGA'] = '50 Legatee'
        self.dictcodes['LVG'] = '50 Living'
        self.dictcodes['MARB'] = '40 Marriage banns'
        self.dictcodes['MARC'] = '40 Marriage contract'
        self.dictcodes['MARL'] = '40 Marriage license'
        self.dictcodes['MARR'] = '45 Marriage'
        self.dictcodes['MARS'] = '40 Marriage settlement'
        self.dictcodes['MISC'] = '50 Miscellaneous'
        self.dictcodes['NAME'] = '50 Name'
        self.dictcodes['NATI'] = '50 Nationality'
        self.dictcodes['NATU'] = '50 Naturalization'
        self.dictcodes['NICK'] = '50 Nickname'
        self.dictcodes['NOTE'] = '50 Additional information'
        self.dictcodes['NPFX'] = '50 Name prefix'
        self.dictcodes['NSFX'] = '50 Name suffix (Jr. or Sr., for example)'
        self.dictcodes['OCCU'] = '50 Occupation'
        self.dictcodes['ORDI'] = '50 Ordinance (religious)'
        self.dictcodes['ORDL'] = '50 Ordination (LDS)'
        self.dictcodes['ORDN'] = '50 Ordination (non-LDS)'
        self.dictcodes['PHON'] = '50 Phone number'
        self.dictcodes['PLAC'] = '50 Place'
        self.dictcodes['POST'] = '50 Postal code'
        self.dictcodes['PRIV'] = '50 Private'
        self.dictcodes['PROB'] = '95 Probate'
        self.dictcodes['RACE'] = '50 Race'
        self.dictcodes['RELI'] = '50 Religion (denomination)'
        self.dictcodes['RESI'] = '50 Residence'
        self.dictcodes['RETI'] = '50 Retirement'
        self.dictcodes['SEX'] = '50 Sex (male or female)'
        self.dictcodes['SLGC'] = '50 Sealing of a child (LDS)'
        self.dictcodes['SLGS'] = '50 Sealing of a spouse (LDS)'
        self.dictcodes['SOUR'] = '50 Source'
        self.dictcodes['SPFX'] = '50 Surname prefix'
        self.dictcodes['SSN'] = '50 Social Security number'
        self.dictcodes['STAE'] = '50 State'
        self.dictcodes['STIL'] = '10 Stillborn'
        self.dictcodes['SUBM'] = '50 Submitter'
        self.dictcodes['SURN'] = '50 Surname'
        self.dictcodes['TEL'] = '50 Telephone Number'
        self.dictcodes['TEMP'] = '50 Temple (LDS)'
        self.dictcodes['TIME'] = '50 Time'
        self.dictcodes['TITL'] = '50 Title'
        self.dictcodes['WIFE'] = '50 Wife'
        self.dictcodes['WILL'] = '50 Will'
        self.dictcodes['_CIRC'] = '20 Circumscision'
        self.dictcodes['_DEG'] = '50 Degree'
        self.dictcodes['_DEST'] = '50 Destination'
        self.dictcodes['_DNA'] = '50 DNA Markers'
        self.dictcodes['_ELEC'] = '50 Elected'
        self.dictcodes['_EMPLOY'] = '50 Employment'
        self.dictcodes['_EXCM'] = '50 Excommunication'
        self.dictcodes['_FUN'] = '90 Funeral'
        self.dictcodes['_HEIG'] = '50 Height'
        self.dictcodes['_INIT'] = '50 Initiatory (LDS)'
        self.dictcodes['_MDCL'] = '50 Medical Condition'
        self.dictcodes['_MILT'] = '50 Military Service Desc'
        self.dictcodes['_MILTID'] = '50 Military Serial Number'
        self.dictcodes['_MISN'] = '50 Mission (LDS)'
        self.dictcodes['_NAMS'] = '50 Namesake'
        self.dictcodes['_ORDI'] = '50 Ordinance'
        self.dictcodes['_ORIG'] = '50 Origin'
        self.dictcodes['_SEPR'] = '50 Separation'
        self.dictcodes['_WEIG'] = '50 Weight'
        self.dictcodes['BURI'] = '90 Burial'
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

