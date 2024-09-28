import json
import requests
import csv
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import nltk
from newspaper import Article
from textblob import TextBlob
import sys

# Download the NLTK punkt package if not already downloaded
nltk.download('punkt')

# Set up Selenium webdriver with headless Chrome
options = Options()
options.headless = True
driver = webdriver.Chrome(options=options)

all_articles = []
all = []
name = ""
# Name and URL of the website to scrape
args = sys.argv[1:]
for arg in args:
    name += " " + arg

# articles from africanmanager
url = "https://africanmanager.com/?s=" + name.strip()

# Load the page
driver.get(url)

# Wait for the page to load completely
time.sleep(1)  # Adjust the sleep time as needed

# Get the page source
page_source = driver.page_source

# Parse the HTML code using BeautifulSoup
soup = BeautifulSoup(page_source, 'html.parser')
divs = soup.find_all('div', class_='td_module_16 td_module_wrap td-animation-stack')
divs = divs[:3]

total_polarity = 0
article_count = 0

for div in divs:
    first_a = div.find('a')  # Find the first <a> tag
    link = first_a['href']  # Get the 'href' attribute value
    article = Article(link)

    # Download and parse the article
    article.download()
    article.parse()

    # Apply NLP to the article
    article.nlp()

    # Get the summary of the article and clean it
    summary = article.summary.replace('\n', ' ')  # Replace newline characters with space
    all.append((summary))
# articles from reuters
url = f"https://www.reuters.com/pf/api/v3/content/fetch/articles-by-search-v2?query=%7B%22keyword%22%3A%22{name}%22%2C%22offset%22%3A0%2C%22orderby%22%3A%22display_date%3Adesc%22%2C%22size%22%3A20%2C%22website%22%3A%22reuters%22%7D&d=203&_website=reuters"

# Make GET request
response = requests.get(url)

# Check if request was successful (status code 200)
if response.status_code == 200:
    # Parse JSON response
    data = response.json()

    # Check if 'articles' key exists in the response
    if 'articles' in data['result']:
        # Extract descriptions

        descriptions = [article['description'] for article in data['result']['articles']]
        descriptions = descriptions[:3]
        # Print descriptions
        for description in descriptions:
            description = description.replace('\n', ' ')
            all.append(description)
# articles from forbes
url = "https://www.forbes.com/search/?q=" + name

# Load the page
driver.get(url)

# Wait for the page to load completely
time.sleep(1)  # Adjust the sleep time as needed

# Get the page source
page_source = driver.page_source

# Parse the HTML code using BeautifulSoup
soup = BeautifulSoup(page_source, 'html.parser')
divs = soup.find_all('p', class_='CardArticle_description__2fQbs')
divs = divs[:3]

# Extract the content of the span tags within each p tag
for div in divs:
    span = div.find('span')
    if span:
        span_text = span.get_text(strip=True)
        all.append(span_text)

# Close the driver
driver.quit()

for article in all:
    sentiment = TextBlob(article).sentiment
    total_polarity += sentiment.polarity
    article_count += 1

    all_articles.append({
        'summary': article,
        'polarity': sentiment.polarity
    })
# Calculate average polarity
if article_count > 0:
    average_polarity = total_polarity / article_count
else:
    average_polarity = 0

# Remove leading/trailing spaces and convert the name to a valid filename format
csv_filename = name.strip().replace(' ', '_') + '.csv'

# Save the results to a CSV file
csv_directory = r"C:\Users\Ahmed\Desktop\Projet Stage\api\csvs"
csv_path = os.path.join(csv_directory, csv_filename)

with open(csv_path, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['article', 'sentiment'])
    for article in all_articles:
        writer.writerow([article['summary'], article['polarity']])

output = {
    'filePath': csv_path,
    'resultat': average_polarity
}
json_data = json.dumps(output)

print(json_data)
# Close the browser
driver.quit()
