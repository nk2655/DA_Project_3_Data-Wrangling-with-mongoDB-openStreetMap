# Data-Wrangling-with-mongoDB-OpenStreetMap
Description of Project  
• Downloaded map of San Jose from https://www.openstreetmap.org and used data munging techniques to clean the OpenStreetMap data.  
• Technologies Used: pandas, re, ET, pymongo, json  

### Description of scripts
##### 1) street.py  
This file use for data wrangling, it will audit street name and corret them.  
Import is_street_name and update_street function from here to shape.py  
##### 2) zipcode.py  
This file also use for data wrangling, it will audit zipcode and corret them.  
Import is_zipcode and update_zipcode function from here to shape.py  
##### 3) shape.py  
This is a multifunctional script file.  
From street import is_street_name, update_street, mapping_street, mapping_abbrev to cleaning street name  
From zipcode import is_zipcode, update_zipcode to cleaning zipcode  
Use shape_elemnt function to wrangle data and parse it.  
Use process_map to write json and output to mongoDB.
