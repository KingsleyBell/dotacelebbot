#Get hero and ability data from dota2.com

import requests
import json
import operator
import re

def striphtml(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)

#Website to scrape top 100 celebrities from
website = "http://www.dota2.com/jsfeed/heropediadata?feeds=abilitydata,herodata&v=3487285YS81IGG3JCd6&l=english"

#Get website data
data = json.loads(requests.get(website).text)

abilities = data["abilitydata"]
heroes = data["herodata"]

for hero in heroes:	
	heroes.get(hero)["abilities"] = {}

for ability in abilities:
	#strip html
	for key in abilities.get(ability):
		abilities.get(ability)[key] = striphtml(abilities.get(ability).get(key))

	for m in re.finditer(r"_", ability):
		if(ability[:m.start()] in heroes):
			tmp_index = m.start()
			hero = ability[:tmp_index]
			break

	heroes.get(hero)["abilities"][ability[tmp_index+1:]] = (abilities.get(ability))

with open("heroes.json", 'w') as f:
    json_data = json.dumps(heroes, sort_keys=True, indent=4, separators=(',', ': '))
    f.write(json_data)