import requests
from bs4 import BeautifulSoup
import re

# URL of the webpage to scrape
url = "https://help.blackboard.com/Learn/Student/Ultra/Getting_Started/Browser_Support"

# Make a request to fetch the webpage content
response = requests.get(url)

# Parse the content with BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')

# Extract the title from the span inside the h1 tag within the div with id 'block-blackboard-page-title'
title_div = soup.find('div', id='block-blackboard-page-title')
title = title_div.find('h1').find('span').get_text(strip=True) if title_div else 'No Title Found'

# Extract the article content
article_content = soup.find('article')

# Initialize content to save
content_to_save = f"Title: {title}\n\n"

# Check if the article content exists
if article_content:
    # Extract all text
    content_to_save += article_content.get_text(separator='\n', strip=True)

    # Extract image sources
    images = article_content.find_all('img')
    if images:
        content_to_save += "\n\nImages:\n"
        for img in images:
            img_src = img.get('src')
            content_to_save += f"{img_src}\n"

    # Extract video sources
    videos = article_content.find_all('video')
    if videos:
        content_to_save += "\n\nVideos:\n"
        for video in videos:
            # Check for video source or child <source> tags
            video_src = video.get('src')
            if video_src:
                content_to_save += f"{video_src}\n"
            else:
                # Check for <source> tags within the video tag
                source_tags = video.find_all('source')
                for source in source_tags:
                    source_src = source.get('src')
                    if source_src:
                        content_to_save += f"{source_src}\n"

    # Extract iframe sources
    iframes = article_content.find_all('iframe')
    if iframes:
        content_to_save += "\n\nIframes:\n"
        for iframe in iframes:
            iframe_src = iframe.get('src')
            if iframe_src:
                content_to_save += f"{iframe_src}\n"

    # Extract background image URLs from styles
    background_divs = article_content.find_all('div', class_='ytp-cued-thumbnail-overlay-image')
    if background_divs:
        content_to_save += "\n\nBackground Images:\n"
        for div in background_divs:
            style = div.get('style')
            # Extract URL from style attribute using regex
            url_match = re.search(r'url\("(.+?)"\)', style)
            if url_match:
                content_to_save += f"{url_match.group(1)}\n"

else:
    content_to_save += "No article content found."

# Print the content
print(content_to_save)

# Optionally, save the content to a text file
with open('browser_support.txt', 'w', encoding='utf-8') as file:
    file.write(content_to_save)
