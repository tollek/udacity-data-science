"""
Your task is to check the "productionStartYear" of the DBPedia autos datafile for valid values.
The following things should be done:
- check if the field "productionStartYear" contains a year
- check if the year is in range 1886-2014
- convert the value of the field to be just a year (not full datetime)
- the rest of the fields and values should stay the same
- if the value of the field is a valid year in range, as described above,
  write that line to the output_good file
- if the value of the field is not a valid year, 
  write that line to the output_bad file
- discard rows (neither write to good nor bad) if the URI is not from dbpedia.org
- you should use the provided way of reading and writing data (DictReader and DictWriter)
  They will take care of dealing with the header.

You can write helper functions for checking the data and writing the files, but we will call only the 
'process_file' with 3 arguments (inputfile, output_good, output_bad).
"""
import csv
import pprint
import time

INPUT_FILE = 'autos.csv'
OUTPUT_GOOD = 'autos-valid.csv'
OUTPUT_BAD = 'FIXME-autos.csv'
PRODUCTION_START_YEAR = 'productionStartYear'

def process_file(input_file, output_good, output_bad):

    with open(input_file, "r") as f:
        reader = csv.DictReader(f)
        header = reader.fieldnames
        # pass 3 first rows (description, schema and ...?)
        for i in xrange(0, 3):
            reader.next()

        good_rows = []
        bad_rows = []
        for row in reader:
            # validate URI value
            if row['URI'].find("dbpedia.org") < 0:
                continue
            # print row
            start_year = row[PRODUCTION_START_YEAR]
            if start_year == 'NULL':
                bad_rows.append(row)
                continue
            # no good way to parse time offset!
            parsed_date = time.strptime(start_year[:-6], "%Y-%m-%dT%H:%M:%S")
            if parsed_date.tm_year < 1886 or parsed_date.tm_year > 2014:
                bad_rows.append(row)
                continue

            row[PRODUCTION_START_YEAR] = parsed_date.tm_year
            good_rows.append(row)

        print len(good_rows)
        print len(bad_rows)

    # This is just an example on how you can use csv.DictWriter
    # Remember that you have to output 2 files
    with open(output_good, "w") as g:
        writer = csv.DictWriter(g, delimiter=",", fieldnames= header)
        writer.writeheader()
        for row in good_rows:
            writer.writerow(row)

    with open(output_bad, "w") as g:
        writer = csv.DictWriter(g, delimiter=",", fieldnames= header)
        writer.writeheader()
        for row in bad_rows:
            writer.writerow(row)


def test():

    process_file(INPUT_FILE, OUTPUT_GOOD, OUTPUT_BAD)


if __name__ == "__main__":
    test()
