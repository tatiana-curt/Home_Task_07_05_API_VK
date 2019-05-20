import json
from pprint import pprint

with open("groups.json", encoding="cp1251") as datafile:
  json_data = json.load(datafile)
print(json_data)
pprint(json_data)