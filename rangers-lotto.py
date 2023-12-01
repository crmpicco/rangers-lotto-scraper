import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re

url = "https://www.rydc.co.uk/?page_id=82"

def get_first_week_lottery_results(url):
    # Send a GET request to the URL
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, "html.parser")

        # Find the first link with "Week" in its text content
        week_link = soup.find("a", string=lambda text: text and "week" in text.lower())

        print(week_link)

        if week_link:
            # Extract the href attribute to get the link
            week_link_url = week_link.get("href")

            # Construct the absolute URL if it's a relative link
            week_link_url = urljoin(url, week_link_url)

            # Send a GET request to the linked page
            week_response = requests.get(week_link_url)

            print(week_response)

            if week_response.status_code == 200:
                # Parse the HTML content of the linked page
                week_soup = BeautifulSoup(week_response.content, "html.parser")

                results_element = week_soup.find("div", class_="entry-content")

                if results_element:
                    # Find all images within the entry content
                    ball_images = results_element.find_all("img")
                    date_pattern = re.compile(r'\b(\w{3} \d{1,2}(?:st|nd|rd|th) \w+ \d{4})\b')
                    matches = list(date_pattern.finditer(results_element.get_text()))

                    if ball_images:
                        # Extract and print the lottery ball numbers
                        ball_numbers = [image['src'].split('/')[-1].split('.')[0] for image in ball_images]
                        print("Lottery Results:", ", ".join(ball_numbers))
                    else:
                        print("No lottery ball images found for the specified week.")
                else:
                    print("No entry content found on the linked page.")
            else:
                print(f"Failed to retrieve the linked page. Status code: {week_response.status_code}")
        else:
            print("No link with 'Week' found.")
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")

# Call the function to get and parse lottery results for the first "Week" link
get_first_week_lottery_results(url)
