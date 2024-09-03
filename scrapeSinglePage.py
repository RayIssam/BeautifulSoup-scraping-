import requests
from bs4 import BeautifulSoup
import re

# URL of the webpage to scrape
url = "https://help.blackboard.com/Learn/Student/Ultra/Interact/Messages"
base_url = "https://help.blackboard.com/"

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

# Function to process and replace images and videos with their URLs
def process_element(element):
    if element.name == 'img':
        img_src = element.get('src')
        if img_src:
            full_url = f"{base_url}{img_src.lstrip('/')}"  # Construct full URL
            return f'[Image: {full_url}]'
    elif element.name == 'video':
        video_src = element.get('src')
        if video_src:
            full_url = f"{base_url}{video_src.lstrip('/')}"  # Construct full URL
            return f'[Video: {full_url}]'
        else:
            # Check for <source> tags within the video tag
            source_tags = element.find_all('source')
            for source in source_tags:
                source_src = source.get('src')
                if source_src:
                    full_url = f"{base_url}{source_src.lstrip('/')}"  # Construct full URL
                    return f'[Video: {full_url}]'
    return element.get_text(strip=True)

# Check if the article content exists
if article_content:
    # Traverse and process the elements to replace images and videos with their URLs
    for element in article_content.descendants:
        if element.name in ['img', 'video']:
            content_to_save += process_element(element) + '\n'
        elif isinstance(element, str):
            content_to_save += element.strip() + '\n'
        elif element.name == 'br':
            content_to_save += '\n'

# Print the content
print(content_to_save)

# Optionally, save the content to a text file
with open('Messages.txt', 'w', encoding='utf-8') as file:
    file.write(content_to_save)
