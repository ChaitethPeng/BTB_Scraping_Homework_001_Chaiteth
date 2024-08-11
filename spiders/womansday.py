import requests
from bs4 import BeautifulSoup
import json

url = 'https://www.womansday.com/relationships/dating-marriage/a41055149/best-pickup-lines/'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Initialize a dictionary
pickup_lines_dict = {}

sections = soup.find_all('h2')
for section in sections:
    title = section.get_text(strip=True)

    ul_tag = section.find_next('ul')
    ol_tag = section.find_next('ol')
    div_tag = section.find_next('div', class_=lambda x: x and 'list' in x.lower())

    # Initialize an empty list to hold pickup lines
    pickup_lines_list = []

    if ul_tag:
        pickup_lines_list = [line.get_text(strip=True) for line in ul_tag.find_all('li')]
    elif ol_tag:
        pickup_lines_list = [line.get_text(strip=True) for line in ol_tag.find_all('li')]
    elif div_tag:
        pickup_lines_list = [line.get_text(strip=True) for line in div_tag.find_all('p')]

    if pickup_lines_list:
        pickup_lines_dict[title] = pickup_lines_list
    else:
        print(f"No pickup lines found for the title: {title}")

# Save the dictionary
with open('pickup_lines.json', 'w') as json_file:
    json.dump(pickup_lines_dict, json_file, indent=4)

