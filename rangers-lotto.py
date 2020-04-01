#!/usr/bin/python

__author__ = "Craig R Morton"
__copyright__ = "Copyright 2020, Craig R Morton"
__email__ = "crmpicco@aol.com"
__version__ = "0.1"
__maintainer__ = "Craig R Morton"

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
hrefText = ''
for text in special_divs:
    download = text.find_all('a', href = re.compile('\page_id=82'))
    for text in download:
        hrefText = (text['href'])
        print hrefText
        break

latest_results_uri = base_uri + hrefText
print 'The Latest Results URL is ' + latest_results_uri

# @TODO temp
latest_results_uri = "http://www.rangerslotto.co.uk/?page_id=82&lottoId=33"

latest_results_page = requests.get(latest_results_uri)
latest_results_soup = BeautifulSoup(latest_results_page.content, 'html.parser')

balls = {}
balls_count = 0

for entry_content in latest_results_soup.find_all('img',vspace='12'):

    if balls_count < 5:
        draw_day = 'sat'
    else:
        draw_day = 'wed'

    ball_number = str(entry_content['src'].rsplit('/', 1)[-1].split('.')[0])

    if not ball_number.startswith('bonus'):
        balls[draw_day].append(int(entry_content['src'].rsplit('/', 1)[-1].split('.')[0]))
    else:
        bonus_ball = ball_number
    balls_count += 1

print balls
print balls_count

winning_numbers = ' ' . join(str(v) for v in balls)
print 'The winning numbers were ' + winning_numbers
#
# # # @TODO compare with my numbers - 18, 19, 44, 49
my_lotto_numbers = [18, 19, 44, 49]

matching_numbers = len(set(my_lotto_numbers) & set(balls))

print 'You matched ' + str(matching_numbers) + ' numbers this week'

print 'The bonus ball was ' + bonus_ball.replace('bonus', '')

my_lotto_numbers_formatted = ' '.join(str(v) for v in my_lotto_numbers)

telegram_message = ("[Rangers Lotto Results](%s)\n"
                    "Winning Numbers: %s\n"
                    "Your Numbers: %s\n"
                    "You matched %s numbers this week\n"
                    % ( latest_results_uri, winning_numbers, my_lotto_numbers_formatted, matching_numbers ))

# result = telegram.send_message(telegram_recipient, telegram_message, parse_mode="Markdown").wait()
# print result