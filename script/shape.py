import sys
sys.path.append("script/")
from street import is_street_name, update_street, mapping_street, mapping_abbrev
from zipcode import is_zipcode, update_zipcode
import xml.etree.cElementTree as ET
import re
from pymongo import MongoClient
import codecs
import json

data = 'data/sample.osm'

client = MongoClient()
db=client.project
db.doc.drop()

problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')
address_regex = re.compile(r'^addr\:')
street_regex = re.compile(r'^street')

CREATED = [ "version", "changeset", "timestamp", "user", "uid"]

def shape_element(element):
    for el_tag in element.iter('tag'):
        key_tag = el_tag.attrib['k']
        if problemchars.search(key_tag):# for cleaning data from problematic characters
            continue
        if is_street_name(el_tag): # Fixing Street names
            el_tag.attrib['v'] = update_street(el_tag.attrib['v'], mapping_street, mapping_abbrev)
        if is_zipcode(el_tag):
            el_tag.attrib['v'] = update_zipcode(el_tag.attrib['v'])
        
    node = {}
    if element.tag == "node" or element.tag == "way" :
        node['type'] = element.tag
        address = {}  # initialize empty address
        
        for a in element.attrib: # parsing through attributes
            if a in CREATED:
                if 'created' not in node:
                    node['created'] = {}
                node['created'][a] = element.get(a)
            elif a in ['lat', 'lon']:
                continue
            else:
                node[a] = element.get(a)

        if 'lat' in element.attrib and 'lon' in element.attrib: # populate position
            node['pos'] = [float(element.get('lat')), float(element.get('lon'))]

        for e in element: # parse second-level tags for nodes
            if e.tag == 'nd': # parse second-level tags for ways and populate `node_refs`
                if 'node_refs' not in node:
                    node['node_refs'] = []
                if 'ref' in e.attrib:
                    node['node_refs'].append(e.get('ref'))
            if e.tag != 'tag' or 'k' not in e.attrib or 'v' not in e.attrib: # drop elements not-tag / without `k`/`v`
                continue
            key = e.get('k')
            val = e.get('v')
            if problemchars.search(key): # skip problematic characters
                continue
            elif address_regex.search(key): # parse address k-v pairs
                key = key.replace('addr:', '')
                address[key] = val
            else: # catch-all
                node[key] = val
        if len(address) > 0: # compile address
            node['address'] = {}
            street_full = None
            street_dict = {}
            street_format = ['prefix', 'name', 'type']
            for key in address: # parse through address objects
                val = address[key]
                if street_regex.search(key):
                    if key == 'street':
                        street_full = val
                    elif 'street:' in key:
                        street_dict[key.replace('street:', '')] = val
                else:
                    node['address'][key] = val
            if street_full: # assign street_full or fallback to compile street dict
                node['address']['street'] = street_full
            elif len(street_dict) > 0:
                node['address']['street'] = ' '.join([street_dict[key] for key in street_format])
        return node
    else:
        return None
		
def process_map(file_in, pretty = False):
    file_out = "{0}.json".format(file_in)
    data = []
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            if el:
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2)+"\n")
                else:
                    fo.write(json.dumps(el) + "\n")
    return data

db.doc.insert_many(process_map(data));