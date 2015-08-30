#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Finds inconsistencies in street names:
- street name of format 'X Y Z' is put as 'X Y Z' and 'Y X Z'
  (X, Y - first and second name, Z - lastname of some historical figure)
- name of person put with or without firstname
- name of person with title (like 'General') and without the title

Scripts works in 2 phases:
- parse the OSM file and extract (street name, city) pairs. Dump the pairs to a .txt file
- load (street name, city) pairs from the .txt file and look for incosistencies with
  following algorithm:
  1. for each street name, find the last segment of the name
  2. if the segment is on a list of exceptions (manually edited list of false positives),
     drop this segment
  3. for each segment left, find potential inconsistencies:
     - street name contains segment
     - segment city and candidate city is the same

"""

import os.path
import xml.etree.cElementTree as ET
import audit_street_names_exceptions


OSMFILE = "krakow_poland.osm"
STREET_NAMES_FILE = "street_city_names.txt"
# manually reviewed list of subsegments that should be excluded from inconsistency lookup - they're OK.
EXCLUDE_SUB = audit_street_names_exceptions.EXCLUDE_SUB
# Only values that have at least MIN_ENTRIES_FOR_REPORT_DISPLAY entries, will be fully displayed in
# final report
MIN_ENTRIES_FOR_REPORT_DISPLAY = -1
PRINT_FIXINGS = False


def extract_street_city_names(osmfile):
    """Extracts dictionary {(street name, city) => count} from osmfile."""
    osm_file = open(osmfile, "r")
    streets = {}

    for event, elem in ET.iterparse(osm_file, events=("start",)):
        street, city = None, None

        if elem.tag == "node":
            for tag in elem.iter('tag'):
                k = tag.get('k')
                if k == "addr:street":
                    street = tag.get('v')
                if k == "addr:city":
                    city = tag.get('v')

        # Some 'ways' use (name=streetname, hightway=...), other (addr:street, addr:city)
        if elem.tag == "way":
            tags = {}
            for tag in elem.iter('tag'):
                k, v = tag.get('k'), tag.get('v')
                # planned roads have extra description in parenthesis
                # e.g. "Południowa Obwodnica Niepołomic (koncepcja, przebieg orientacyjny)"
                v = v.split('(')[0]
                tags[k] = v
            # Either way has {name, highway} or {addr:street, addr:city?}
            if 'name' in tags and 'highway' in tags:
                highway = tags['highway']
                # some of the public transport stops have nodes with highway = ...
                if highway in ['platform']:
                    pass
                else:
                    street = tags['name']
            elif 'addr:street' in tags:
                street = tags['addr:street']
                if 'addr:city' in tags:
                    city = tags['addr:city']

        if street is not None:
            # some of the 'node' entries and all 'way' are missing addr:city tag.
            # As we're most interested in the Kraków street names, missing city is treated as if 'Kraków' was set.
            # Clearly, it's not the best solution, but it's easiest one to implement.
            # Alternative would take [lat, long] and check which city this particular location belongs to -
            # too complicated for our scenario.
            if city is None:
                city = u'Kraków'
            # Little bit of dancing with ',', whitechars and non-unicode charcaters.
            if ',' in street:
                street = street.replace(',', '')
            if ',' in city:
                city = city.replace(',', '')
            street = street.strip()
            city = city.strip()
            street = make_unicode(street)
            city = make_unicode(city)

            street_key = tuple([street, city])
            streets.setdefault(street_key, 0)
            streets[street_key] += 1

    return streets


def extract_or_load_street_city_names(osmfile, street_city_names_file):
    """Extracts (street name, city, count) pairs from osmfile, or loads them from street_city_names_file if it exists."""
    if os.path.isfile(street_city_names_file):
        # load the (street name, city) from checkpoint file.
        street_names = open(street_city_names_file, 'r').readlines()
        utf_street_names = []
        for street_name in street_names:
            street_name = street_name.decode('utf-8')
            segments = street_name[:-1].split(',')
            street, city, count = segments[0], segments[1], int(segments[2])
            utf_street_names.append(tuple([street, city, count]))
        return utf_street_names
    else:
        # extract the (street name, city) pairs and save them to checkpoint file.
        street_names = extract_street_city_names(osmfile)
        # convert the {(street, city) => count} dictionary to [(street, city, count)] list.
        street_names_list = []
        for k, v in street_names.iteritems():
            street_names_list.append(tuple([k[0], k[1], v]))
        street_names_list = sorted(street_names_list)

        # save the sorted list to file
        f = open(street_city_names_file, 'w')
        file_content = u'\n'.join([u'{0},{1},{2}'.format(x[0],x[1],x[2]) for x in street_names_list])
        file_content = file_content + u'\n'
        f.write(file_content.encode('utf-8'))
        f.close()
        return street_names_list


def make_unicode(v):
    """Returns v as properly encoded utf-8 string."""
    if type(v) == str:
        return unicode(v, errors='replace')
    if type(v) == unicode:
        return v
    raise Exception('unknown type: ', type(v))


def audit_street_names(street_cities):
    """For each street, finds other streets that has the same last segment (suffix?).

    Returns dictionary {suffix -> group of streets (street name, city, counter) with same suffix}
    """
    uniform_warns = {}

    for street_city in street_cities:
        street, city = street_city[0], street_city[1]
        sub = street.split(' ')
        last_sub = sub[-1]
        if last_sub in EXCLUDE_SUB:
            continue

        for another_name in street_cities:
            if last_sub in another_name[0] and another_name[0] != street and city in another_name[1] :
                uniform_warns.setdefault(last_sub, set())
                uniform_warns[last_sub].add(street_city)
                uniform_warns[last_sub].add(another_name)

    return uniform_warns


def report_street_name_inconsistency():
    """Prints reports about street inconsistencies to stdout."""
    streets = extract_or_load_street_city_names(OSMFILE, STREET_NAMES_FILE)
    # print '\n'.join(['{0},{1},{2}'.format(x[0],x[1],y) for x,y in streets.iteritems()])
    inconsistent_streets = audit_street_names(streets)
    # print inconsistent_streets

    totals = []
    for k, v in inconsistent_streets.iteritems():
        t = sum([vv[2] for vv in v])
        totals.append(t)
        if t >= MIN_ENTRIES_FOR_REPORT_DISPLAY:
            print k
            for vv in v:
                print u'\t{0}, {1} ({2})'.format(vv[0], vv[1], vv[2])
            print

    print 'Total number of inconsistent names: ', len(totals)
    print 'Total number of entries with inconsistent names: ', sum(totals)
    print 'Exeptions list size:', len(EXCLUDE_SUB)

    # print fixings?
    if PRINT_FIXINGS:
        print_streetname_fixings(inconsistent_streets)


def print_streetname_fixings(inconsistent_streets):
    print '----------------------------------------------'
    print 'FIXINGS'
    for k, v in inconsistent_streets.iteritems():
        if len(v) == 2:
            vlist = list(v)
            inconsistent, valid = vlist[0], vlist[1]
            if inconsistent[2] > valid:
                inconsistent, valid = valid, inconsistent
            print u'\'{0}\': \'{1}\','.format(inconsistent[0], valid[0])
        else:
            print
            print k
            for vv in v:
                print u'\t{0}, {1} ({2})'.format(vv[0], vv[1], vv[2])
            print


if __name__ == '__main__':
    report_street_name_inconsistency()
