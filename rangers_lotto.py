"""
Script: rangers_lotto.py
Author: Craig R Morton
Date: 6th December 2023
Description: Scrape the RYDC website, grab the latest Rangers Lotto numbers and post them to Twitter and Telegram.
"""

import os
import re
import sys
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
import tweepy
from typing import Dict, List, Optional, Union

RYDC_URL = "https://www.rydc.co.uk/?page_id=82"

# Twitter config
twitter_api_key = os.environ.get("TWITTER_API_KEY")
twitter_api_secret_key = os.environ.get("TWITTER_API_SECRET_KEY")
twitter_access_token = os.environ.get("TWITTER_ACCESS_TOKEN")
twitter_access_token_secret = os.environ.get("TWITTER_ACCESS_TOKEN_SECRET")

# Telegram config
telegram_bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
telegram_user_id = os.environ.get("TELEGRAM_USER_ID")
TELEGRAM_CHANNEL_ID = '@GlasgowRangersUpdates'

if any(env_var is None for env_var in
       [twitter_api_key, twitter_api_secret_key, twitter_access_token, twitter_access_token_secret]):
    print("Some environment variables are not set. All 4 environment variables must be configured to post to Twitter.")
    sys.exit(1)

if len(sys.argv) != 5:
    print("You need to provide 4 individual lottery numbers")
    print("Usage: python rangers_lotto.py 5 9 16 18")
    sys.exit(1)

selected_balls = {
    'ball1': int(sys.argv[1]),
    'ball2': int(sys.argv[2]),
    'ball3': int(sys.argv[3]),
    'ball4': int(sys.argv[4]),
}


def post_to_telegram(message: str, channel_id: Optional[str] = TELEGRAM_CHANNEL_ID) -> None:
    """
    Post a message to the 'Glasgow Rangers Updates' Telegram channel
    Args:
         message (str): The message to be posted
         channel_id (str): The Telegram channel ID (default is TELEGRAM_CHANNEL_ID)
    Returns:
        None
    """
    # call the Telegram API synchronously, async calls aren't strictly needed here
    url = f"https://api.telegram.org/bot{telegram_bot_token}/sendMessage"
    params = {
        'chat_id': channel_id,
        'text': message
    }
    response = requests.post(url, params=params, timeout=30)
    if response.status_code == 200:
        print(f"Posted to Telegram, Channel ID {channel_id}")
    else:
        print(f"Failed to post to Telegram, Channel ID {channel_id}. Status code: {response.status_code}")


def post_to_twitter(message: str) -> None:
    """
    Post a tweet to Twitter with the lottery numbers scraped from the website.
    Args:
        message (str): The message to be posted.
    Returns:
        None
    """
    # Authenticate to Twitter
    client = tweepy.Client(
        consumer_key=twitter_api_key,
        consumer_secret=twitter_api_secret_key,
        access_token=twitter_access_token,
        access_token_secret=twitter_access_token_secret
    )

    # Post Tweet
    client.create_tweet(text=message)
    print("Tweet sent!")


def get_first_week_lottery_results(url: str) -> None:
    """
    Do a GET request to the RYDC website to get the latest Rangers Lotto numbers
    Args:
        url (str): The URL of the RYDC website
    Returns:
        None
    """
    # Send a GET request to the URL
    response = requests.get(url, timeout=30)
    print(f"Getting results from {url}")

    # Check if the request was successful (status code 200)
    if response.status_code != 200:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        return

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")

    # Find the first link with "Week" in its text content
    week_link = soup.find("a", string=lambda text: text and "week" in text.lower())

    if not week_link:
        print("No link with 'Week' found.")
        return

    # Extract the href attribute to get the link
    week_link_url = week_link.get("href")

    # Construct the absolute URL if it's a relative link
    week_link_url = urljoin(url, week_link_url)

    # Send a GET request to the linked page
    week_response = requests.get(week_link_url, timeout=30)

    if week_response.status_code != 200:
        print(f"Failed to retrieve the linked page. Status code: {week_response.status_code}")
        return

    # Parse the HTML content of the linked page
    week_soup = BeautifulSoup(week_response.content, "html.parser")

    results_element = week_soup.find("div", class_="entry-content")

    if not results_element:
        print("No entry content found on the linked page.")

    result_dict = get_numbers(results_element)

    check_results(result_dict)

    twitter_message = build_twitter_message(result_dict)
    print(twitter_message)

    try:
        post_to_twitter(twitter_message)
        post_to_telegram(twitter_message)
    except requests.exceptions.RequestException as requests_exception:
        print(f"There was a problem posting to Twitter/Telegram - {requests_exception}")


def check_results(results: Dict[str, List[Union[int, str]]]) -> None:
    """
    Check the results and post to the user if they have hit the jackpot!
    :param results: Dictionary of dates to results
    :return: None
    """
    for date, number_list in results.items():
        # check the first four numbers only and use a list comprehension to convert them to integers
        number_list_int = [int(num) for num in number_list[:4]]
        if number_list_int == list(selected_balls.values()):
            # jackpot!
            post_to_telegram(f'You have won the Rangers Lotto jackpot for {date}! Contact rydc.co.uk', telegram_user_id)

        # TODO: find out what sequence or other matches result in a win  # pylint: disable=W0511


def get_numbers(results_element: str) -> Dict[str, List[Union[int, str]]]:
    """
    Get the numbers from the page
    :param results_element: The markup
    :return: A dictionary of results
    """
    # Find all images within the entry content
    ball_images = results_element.find_all("img")
    date_pattern = re.compile(r'\b(\w{3} \d{1,2}(?:st|nd|rd|th) \w+ \d{4})\b')
    matches = list(date_pattern.finditer(results_element.get_text()))
    # print(matches)
    date_values = [match.group(0) for match in matches]
    if not ball_images:
        print("No lottery ball images found for the specified week.")

    # Extract and print the lottery ball numbers
    ball_numbers = [image['src'].split('/')[-1].split('.')[0] for image in ball_images]

    result_dict = {}
    # Iterate over the dates and assign the first 5 elements of numbers to each date
    for date, number_list in zip(date_values,
                                 [ball_numbers[i:i + 5] for i in range(0, len(ball_numbers), 5)]):
        result_dict[date] = number_list

    return result_dict


def build_twitter_message(result_dict: Dict[str, List[Union[int, str]]]) -> str:
    """
    Build a formatted Twitter message for the Rangers Lotto Results.

    Parameters:
    - result_dict (dict):
    A dictionary containing lotto results where keys are dates and values are lists of numbers.

    Returns:
    - str: The formatted Twitter message.
    """
    twitter_message = 'Rangers Lotto Results 🔴⚪🔵\n'

    for date, number_list in result_dict.items():
        formatted_numbers = [f"Bonus: {num[5:]}\n" if num.startswith("bonus") else num for num in number_list]
        twitter_message += f"{date}\n"
        twitter_message += f"{', '.join(formatted_numbers)}"

    return twitter_message


if __name__ == "__main__":
    # Call the function to get and parse lottery results for the first "Week" link
    try:
        get_first_week_lottery_results(RYDC_URL)
    except requests.exceptions.RequestException as exception:
        print(f"There was a problem with one of the requests - {exception}")
    except Exception as e:  # pylint: disable=broad-except
        print(f"Exception thrown when getting Rangers Lotto numbers - {e}")
