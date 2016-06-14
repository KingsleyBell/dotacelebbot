#Get dota celebrity data from reddit.com

from bs4 import BeautifulSoup
import json
import re
import requests

#Website to scrape top 100 celebrities from
website = "https://www.reddit.com/r/DotA2/wiki/twitter"

#Get website data
data = requests.get(website).text

#Parse data using bs4
soup = BeautifulSoup(data, "html.parser")

#List of top dota celebs
tag_data = soup.find_all(['strong', 'h1', 'h2', 'p'])
celebs = {}

type = ""

for element in tag_data: 

    #Subsections              
    if (element.name == 'strong'):        
        if (element.string == "Subreddit Mods"):
            type = 1
        elif (element.string == "Casters & Personalities"):
            type = 2
        elif (element.string == "Studios, Services, Tools, Webs & such"):
            type = 3
        elif (element.string == "Video Makers"):
            type = 4
        elif (element.string == "Tournaments & eSports people"):
            type = 5
        elif (element.string == "Icefrog & Icefrog impersonators"):
            type = 6
        elif (element.string == "Valve official accounts"):
            type = 7
        elif (element.string == "Teams & Players"):
            type = 8


    


#with open("celebs.json", 'w') as f:
#    json_data = json.dumps(celebs, sort_keys=True, indent=4, separators=(',', ': '))
#    f.write(json_data)


