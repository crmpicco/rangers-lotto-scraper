import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import tweepy

url = "https://www.rydc.co.uk/?page_id=82"


def post_to_twitter(message):
    # auth = tweepy.OAuthHandler(api_key, api_secret_key)
    # auth.set_access_token(access_token, access_token_secret)
    # # api = tweepy.API(auth)
    # api = tweepy.API(auth, wait_on_rate_limit=True)
    #
    # api.update_status(status=message)

    # Authenticate to Twitter
    client = tweepy.Client(
        consumer_key=api_key,
        consumer_secret=api_secret_key,
        access_token=access_token,
        access_token_secret=access_token_secret
    )

    # Post Tweet
    message = " MESSAGE "
    client.create_tweet(text=message)
    print("Tweeted!")


    print("Tweet sent!")


def get_first_week_lottery_results(url):
    # Send a GET request to the URL
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code != 200:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        return

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")

    # Find the first link with "Week" in its text content
    week_link = soup.find("a", string=lambda text: text and "week" in text.lower())

    if week_link:
        # Extract the href attribute to get the link
        week_link_url = week_link.get("href")

        # Construct the absolute URL if it's a relative link
        week_link_url = urljoin(url, week_link_url)

        # Send a GET request to the linked page
        week_response = requests.get(week_link_url)

        if week_response.status_code == 200:
            # Parse the HTML content of the linked page
            week_soup = BeautifulSoup(week_response.content, "html.parser")

            results_element = week_soup.find("div", class_="entry-content")

            if results_element:
                # Find all images within the entry content
                ball_images = results_element.find_all("img")
                date_pattern = re.compile(r'\b(\w{3} \d{1,2}(?:st|nd|rd|th) \w+ \d{4})\b')
                matches = list(date_pattern.finditer(results_element.get_text()))
                # print(matches)
                date_values = [match.group(0) for match in matches]
                # print(date_values)
                if ball_images:
                    # Extract and print the lottery ball numbers
                    ball_numbers = [image['src'].split('/')[-1].split('.')[0] for image in ball_images]
                    # print(ball_numbers)
                    # print("Lottery Results:", ", ".join(ball_numbers))

                    result_dict = {}
                    # Iterate over the dates and assign the first 5 elements of numbers to each date
                    for date, number_list in zip(date_values,
                                                 [ball_numbers[i:i + 5] for i in range(0, len(ball_numbers), 5)]):
                        result_dict[date] = number_list

                    twitter_message = ''
                    for date, number_list in result_dict.items():
                        twitter_message += f"{date} = {', '.join(number_list)}"
                        print(twitter_message)
                        try:
                            post_to_twitter(twitter_message)
                        except Exception as e:
                            print(f"There was a problem posting to Twitter - {e}")

                else:
                    print("No lottery ball images found for the specified week.")
            else:
                print("No entry content found on the linked page.")
        else:
            print(f"Failed to retrieve the linked page. Status code: {week_response.status_code}")
    else:
        print("No link with 'Week' found.")


# Call the function to get and parse lottery results for the first "Week" link
get_first_week_lottery_results(url)
