import json

with open('RES_OUTPUT.json') as f:
  infile = json.load(f)


#items = infile["items"][0]
#print("isEnterpriseOwned" in items)
#print(items["id"])
print(len(infile))


