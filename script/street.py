import re
import xml.etree.cElementTree as ET
from collections import defaultdict
import string
import sys
data = 'data/sample.osm'

street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)
street_abbrev_re = re.compile(r'^([a-z]){1}\.?(\s)+', re.IGNORECASE)
expected = ['Avenue', 'Boulevard', 'Commons', 'Court', 'Drive', 'Lane', 'Parkway', 
                         'Place', 'Road', 'Square', 'Street', 'Trail']
mapping_street = {'Ave'  : 'Avenue',
           'Blvd' : 'Boulevard',
           'Dr'   : 'Drive',
           'Ln'   : 'Lane',
           'Pkwy' : 'Parkway',
           'Rd'   : 'Road',
           'Rd.'   : 'Road',
           'St'   : 'Street',
           'street' :'Street',
           'Ct'   : 'Court',
           'Cir'  : 'Circle',
           'Cr'   : 'Court',
           'ave'  : 'Avenue',
           'Hwg'  : 'Highway',
           'Hwy'  : 'Highway',
           'Sq'   : 'Square'}
mapping_abbrev = { 'W ': 'West ', 'S ': 'South ', 'N ': 'North ', 'E ': 'East ',\
                   'W. ': 'West ', 'S. ': 'South', 'N. ': 'North ', 'E. ': 'East '}

def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)

def is_street_name(elem):
    return (elem.tag == 'tag') and (elem.attrib['k'] == 'addr:street')

def audit(osmfile):
    osm_file = open(osmfile, 'r')
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=('start',)):
        if elem.tag == "node" or elem.tag == 'way':
            for tag in elem.iter('tag'):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
    return street_types

def update_street(name, mapping_street, mapping_abbrev):
    m_1 = street_type_re.search(name)
    if m_1:
        street_type = m_1.group()
        if street_type in mapping_street:
            name = re.sub(street_type, mapping_street[street_type], name) # update street name to full street name
    m_2 = street_abbrev_re.search(name)
    if m_2:
        street_abbrev = m_2.group()
        if street_abbrev in mapping_abbrev.keys():
            name = re.sub(street_abbrev, mapping_abbrev[street_abbrev], name) # Update W , E, N, S to West, East, North, South
    name = string.capwords(name) # capitalizing first letter of all words in problematic address
    return name