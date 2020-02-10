#!/usr/bin/python

# Author: Craig R Morton <crmpicco@aol.com>

import boto3
from bs4 import BeautifulSoup
from twx.botapi import TelegramBot
import json
import os
import requests
import re
from pprint import pprint

telegram = TelegramBot(os.environ['TELEGRAM_API_KEY'])
telegram_recipient = os.getenv('TELEGRAM_CRMPICCO')

base_uri = 'http://www.rangerslotto.co.uk'

page = requests.get(base_uri + "/?page_id=82")

soup = BeautifulSoup(page.content, 'html.parser')

special_divs = soup.find_all('div',{'class':'entry-content'})
for text in special_divs:
    download = text.find_all('a', href = re.compile('\page_id=82'))
    for text in download:
        hrefText = (text['href'])
        print hrefText
        break

print 'The Latest Results URL is ' + base_uri + hrefText

#
# balls = []
# for entry_content in soup.find_all('img',vspace='12'):
#
#     ball_number = str(entry_content['src'].rsplit('/', 1)[-1].split('.')[0])
#
#     if not ball_number.startswith('bonus'):
#         balls.append(int(entry_content['src'].rsplit('/', 1)[-1].split('.')[0]))
#     else:
#         bonus_ball = ball_number
#
# print balls
#
# winning_numbers = ' ' . join(str(v) for v in balls)
# print 'The winning numbers were ' + winning_numbers
#
# # # @TODO compare with my numbers - 18, 19, 44, 49
# my_lotto_numbers = [18, 19, 44, 49]
#
# matching_numbers = len(set(my_lotto_numbers) & set(balls))
#
# print 'You matched ' . matching_numbers . ' numbers this week'
#
# print 'The bonus ball was ' + bonus_ball.replace('bonus', '')

# @TODO Send to Telegram
