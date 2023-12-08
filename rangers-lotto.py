"""Module docstring for rangers-lotto.py.

Script: rangers-lotto.py
Author: Craig R Morton
Date: 6th December 2023
Description: Scrape the RYDC website, grab the latest Rangers Lotto numbers and post them to Twitter.
"""

import os
import re
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
import tweepy

URL = "https://www.rydc.co.uk/?page_id=82"

api_key = os.environ.get("TWITTER_API_KEY")
api_secret_key = os.environ.get("TWITTER_API_SECRET_KEY")
access_token = os.environ.get("TWITTER_ACCESS_TOKEN")
access_token_secret = os.environ.get("TWITTER_ACCESS_TOKEN_SECRET")


def post_to_twitter(message):
    """
    Post a tweet to Twitter with the lottery numbers scraped from the website.
    Args:
        message (str): The message to be posted.
    Returns:
        None
    """
    # Authenticate to Twitter
    client = tweepy.Client(
        consumer_key=api_key,
        consumer_secret=api_secret_key,
        access_token=access_token,
        access_token_secret=access_token_secret
    )

    # Post Tweet
    client.create_tweet(text=message)
    print("Tweet sent!")


def get_first_week_lottery_results(url):
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

    # Find all images within the entry content
    ball_images = results_element.find_all("img")
    date_pattern = re.compile(r'\b(\w{3} \d{1,2}(?:st|nd|rd|th) \w+ \d{4})\b')
    matches = list(date_pattern.finditer(results_element.get_text()))
    # print(matches)
    date_values = [match.group(0) for match in matches]
    # print(date_values)
    if not ball_images:
        print("No lottery ball images found for the specified week.")

    # Extract and print the lottery ball numbers
    ball_numbers = [image['src'].split('/')[-1].split('.')[0] for image in ball_images]

    result_dict = {}
    # Iterate over the dates and assign the first 5 elements of numbers to each date
    for date, number_list in zip(date_values,
                                 [ball_numbers[i:i + 5] for i in range(0, len(ball_numbers), 5)]):
        result_dict[date] = number_list

    twitter_message = 'Rangers Lotto Results 🔴⚪🔵\n'
    for date, number_list in result_dict.items():
        formatted_numbers = [f"Bonus: {num[5:]}" if num.startswith("bonus") else num for num in
                             number_list]
        twitter_message += f"{date}\n"
        twitter_message += f"{', '.join(formatted_numbers)}"

    print(twitter_message)

    try:
        post_to_twitter(twitter_message)
    except requests.exceptions.RequestException as requests_exception:
        print(f"There was a problem posting to Twitter - {requests_exception}")


def extract_lottery_numbers(ball_images, date_values):
    """
    Extract lottery ball numbers and organize them into a dictionary.

    Args:
        ball_images (list): List of BeautifulSoup tag objects representing lottery ball images.
        date_values (list): List of dates.

    Returns:
        dict: A dictionary where each date is associated with a list of lottery ball numbers.
    """
    # Extract and print the lottery ball numbers
    ball_numbers = [image['src'].split('/')[-1].split('.')[0] for image in ball_images]

    result_dict = {}
    # Iterate over the dates and assign the first 5 elements of numbers to each date
    for date, number_list in zip(date_values, [ball_numbers[i:i + 5] for i in range(0, len(ball_numbers), 5)]):
        result_dict[date] = number_list

    return result_dict


# Call the function to get and parse lottery results for the first "Week" link
try:
    get_first_week_lottery_results(URL)
except requests.exceptions.RequestException as requests_exception:
    print(f"There was a problem with one of the requests - {requests_exception}")
except Exception as e:
    print(f"Exception thrown when getting Rangers Lotto numbers - {e}")
