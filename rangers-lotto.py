#!/usr/bin/python

# Author: Craig R Morton <crmpicco@aol.com>

import boto3
from bs4 import BeautifulSoup
import json
import os
import requests
import re
from pprint import pprint

# @TODO pull from environment variables, e.g os.getenv('TELEGRAM_CRMPICCO'), os.environ['TELEGRAM_APIKEY']
telegram = TelegramBot()
telegram_recipient = 1872

# @TODO change this URL to the latest results page
page = requests.get("http://www.rangerslotto.co.uk/?page_id=82&lottoId=27")

soup = BeautifulSoup(page.content, 'html.parser')

balls = []
for entry_content in soup.find_all('img',vspace='12'):
    balls.append(entry_content['src'].rsplit('/', 1)[-1].split('.')[0])

winning_numbers = ' ' . join(balls)
print 'The winning numbers were ' + winning_numbers

# @TODO compare with my numbers

# @TODO Send to Telegram