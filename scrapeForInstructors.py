import requests
from bs4 import BeautifulSoup
import os
import time

# Base URL of the main page to scrape
base_url = "https://howtomef.helpdocsite.com/instructors2"

# Send a GET request to the main page
response = requests.get(base_url)
soup = BeautifulSoup(response.content, "html.parser")

# Find all article links within the 'articles-list' ul
article_links = soup.find("ul", class_="articles-list").find_all("li")

# Loop through each article link and scrape its content
for li in article_links:
    # Get the article endpoint from the href attribute
    article_name = li.find("a")["href"]
    print (article_name)
    # Correct URL formation: combine base URL with article name
    article_url = " https://" + article_name.lstrip('/')

    # Print URL for debugging
    print(f"Scraping URL: {article_url}")

    # Send a GET request to the article page
    article_response = requests.get(article_url)

    # Parse the article page content
    article_soup = BeautifulSoup(article_response.content, "html.parser")

    # Find the header title with error handling
    header_title_tag = article_soup.find("h2", class_="header-title")
    if header_title_tag:
        header_title = header_title_tag.get_text(strip=True)
    else:
        print(f"Header title not found for URL: {article_url}")
        continue  # Skip to the next article if header title is not found

    # Find the article within the article-body section
    article_body_section = article_soup.find("section", class_="article-body")
    if article_body_section:
        article = article_body_section.find("article")
    else:
        print(f"Article body section not found for URL: {article_url}")
        continue  # Skip to the next article if article body section is not found

    # Initialize content variable
    content = ""

    # Get all text and images inside the article in order
    for element in article.find_all(["p", "h1", "h2", "h3", "h4", "h5", "h6", "ul", "ol", "li", "img", "div"]):
        if element.name == "img":
            # If the element is an image, add the image URL
            content += f"[IMAGE: {element.get('src')}]\n"
        else:
            # Extract text for paragraphs, headings, lists, etc.
            text = element.get_text(separator=" ", strip=True)
            if text:
                content += text + "\n\n"

    # Define the file name based on the header title (make it safe for file names)
    filename = "".join(x for x in header_title if (x.isalnum() or x in "._- ")).strip() + ".txt"

    # Save the content to a text file
    with open(filename, "w", encoding="utf-8") as file:
        file.write(header_title + "\n\n" + content)

    print(f"Content scraped and saved to '{filename}'")

    # Be polite: wait a second before next request
    time.sleep(1)

print("All articles have been scraped and saved.")
