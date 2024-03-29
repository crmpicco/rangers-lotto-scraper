![Rangers Lotto](https://i.imgur.com/SkxOHiF.png)

# Rangers Lotto Results Scraper
Scrape the latest results from the [Rangers Lotto site](https://www.rydc.co.uk) following the draw of the lottery numbers and post them to Twitter and Telegram.

![Build Status](https://github.com/crmpicco/rangers-lotto-scraper/actions/workflows/pylint.yml/badge.svg)
![Build Status](https://github.com/crmpicco/rangers-lotto-scraper/actions/workflows/bandit.yml/badge.svg)
[![Python Versions](https://img.shields.io/badge/Python-3.8%2C%203.9%2C%203.10%2C%203.11%2C%203.12-blue?style=flat&logo=python&logoColor=white)](https://www.python.org/)

## Social
[![Twitter URL](https://img.shields.io/twitter/url/https/twitter.com/RangersLottoBot.svg?style=social&label=Follow%20%40RangersLottoBot)](https://twitter.com/RangersLottoBot)
[![Telegram](https://img.shields.io/badge/-telegram-red?color=white&logo=telegram&logoColor=black)](https://t.me/GlasgowRangersUpdates)

## Setup

### Virtual Environment
```shell
# Create a virtual environment named "rangers-lotto"
python3 -m venv /opt/virtualenv/rangers-lotto
# Activate the virtual environment
source /opt/virtualenv/rangers-lotto/bin/activate
# Install project dependencies
pip install -r requirements.txt
```

### Environment variables
```shell
# RangersLottoBot Twitter API keys
export TWITTER_API_KEY="your_twitter_api_key"
export TWITTER_API_SECRET_KEY="your_twitter_api_secret_key"
export TWITTER_ACCESS_TOKEN="your_twitter_access_token"
export TWITTER_ACCESS_TOKEN_SECRET="your_twitter_access_token_secret"

# RangersLottoBot Telegram Bot Key
export TELEGRAM_BOT_TOKEN="your_telegram_bot_token"
# Your UserID in Telegram (use GetIDs Bot)
export TELEGRAM_USER_ID="187219972021"
```

## Crontab
Add it to the crontab to run twice a week, for example. Pass in your numbers (e.g. `1 6 9 55`) to check if you have hit the jackpot! 💰
```commandline
# Post the Rangers Lotto results to Twitter and Telegram twice per week
09 09 * * 1,4 . $HOME/.zshrc; source /opt/virtualenv/rangers-lotto/bin/activate && /opt/virtualenv/rangers-lotto/bin/python3 /Users/crmpicco/rangers-lotto-scraper/rangers_lotto.py 1 6 9 55 > /var/log/rangers-lotto-scraper.log 2>&1
```
