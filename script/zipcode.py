import re
import xml.etree.cElementTree as ET
from collections import defaultdict
import sys
data = 'data/sample.osm'

''' In this dataset, some zipcode are invalid format such as CUPERTINO, 140010, etc.
If the zipcode is not digit or start without 95, add to invalid zicodes.'''
def audit_zipcode(invalid_zipcodes, zipcode):
    twoDigits = zipcode[0:2]
    if not twoDigits.isdigit():
        invalid_zipcodes[twoDigits].add(zipcode)
    elif twoDigits != 95:
        invalid_zipcodes[twoDigits].add(zipcode)
        
def is_zipcode(elem):
    return (elem.tag == "tag") and (elem.attrib['k'] == 'addr:postcode')

''' We use defaultdict to defined invalid_zipcodes as a set
use ET to parse data and implement for loop
check element tag is node or way and go to next for loop
if they meet is_zipcode() function, make suke their attrib is postcode,
then implement audit_zipcode() function to get invalid zipcodes	'''
def audit_zip(osmfile):
    osm_file = open(osmfile, 'r')
    invalid_zipcodes = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=('start',)):
        if elem.tag == 'node' or elem.tag == 'way':
            for tag in elem.iter('tag'):
                if is_zipcode(tag):
                    audit_zipcode(invalid_zipcodes,tag.attrib['v'])
    return invalid_zipcodes

''' We check zipcode, if start with CA, we go to next step, return to first 5 digitals, drop last 4 digitals.
If zipcode is digit an start with 95, also return to first 5 digitals.
other situation such as CUPERTINO or 140010, all return to string None.
Remeber, must return a sting, it will not work even you want to return to 95001,Regular expression also will return to an array.
'''	
def update_zipcode(zipcode):
    testNum = re.findall('[a-zA-Z]*', zipcode)
    if testNum:
        testNum = testNum[0]
    testNum.strip()
    if testNum == 'CA':
        return (re.findall(r'\d+', zipcode))[0]
    elif re.findall(r'^(95\d{3})-\d{4}$', zipcode):
        return re.findall(r'\d{5}', zipcode)[0]
    else:
        return 'None'