import json
import re
from pprint import pprint 

d = {}
with open('file.json') as f:
    for lst in f.readlines():
        if "instance" in lst:
            instance_id = lst.split(':')[1].replace('"','').replace(',','').strip()
            d['instance'] = instance_id
        if "security" in lst:
            sg_id = lst.split(':')[1].replace('"','').replace(',','').strip()
            d['security'] = sg_id
print(d)
