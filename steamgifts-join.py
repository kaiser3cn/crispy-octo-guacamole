#!/usr/bin/env python
# Lara Maia <dev@lara.click> 2015

from bs4 import BeautifulSoup as bs
import requests
import stconfig
import os, sys
from signal import signal, SIGINT

from stnetwork import tryConnect

config = stconfig.init(os.path.splitext(sys.argv[0])[0]+'.config')

try:
    cookie = {'PHPSESSID': config.get('CONFIG', 'Cookie')}
except(configparser.NoOptionError, configparser.NoSectionError):
    print("Incorrect data. Please, check your config file.", file=sys.stderr)
    exit(1)

def signal_handler(signal, frame):
    print("Exiting...")
    exit(0)

if __name__ == "__main__":
    signal(SIGINT, signal_handler)

    data = {}

    url = 'http://www.steamgifts.com/giveaways/search?type=wishlist'

    print("Connecting to the server")
    page = tryConnect(url, cookies=cookie).content

    try:
        giveawayList = []
        container = bs(page, 'html.parser').find('div', class_='widget-container')
        for div in container.findAll('div', class_=None):
            if div.find('div', class_='giveaway__row-outer-wrap'):
                giveawayList.append(div)

        for giveaway in giveawayList[1].findAll('div', class_='giveaway__row-outer-wrap'):
            gameName = giveaway.find('a', class_='giveaway__heading__name').text
            gameURL = giveaway.find('a', class_='giveaway__heading__name')['href']
            gamePoints = giveaway.find('span', class_='giveaway__heading__thin').text

            try:
                gameLevel = giveaway.find('div', class_='giveaway__column--contributor-level').text
            except AttributeError:
                gameLevel = "Level 0+"

            if giveaway.find('div', class_='giveaway__column--contributor-level--negative'):
                gameCanEnter = "CanEnter: No"
            else:
                gameCanEnter = "CanEnter: Yes"

            ### STUB ###
            print(gameName)
            print(gameURL)
            print(gamePoints)
            print(gameLevel)
            print(gameCanEnter)

            print('\n')

        print(' *** Hey, don\'t use this yet! ***\n\n')
        ### STUB ###

    except Exception as e:
        print(e, file=sys.stderr)
