#Get dota celebrity data from reddit.com

from bs4 import BeautifulSoup
import json
import re
import requests

def addCeleb(celeb, type):

    if(type == 0):
        return 0

    jsonCeleb = {}

    if (celeb[0] != '@'):
        celeb = '@' + celeb

    jsonCeleb['name'] = celeb
    jsonCeleb['type'] = typeDict[type]

    return jsonCeleb



#Website to scrape top 100 celebrities from
website = "https://www.reddit.com/r/DotA2/wiki/twitter"

#Get website data
data = requests.get(website).text

#Parse data using bs4
soup = BeautifulSoup(data, "html.parser")

#List of top dota celebs
tag_data = soup.find_all(['strong', 'h2', 'p'])
celebs = {}

type = 0
typeDict = {1:'mod', 2:'caster', 3:'studio', 4:'video', 5:'tournament', 6:'icefrog', 7:'valve', 8:'teams'}

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
    elif (element.name == 'p' or element.name == 'h2'):
        pSoup = BeautifulSoup(str(element), 'html.parser')
        for a in pSoup.find_all('a', rel=True):
            if('nofollow' in a['rel']):                
                link = a['href']
                if ('twitter' in link):
                    if(link[-1] != '/'):
                        celeb = (link[link.rfind("/")+1:])
                        jsonCeleb = addCeleb(celeb, type)
                        if (jsonCeleb):
                            celebs[jsonCeleb['name']] = jsonCeleb
                    else:
                        link = link[:-1]
                        celeb =  (link[link.rfind("/")+1:])
                        jsonCeleb = addCeleb(celeb, type)
                        if (jsonCeleb):
                            celebs[jsonCeleb['name']] = jsonCeleb   


with open("dotaCelebs.json", 'w') as f:
    json_data = json.dumps(celebs, sort_keys=True, indent=4, separators=(',', ': '))
    f.write(json_data)


