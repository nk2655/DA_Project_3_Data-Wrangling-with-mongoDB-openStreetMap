import re
import xml.etree.cElementTree as ET
from collections import defaultdict
import sys
data = 'data/sample.osm'

def audit_zipcode(invalid_zipcodes, zipcode):
    twoDigits = zipcode[0:2]
    if not twoDigits.isdigit():
        invalid_zipcodes[twoDigits].add(zipcode)
    elif twoDigits != 95:
        invalid_zipcodes[twoDigits].add(zipcode)
        
def is_zipcode(elem):
    return (elem.tag == "tag") and (elem.attrib['k'] == 'addr:postcode')

def audit_zip(osmfile):
    osm_file = open(osmfile, 'r')
    invalid_zipcodes = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=('start',)):
        if elem.tag == 'node' or elem.tag == 'way':
            for tag in elem.iter('tag'):
                if is_zipcode(tag):
                    audit_zipcode(invalid_zipcodes,tag.attrib['v'])
    return invalid_zipcodes
	
def update_zipcode(zipcode):
    testNum = re.findall('[a-zA-Z]*', zipcode)
    if testNum:
        testNum = testNum[0]
    testNum.strip()
    if testNum == 'CA':
        return (re.findall(r'\d+', zipcode))[0]
    elif re.match(r'^95\d+', zipcode):
        return re.findall(r'\d{5}', zipcode)[0]
    else:
        return 'None'