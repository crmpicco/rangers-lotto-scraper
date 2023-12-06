![Rangers Lotto](https://i.imgur.com/z2hrTgT.png)

# Rangers Lotto Results Scraper
Scrape the latest results from the Rangers Lotto site

[![python](https://img.shields.io/badge/Python-3.9-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)

## Crontab
Add it to the crontab to run twice a week, for example
```commandline
# Post the Rangers Lotto results to Twitter twice per week
15 17 * * 1,4 source /opt/virtualenv/rangers-lotto/bin/activate && /opt/virtualenv/rangers-lotto/bin/python3 /path/to/script/rangers-lotto-scraper/rangers-lotto.py > /var/log/rangers-lotto-scraper.log 2>&1
```
