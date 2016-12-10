import re
from collections import defaultdict
import xml.etree.cElementTree as ET

def audit_zipcode(invalid_zipcodes, zipcode):
    twoDigits = zipcode[0:2]
    if not twoDigits.isdigit():
        invalid_zipcodes[twoDigits].add(zipcode)
    elif twoDigits != 95:
        invalid_zipcodes[twoDigits].add(zipcode)
        
def is_zipcode(elem):
    return (elem.attrib['k'] == 'addr:postcode')

def audit_zip(osmfile):
    osm_file = open(osmfile, 'r')
    invalid_zipcodes = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=('start',)):
        if elem.tag == 'node' or elem.tag == 'way':
            for tag in elem.iter('tag'):
                if is_zipcode(tag):
                    audit_zipcode(invalid_zipcodes,tag.attrib['v'])
    return invalid_zipcodes