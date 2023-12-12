![Rangers Lotto](https://i.imgur.com/SkxOHiF.png)

# Rangers Lotto Results Scraper
Scrape the latest results from the [Rangers Lotto site](https://www.rydc.co.uk)

[![python](https://img.shields.io/badge/Python-3.9-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org) ![Build Status](https://github.com/crmpicco/rangers-lotto-scraper/actions/workflows/pylint.yml/badge.svg)

## Crontab
Add it to the crontab to run twice a week, for example
```commandline
# Post the Rangers Lotto results to Twitter twice per week
09 09 * * 1,4 . $HOME/.zshrc; source /opt/virtualenv/rangers-lotto/bin/activate && /opt/virtualenv/rangers-lotto/bin/python3 /Users/craigrmorton/rangers-lotto-scraper/rangers_lotto.py > /var/log/rangers-lotto-scraper.log 2>&1
```
