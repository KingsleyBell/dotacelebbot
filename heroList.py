import requests
import json

#Website to scrape top 100 celebrities from
website = "http://www.dota2.com/jsfeed/heropediadata?feeds=abilitydata,herodata&v=3487285YS81IGG3JCd6&l=english"

#Get website data
data = json.loads(requests.get(website).text)

abilities = data["abilitydata"]
heroes = data["herodata"]

for ability in abilities:
	hero = ability

with open("heroes.txt", 'w') as f:
    json_data = json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))
    f.write(json_data)