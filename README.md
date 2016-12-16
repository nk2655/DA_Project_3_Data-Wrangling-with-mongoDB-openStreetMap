# Data_Wrangling_with_mongoDB_OpenStreetMap
by NK Zhehua Zou

### Description of scripts
##### 1) street.py  
This file use for data wrangling, it will audit street name and corret them.  
We will import is_street_name and update_street function from here to shape.py  
##### 2) zipcode.py  
This file also use for data wrangling, it will audit zipcode and corret them.  
We will import is_zipcode and update_zipcode function from here to shape.py  
##### 3) shape.py  
This is a multifunctional script file.  
we use shape_elemnt function to wrangle data and parse it.  
We use process_map to write json and output to mongoDB.  
  
### 1. Data Audit
##### Tags
Parse through the San Jose dataset with ElementTree and count the number of unique element types to get an overall understanding of the data by using count_tags function.  
{'bounds': 1, 'member': 115, 'nd': 21564, 'node': 13332, 'osm': 1, 'relation': 21, 'tag': 7128, 'way': 3721}  
  
##### Keys Type
For the follinwg function: key_type & process_key. We check the "k" value for each.   
"lower", for tags that contain only lowercase letters and are valid.  
"lower_colon", for otherwise valid tags with a colon in their names.  
"problemchars", for tags with problematic characters.  
{'lower': 6751, 'lower_colon': 363, 'other': 14, 'problemchars': 0}  
  
##### Users
94 peoples invovlved in the map editing.  
  
### 2. Problems Encountered in the Map
After initially downloading a small sample size of the San Jose area and running it, I noticed two main problems with the data, which I will discuss in the following order:  
1) Abbreviated street names ('Branham Ln')  
2) Inconsistent postal codes ('CA950543', '95014-1899')  
  
##### Abbreviated Street Names
Once the data was imported to MongoDB, some basic querying revealed street name abbreviations. I updated all substrings in problematic address strings, such that 'Branham Ln' becomes 'Branham Lane'.  
1) The main problem we encountered in this dataset come from the street name abbreviation inconsistency. We build the regex matching the last element in the string, where usually the street type is based. Then we come up with a list of mapping that need not to be cleaned.  
2) audit_street_type function search the input string for the regex. If there is a match and it is not within the 'expected' list, add the match as a key and add the string to the set.  
3) is_street_name function looks at the attribute k if k='addre:street'.  
4) audit functio will return the list that match previous two functions.  
5) After that, we would do a pretty print the output of the audit. With the list of all the abbreviated street types we can understand and fill-up our 'mapping' dictionary as a preparatio to convert these street name into proper form.  
6) update_name is the last step of the process, which take the old name and update them with a better name.  
  
##### Zip Codes
Postal code strings posed a different sort of problem, forcing a decision to strip all leading and trailing characters before and after the main 5-digit zip code. This effectually dropped all leading state characters (as in 'CA950543') and 4-digit zip code extensions following a hyphen ('95014-1899'). This 5-digit constriction benefits MongoDB aggregation calls on postal codes.  
1) Although most of the zip code is correct, there're still a lot of zip code with incorrect 5 digit formats. We will process it like update street name.  
2 )The output of the clean zip code is summarised below. There are the format of 5 digits or string 'None'.  
  
### 3. Data Overview
This section contains basic statistics about the dataset and the MongoDB queries used to gather them.  
Preparing for MongoDB by converting XML to JSON  
In order to transform the data from XML to JSON, we need to follow these rules:  
1) Process only 2 types of top level tags: "node" and "way"  
2) All attributes of "node" and "way" should be turned into regular key/value pairs, except: attributes in the CREATED array should be added under a key "created", attributes for latitude and longitude should be added to a "pos" array, for use in geospacial indexing. Make sure the values inside "pos" array are floats and not strings.  
3) If second level tag "k" value contains problematic characters, it should be ignored  
4) If second level tag "k" value starts with "addr:", it should be added to a dictionary "address"  
5) If second level tag "k" value does not start with "addr:", but contains ":", you can process it same as any other tag.  
6) If there is a second ":" that separates the type/direction of a street, the tag should be ignored  
After all the cleaning and data transformation are done, we would use last function process_map and convert the file from XML into JSON format  

##### File sizes
The original OSM file is 3.329866 MB  
The JSON file is 3.795992 MB  
The number of documents is 17053  
The number of node is 13332  
The number of way is 3721  
The number of unique users is 91  
The first contributor is TELCOM IP with 4921 contributions.  
There is 22 users appearing only once.  
  
### 4. Additional Ideas
Contributor statistics and suggestion  
According to these results below, we found unbelievable truth.  
1) Best contributor gave 28% documents, greater than 1/4 of total contributions.  
2) Three contributors also over half of total contributions, it means top 2 and top 3 contributors are far behind top 1 contributors.  
3) Just 20 contributors already gave 96% of total documents, it means rest of people almost have not any contributors in here even if still have 24% contributors gave one post.  
4) Eeery contributor shall gave 187 documents by average contribution, but most of people can't close to this number.  
5) What incentives should we increase? Perhaps we can refer to the experience of waze, which is a great application for navigation app. We can be divided different levels according to contribution, each level users will enjoy different privileges, badges and rewards.  
  
##### Additional data exploration using MongoDB queries
1) 17053 people living in this area.  
2) We found most amenities are bus stations, gas stations (fuel) and schools in this area. Let's explorating them.  
3) I am a bit suprised for this result, there has many long distance bus station in this small area. I though there has many caltrain or city bus stations.  
4) It looks like Grifo has most gas stations in this area, no much suprised for this result, but I can't belive only 1 Vista and have not some popular gas station like Shell in here.  
5) Pescador is the most popular restaurant in this area, they have 2 restaurant in here. After google it, I found this is a fish restaurant and keep a lower rate 3 in 5 stars. Interesting, they don't have delicious food for residents?  
  
### 5. Conclusion
1) The map about the city of San Jose is relatively clean so I could retrieve some interesting content. But still the data is not entirely clean.  
2) The data contains some mistakes or different references for the same feature. So I had to clean the data programmatically for the street and the postal codes.  
3) When we audit the data, it was very clear that although there are minor error caused by human input, the dataset is fairly well-cleaned. Considering there're hundreds of contributors for this map, there is a great numbers of human errors in this project. I'd recommend a srtuctured input form so everyone can input the same data format to reduce this error.  
4) We can incentivize users by gamify the contribution process, then we can create a recommendation engine to leverage these data (eg. restaurant recommendation, building, etc).  
5) OpenStreetMaps is an open source project, there're still a lot of areas left unexplored as people tend to focus on a certain key areas and left other part outdated. Since each node has a coordinate (lattitude & longtitude), we can resolve this issue by cross-referencing/cross-validating missing data from other database like Google API.
