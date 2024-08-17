import requests
from bs4 import BeautifulSoup
import time
import os

f = open("food_brands.csv", "r")
food_brands = f.readline().rstrip(",")
food_brands_list = food_brands.split(",")
f.close

BASE_URL = os.environ["nutrition_data_site"]

for food_brand in food_brands_list:

	f = open("nutrition_data.txt", "a")
	f.write(f"\n\nBrand: {food_brand}\n\n")
	f.close

	response = requests.get(BASE_URL + "search?q=" + food_brand)

	response_body = BeautifulSoup(response.text, 'html.parser')

	pagination_div = response_body.find('div', class_ = 'searchResultsPaging')
	if pagination_div == None:
		continue
	next_page = pagination_div.find('span', class_ = "next")

	res_table = response_body.find('table', class_ = "generic searchResult")
	rows = res_table.find_all('tr')

	for row in rows:
		anchor = row.find('a', class_ = "prominent")
		link = anchor.get('href')
		item_name = anchor.string

		item_page = requests.get(BASE_URL + link)
		item_body = BeautifulSoup(item_page.text, 'html.parser')

		nutrition_table = item_body.find('div', class_ = 'nutrition_facts international')
		print(link)
		table_divs = nutrition_table.find_all('div')

		print(f"||||||||||||||nutrition details for {food_brand}: {item_name}|||||||||||||||||||")
		nutrition = " "
		f = open("nutrition_data.txt", "a")
		f.write(f"nutrition details for {food_brand}: {item_name} \n")
		for table_div in table_divs:
			ignored_headings = ['heading', 'divider']
			if table_div.get('class') and table_div.get('class')[0] not in ignored_headings:
				if table_div.get('class')[-1] == 'serving_size_label':
					nutrition += table_div.getText() + ":"
				elif table_div.get('class')[-1] == 'serving_size_value':
					nutrition += table_div.getText()
					f.write(nutrition + "\n")
					nutrition = " "
				elif table_div.get('class')[-1] == 'left':
					nutrition += table_div.getText() + ":"
				elif table_div.get('class')[-1] == 'tRight':
					nutrition += table_div.getText()
					# print(nutrition)
					f.write(nutrition + "\n")
					nutrition = " "
		f.close()
		time.sleep(10)

	while next_page != None:
		next_page_link = next_page.find('a').get('href')

		response = requests.get(BASE_URL + next_page_link)
		response_body = BeautifulSoup(response.text, 'html.parser')
		res_table = response_body.find('table', class_ = "generic searchResult")
		rows = res_table.find_all('tr')

		for row in rows:
			anchor = row.find('a', class_ = "prominent")
			link = anchor.get('href')
			item_name = anchor.string

			item_page = requests.get(BASE_URL + link)
			item_body = BeautifulSoup(item_page.text, 'html.parser')

			nutrition_table = item_body.find('div', class_ = 'nutrition_facts international')
			print(link)

			table_divs = nutrition_table.find_all('div')

			print(f"||||||||||||||nutrition details for {food_brand}: {item_name}|||||||||||||||||||")
			nutrition = " "
			f = open("nutrition_data.txt", "a")
			f.write(f"nutrition details for {food_brand}: {item_name} \n")
			for table_div in table_divs:
				ignored_headings = ['heading', 'divider']
				if table_div.get('class') and table_div.get('class')[0] not in ignored_headings:
					if table_div.get('class')[-1] == 'serving_size_label':
						nutrition += table_div.getText() + ":"
					elif table_div.get('class')[-1] == 'serving_size_value':
						nutrition += table_div.getText()
						# print(nutrition)
						f.write(nutrition + "\n")

						nutrition = " "
					elif table_div.get('class')[-1] == 'left':
						nutrition += table_div.getText() + ":"
					elif table_div.get('class')[-1] == 'tRight':
						nutrition += table_div.getText()
						# print(nutrition)
						f.write(nutrition + "\n")

						nutrition = " "
			f.close
			time.sleep(10)

		pagination_div = response_body.find('div', class_ = 'searchResultsPaging')
		next_page = pagination_div.find('span', class_ = "next")