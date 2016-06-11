#Get celebrity data from posh24.com

from bs4 import BeautifulSoup
import json
import re
import requests

#Website to scrape top 100 celebrities from
website = "http://www.posh24.com/celebrities"

#Get website data
data = requests.get(website).text

#Parse data using bs4
soup = BeautifulSoup(data, "html.parser")

#List of top 100 celebs
data = soup.find_all(attrs={"class": "channelListEntry"})
celebs = {}

i = 1
for div in data:
    links = div.findAll('a')
    for a in links:
        
        #Celeb object
        celeb = {}

        raw_name = a.get('href')
        celeb_name = raw_name.replace("_", " ")[1:].title()

        celeb['name'] = celeb_name    

        #Celeb page
        nameWebsite = website[:website.rfind('/')] + raw_name        
        nameData = requests.get(nameWebsite).text

        #Parse celeb page
        nameSoup = BeautifulSoup(nameData, 'html.parser')

        #Celeb info        
        attrs = nameSoup.find_all(attrs={"class": "attributeContent"})

        #Celeb bio
        bio = nameSoup.find(attrs={"class": "info"}).contents[0]
        if (" he " in bio or " him " in bio):
            celeb['gender'] = "m"
        elif (" she " in bio or " her " in bio):
            celeb['gender'] = "f"
        else:
            celeb['gender'] = "unknown"

        if (len(attrs) != 0):            

            birthInfo = re.sub('\s+',' ',attrs[0].contents[0])
        

            if ("in" in birthInfo):
        	    birthInfo = birthInfo.split("in")        
        	    celebBD = birthInfo[0]
        	    celebPlace = birthInfo[1]
        	    celebAge = re.sub('\s+',' ',attrs[1].contents[0])

            else:
            	celebBD = "unknown"
            	celebPlace = birthInfo
            	celebAge = "unknown"

            #print(celebBD, celebPlace, celebAge)            

            celeb['birth'] = celebBD
            celeb['birth-place'] = celebPlace
            celeb['age'] = celebAge

        else:
            celeb['birth'] = "unknown"
            celeb['birth-place'] = "unknown"
            celeb['age'] = "unknown"

        celeb['rank'] = i
        i = i+1

        #Add celeb to celeb list
        celebs[celeb_name] = (celeb)        


with open("celebs.json", 'w') as f:
    json_data = json.dumps(celebs, sort_keys=True, indent=4, separators=(',', ': '))
    f.write(json_data)


