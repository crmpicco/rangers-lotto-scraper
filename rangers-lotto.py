import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

url = "https://www.rydc.co.uk/?page_id=82"

def get_first_week_lottery_results(url):
    # Send a GET request to the URL
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, "html.parser")

        # Find the first link with "Week" in its text content
        week_link = soup.find("a", string=lambda text: text and "Week" in text)

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

                # Find the element containing the results (adjust as needed)
                results_element = week_soup.find("div", class_="result")

                if results_element:
                    # Extract and print the text content of the element
                    results = results_element.find_next("ul")  # Assuming the results are in an unordered list (adjust as needed)
                    if results:
                        for li in results.find_all("li"):
                            print(li.get_text(strip=True))
                    else:
                        print("No results found for the specified week.")
                else:
                    print("No results element found on the linked page.")
            else:
                print(f"Failed to retrieve the linked page. Status code: {week_response.status_code}")
        else:
            print("No link with 'Week' found.")
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")

# Call the function to get and parse lottery results for the first "Week" link
get_first_week_lottery_results(url)
