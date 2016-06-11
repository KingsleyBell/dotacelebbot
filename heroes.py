from bs4 import BeautifulSoup

import requests

r  = requests.get("http://dota2.gamepedia.com/Heroes")

data = r.text

soup = BeautifulSoup(data, "html.parser")

data = soup.find_all(attrs={"class": "channelListEntry"})

namesList = []

for div in data:
    links = div.findAll('a')
    for a in links:
        namesList.append(a.get('href').replace("_", " ")[1:].title())

with open("celebs.txt", 'wb') as f:
	f.write(bytes("\n".join(namesList), 'UTF-8'))