import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin

# Base URL
base_url = 'https://tiasays.in'

# Send request to the main page
response = requests.get(base_url)
soup = BeautifulSoup(response.text, 'html.parser')

# Create directories to save files and text
os.makedirs('downloaded_files', exist_ok=True)
os.makedirs('downloaded_text', exist_ok=True)

# Find all links on the page
links = soup.find_all('a')

# Scrape text content and download files (e.g., images)
for link in links:
    href = link.get('href')
    if not href:
        print(f'Skipped empty link')
        continue

    # Convert relative URLs to absolute URLs
    full_url = urljoin(base_url, href)

    # Download files (images, PDFs, etc.)
    if full_url.endswith(('.jpg', '.jpeg', '.png', '.gif', '.pdf')):
        try:
            file_response = requests.get(full_url)
            file_name = os.path.join('downloaded_files', os.path.basename(full_url))
            with open(file_name, 'wb') as file:
                file.write(file_response.content)
            print(f'Downloaded file: {file_name}')
        except Exception as e:
            print(f'Failed to download {full_url}: {e}')
    else:
        # Scrape text content from the linked page
        try:
            page_response = requests.get(full_url)
            page_soup = BeautifulSoup(page_response.text, 'html.parser')
            # Extract text from paragraphs or other relevant tags
            text_content = page_soup.get_text(separator=' ', strip=True)
            # Save text content to a file
            text_file_name = os.path.join('downloaded_text', f'text_{os.path.basename(full_url)}.txt')
            with open(text_file_name, 'w', encoding='utf-8') as text_file:
                text_file.write(text_content)
            print(f'Saved text content: {text_file_name}')
        except Exception as e:
            print(f'Failed to scrape text from {full_url}: {e}')
            