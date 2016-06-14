#Get dota text from soundboard.com

from bs4 import BeautifulSoup
import json
import re
import requests

#Website to scrape dota text from
website = "http://www.soundboard.com/sb/howboutthis"

#Get website data
data = requests.get(website).text

#Parse data using bs4
soup = BeautifulSoup(data, "html.parser")

#List of dota text
dataList = soup.find("div", {"ul": "playlist"})


texts = []

for i in range(25):
	text = soup.find("a", {"id": "track_" + str(i)}).find("span").contents[0]
	texts.append(text)

with open("dotaTexts", 'w') as f:
    for text in texts:
    	f.write(text + "\n")