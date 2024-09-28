import requests

# API endpoint URL
name='elon musk'
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
        descriptions= descriptions[:3]
        # Print descriptions
        for description in descriptions:
            print(description)
    else:
        print("No articles found in the response.")
else:
    print("Failed to fetch data from the API.")
