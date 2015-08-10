#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv

CITIES = 'cities.csv'
AUDIT_FIELDS = ['name', 'populationTotal', 'areaMetro', 'postalCode']

def other_fields(filename = CITIES):
    with open(filename, "r") as f:
        reader = csv.DictReader(f)
        # skip lines
        for i in xrange(0, 3):
            reader.next()

        values = {}
        for row in reader:
            for f in AUDIT_FIELDS:
                value = row[f]
                values.setdefault(f, [])
                values[f].append(value)

        for k, v in values.iteritems():
            print k
            print '\n\t' + '\n\t'.join(v)
            print


if __name__ == "__main__":
    other_fields()
