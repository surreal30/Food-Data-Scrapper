import requests
from bs4 import BeautifulSoup
import time
import os

alphabets = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i',
	'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q',
	'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '*'
	]

BASE_URL = os.environ["brand_data_site"]

for alphabet in alphabets:
	f = open("food_brands.csv", "a")
	response = requests.get(f"{BASE_URL}&f={alphabet}")
	first_page = BeautifulSoup(response.text, 'html.parser')
	brand_table = first_page.find('div', class_ = 'leftCellContent')
	brands = brand_table.find_all('h2')

	pages_div = first_page.find('div', class_ = 'searchResultsPaging')
	no_of_pages = len(pages_div.find_all('a'))

	for brand in brands:
		anchor = brand.find('a')
		name = anchor['title']
		f.write(f"{name},")
		print(name)

	if no_of_pages > 1:
		for i in range(1, no_of_pages):
			next_page = requests.get(f"{BASE_URL}&pg={i}&f={alphabet}")
			page = BeautifulSoup(next_page.text, 'html.parser')
			brand_table = page.find('div', class_ = 'leftCellContent')
			brands = brand_table.find_all('h2')
			for brand in brands:
				anchor = brand.find('a')
				name = anchor['title']
				f.write(f"{name},")
				print(name)
	f.close()
	time.sleep(2)