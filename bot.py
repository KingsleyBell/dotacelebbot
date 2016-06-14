# Copyright (c) 2015–2016 Molly White
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# Run script with python3 using args:
#   Follow, to follow list of dotacelebs found in json file
#   Tweet, to tweet randomly selected hero spell on randomly selected dota celeb 

import os
import sys
import tweepy
from secrets import *
from time import gmtime, strftime
import json
import random

from secrets import *

auth = tweepy.OAuthHandler(C_KEY, C_SECRET)  
auth.set_access_token(A_TOKEN, A_TOKEN_SECRET)  
api = tweepy.API(auth)


# ====== Individual bot configuration ==========================
bot_username = 'dotaceleb'
logfile_name = bot_username + ".log"

# ==============================================================


def create_tweet():
    """Create the text of the tweet you want to send."""

    #list of exclamations
    exclamations = ["Yay!", "Oh no!"]

    #open celeb and dota files
    with open('dotaCelebs.json') as celebs_file:    
        celebs = json.load(celebs_file)
    with open('heroes.json') as heroes_file:    
        heroes = json.load(heroes_file)

    #choose random celeb and hero and spell
    celeb = random.choice(list(celebs.keys()))
    hero = random.choice(list(heroes.keys()))

    spellFlag = False
    i = 0
    while (not spellFlag):
        spell = random.choice(list(heroes[hero]["abilities"].keys()))
        #Make sure no passive or non target or creep spells are chosen 
        if("No Target" not in heroes[hero]["abilities"][spell]["affects"] and "Passive" not in heroes[hero]["abilities"][spell]["affects"] and "Allies" not in heroes[hero]["abilities"][spell]["affects"]):
            spellFlag = True
        else:
            i = i+1
            if (i > 10):
                hero = random.choice(list(heroes.keys()))

    if("Unit Target" in heroes[hero]["abilities"][spell]["affects"]):
        spellType = "unit"
    elif("Point Target" in heroes[hero]["abilities"][spell]["affects"]):
        spellType = "area"

    if("Enemy Units" in heroes[hero]["abilities"][spell]["affects"]):
        affects = "enemies"
    elif("Allied Heroes" in heroes[hero]["abilities"][spell]["affects"]):
        affects = "allies"

    hero = hero.replace("_", " ").title()
    spell = spell.replace("_", " ").title()
   
    text = hero + " " + spell + "s " + celeb
    return text


def tweet(text):
    """Send out the text as a tweet."""
    # Twitter authentication
    auth = tweepy.OAuthHandler(C_KEY, C_SECRET)
    auth.set_access_token(A_TOKEN, A_TOKEN_SECRET)
    api = tweepy.API(auth)

    # Send the tweet and log success or failure
    try:
        api.update_status(text)
    except tweepy.error.TweepError as e:
        log("Can't tweet \"" + text + "\"\nError: " str(e))
    else:
        log("Tweeted: " + text)

def followCelebs():
    """Follow all the dota celebs """
    # Twitter authentication
    auth = tweepy.OAuthHandler(C_KEY, C_SECRET)
    auth.set_access_token(A_TOKEN, A_TOKEN_SECRET)
    api = tweepy.API(auth)

    with open('dotaCelebs.json') as celebs_file:    
        celebs = list(json.load(celebs_file).keys())
        for celeb in celebs:
            try:
                api.create_friendship(celeb)
            except tweepy.error.TweepError as e:
                log("cant follow " + celeb + "\nError: " + str(e))
            else:
                log("followed: " + celeb) 



def log(message):
    """Log message to logfile."""
    path = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    with open(os.path.join(path, logfile_name), 'a+') as f:
        t = strftime("%d %b %Y %H:%M:%S", gmtime())
        f.write("\n" + t + " " + message)


if __name__ == "__main__":
    if (sys.argv[1] == 'tweet'):
        tweet_text = create_tweet()   
        tweet(tweet_text)
        print(tweet_text)
    elif (sys.argv[1] == 'follow'):
        followCelebs()
    else:
        print(sys.argv[1])
