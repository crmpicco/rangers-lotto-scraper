# Author: Craig R Morton <crmpicco@aol.com>
from bs4 import BeautifulSoup
import requests
import re

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