#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Give a reference list of restaurant names, checks how much of the places from references list can be found
on the map.

"""

import xml.etree.cElementTree as ET
import restaurants.extract_restaurants as restaurants

OSMFILE = "krakow_poland.osm"

def audit_restaurant_completeness(osmfile, rest_names):
    """Returns lists (found, not_found), each with names of restaurants that was found/not found in OSM file."""
    osm_file = open(osmfile, "r")
    found, not_found = set(), set()

    for event, elem in ET.iterparse(osm_file, events=("start",)):
        if elem.tag == "node":
            restaurant = False
            name = ''
            for tag in elem.iter('tag'):
                k = tag.get('k')
                if k == "name":
                    name = tag.get('v')
                if k == "amenity" and tag.get('v') == 'restaurant':
                    restaurant = True

            if restaurant:
                for rest_name in rest_names:
                    if rest_name in name:
                        found.add(rest_name)

    for rest_name in rest_names:
        if rest_name not in found:
            not_found.add(rest_name)

    return list(found), list(not_found)


def report_restaurant_completeness(found, not_found):
    f, nf = len(found), len(not_found)
    print 'Found: ', f
    print 'Not found: ', nf
    print 'Not found %: ', (1.0 * nf) / (f + nf)
    print
    print 'Not found restaurants:'
    for r in not_found:
        print '\t', r
    print


if __name__ == '__main__':
    rest_names = restaurants.load_restaurants('restaurants/' + restaurants.RESTAURANTS_LIST)
    found, not_found = audit_restaurant_completeness(OSMFILE, rest_names)
    report_restaurant_completeness(found, not_found)
