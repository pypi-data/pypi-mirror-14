from __future__ import print_function

from parseratorvariable import ParseratorType
import usaddress
import re

STREET = (('address number',   ('AddressNumberPrefix',
                                'AddressNumber',
                                'AddressNumberSuffix')),
          ('street direction', ('StreetNamePreDirectional',
                                'StreetNamePostDirectional')),
          ('street name',      ('StreetNamePreModifier',
                                'StreetName',
                                'StreetNamePostModifier')),
          ('street type',      ('StreetNamePostType',
                                'StreetNamePreType')),
          ('occupancy type',   ('OccupancyType',)),
          ('occupancy id',     ('OccupancyIdentifier',)),
          ('building name',    ('BuildingName',)))

BOX =  (('box group id',   ('USPSBoxGroupID',)),
        ('box id',         ('USPSBoxID',)))

INTERSECTION_A = (('street direction A', ('StreetNamePreDirectional',
                                          'StreetNamePostDirectional')),
                  ('street name A',      ('StreetNamePreModifier',
                                          'StreetName',
                                          'StreetNamePostModifier')),
                  ('street type A',      ('StreetNamePostType',
                                          'StreetNamePreType')))
INTERSECTION_B = (('street direction B', ('SecondStreetNamePreDirectional',
                                          'SecondStreetNamePostDirectional')),
                  ('street name B',      ('SecondStreetNamePreModifier',
                                          'SecondStreetName',
                                          'SecondStreetNamePostModifier')),
                  ('street type B',      ('SecondStreetNamePostType',
                                          'SecondStreetNamePreType')))


class USAddressType(ParseratorType) :
    type = "Address"
    
    def tagger(self, field) :
        return normalize(field)

    def __init__(self, definition) :
        self.components = (('Street Address', self.compareFields, STREET),
                           ('PO Box', self.compareFields, BOX),
                           ('Intersection', self.comparePermutable, 
                            INTERSECTION_A, INTERSECTION_B))

        super(USAddressType, self).__init__(definition)

def street_direction(field) :
    aliases = {'north' : 'n',
               'south' : 's',
               'east'  : 'e',
               'west'  : 'w',
               'northeast' : 'ne',
               'northwest' : 'nw',
               'southeast' : 'se',
               'southwest' : 'sw'}

    cleaned = re.sub('[\W_]+', '', field.lower())
    return aliases.get(cleaned, cleaned)

def normalize(field) :
    transforms = {'StreetNamePreDirectional'  : street_direction,
                  'StreetNamePostDirectional' : street_direction}

    tags, address_type = usaddress.tag(field)
    for tag in transforms :
        if tag in tags :
            tags[tag] = transforms[tag](tags[tag])

    return tags, address_type

