import requests
from bs4 import BeautifulSoup
import os

# Base URL and the path to match after 'https://help.blackboard.com'
base_url = "https://help.blackboard.com/Learn/Student/Ultra/About_You"
url_prefix = "/Learn/Student/Ultra/"

# Send a GET request to the main page
response = requests.get(base_url)
soup = BeautifulSoup(response.content, "html.parser")

# Find all divs with class 'field-content'
divs = soup.find_all("div", class_="field-content")

# Loop through each div to find <a> tag and scrape the href that matches the desired prefix
for div in divs:
    a_tag = div.find("a")
    if a_tag and a_tag.has_attr("href"):
        href = a_tag["href"]

        # Check if the href starts with the desired path
        if href.startswith(url_prefix):
            full_url = "https://help.blackboard.com" + href
            print(f"Scraping URL: {full_url}")

            # Send a GET request to the specific page
            page_response = requests.get(full_url)
            page_soup = BeautifulSoup(page_response.content, "html.parser")

            # Find the title in the <h1> inside the div with id 'block-blackboard-page-title'
            title_tag = page_soup.find("div", id="block-blackboard-page-title").find("h1")
            title = title_tag.get_text(strip=True) if title_tag else "Untitled"

            # Find all content within the div with id 'block-blackboard-content'
            content_div = page_soup.find("div", id="block-blackboard-content")
            content = ""

            if content_div:
                for element in content_div.find_all():
                    if element.name in ["p", "h1", "h2", "h3", "h4", "h5", "h6", "div", "span"]:
                        text = element.get_text(separator=" ", strip=True)
                        if text:
                            content += text + "\n\n"
                    elif element.name in ["img", "video"]:
                        src = element.get("src")
                        if src:
                            content += f"[MEDIA: {src}]\n"

            # Define the file name based on the title (sanitize to make it file-system safe)
            filename = "".join(x for x in title if x.isalnum() or x in "._- ").strip() + ".txt"

            # Save the content to a text file
            with open(filename, "w", encoding="utf-8") as file:
                file.write(title + "\n\n" + content)

            print(f"Content scraped and saved to '{filename}'")
