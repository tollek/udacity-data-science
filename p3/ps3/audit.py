#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
In this problem set you work with cities infobox data, audit it, come up with a
cleaning idea and then clean it up. In the first exercise we want you to audit
the datatypes that can be found in some particular fields in the dataset.
The possible types of values can be:
- NoneType if the value is a string "NULL" or an empty string ""
- list, if the value starts with "{"
- int, if the value can be cast to int
- float, if the value can be cast to float, but CANNOT be cast to int.
   For example, '3.23e+07' should be considered a float because it can be cast
   as float but int('3.23e+07') will throw a ValueError
- 'str', for all other values

The audit_file function should return a dictionary containing fieldnames and a 
SET of the types that can be found in the field. e.g.
{"field1: set([float, int, str]),
 "field2: set([str]),
  ....
}

All the data initially is a string, so you have to do some checks on the values
first.
"""
import codecs
import csv
import json
import pprint

CITIES = 'cities.csv'

FIELDS = ["name", "timeZone_label", "utcOffset", "homepage", "governmentType_label", "isPartOf_label", "areaCode", "populationTotal", 
          "elevation", "maximumElevation", "minimumElevation", "populationDensity", "wgs84_pos#lat", "wgs84_pos#long", 
          "areaLand", "areaMetro", "areaUrban"]


def is_int(value):
    try:
        unused = int(value)
        return True
    except ValueError:
        return False

def is_float(value):
    try:
        unused = float(value)
        return True
    except ValueError:
        return False

def audit_file(filename, fields):
    fieldtypes = {}

    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile)
        # Skip 3 lines (extra headr data)
        for unused in xrange(0, 3):
            reader.next()

        for row in reader:
            for f in fields:
                value = row[f]

                value_type = type(value)
                if value == 'NULL' or value == "":
                    value_type = type(None)
                elif len(value) > 0 and value[0] == '{':
                    value_type = type([])
                elif is_int(value):
                    value_type = type(1)
                elif is_float(value):
                    value_type = type(1.1)

                fieldtypes.setdefault(f, set())
                fieldtypes[f].add(value_type)

    return fieldtypes


def test():
    fieldtypes = audit_file(CITIES, FIELDS)

    pprint.pprint(fieldtypes)

    assert fieldtypes["areaLand"] == set([type(1.1), type([]), type(None)])
    assert fieldtypes['areaMetro'] == set([type(1.1), type(None)])
    
if __name__ == "__main__":
    test()

