import requests
from bs4 import BeautifulSoup
import csv

# URL of the page containing the links
url = "https://www.basarisiralamalari.com/ozel-universite-ogrenim-egitim-ucretleri/"  # replace with the actual URL

# Send a request to the webpage
response = requests.get(url)
response.raise_for_status()  # Check if the request was successful

# Parse the webpage content
soup = BeautifulSoup(response.text, 'html.parser')

# Find all <a> tags within the list that contain links to university fees pages
links = soup.select('ul li a')  # Customize selector based on the actual page structure

# Extract only URLs
university_links = [link['href'] for link in links if 'href' in link.attrs]

# Write the results to a CSV file
with open('university_links.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["Link"])  # Write header

    # Write each URL
    for link in university_links:
        writer.writerow([link])

print("CSV file has been created successfully: university_links.csv")
