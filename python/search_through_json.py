

import json

with open('practice.json') as f:
  infile = json.load(f)


items = infile["items"][0]
print("isEnterpriseOwned" in items)
print(items["id"])
#print(items)

