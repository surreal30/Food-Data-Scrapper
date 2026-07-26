import json

brands = []
products = []

# convert text into list
def process_row(text):
    text = text.replace("\n", "")
    text = text.split("\t")
    return list(map(lambda x: x.strip(), text))

def check_ingredients(row):
    return row[INGREDIENTS_INDEX] != ''

def create_obj(fieldnames, row):
    # I manually inserted checked the index of the attributes
    obj = {
        'code': row[0],
        'url': row[1],
        'name': row[10],
        'generic_name': row[12],
        'brand': row[18],
        'brand_tags': row[19],
        'categories': row[20],
        'ingredients': row[41],
        'ingredient_tags': row[42],
        'ingredient_analysis_tags': row[43],
        'allergens': row[44],
        'traces': row[46],
        'main_category': row[79],
        'serving_size': row[49],
        'serving_quantity': row[50]
    }

    # join the dicts
    obj = obj | fetch_nutrition(fieldnames, row)
    return obj

# Check if any nutrition data is provided if it is then create a dict for it
def fetch_nutrition(fieldnames, row):
    nutrition = {}
    for i in range(87, len(row)):
        if row[i] != '':
            attr = fieldnames[i]
            nutrition[attr] = row[i]

    return nutrition

# A lot of products are duplicates. This doesn't remove all the duplicates but removes major ones.
# Sometimes names are little bit different and go undetected by this functions.
def check_not_duplicate(row):
    if row[10].lower() not in products and row[18].lower() not in brands:
        return True

    return False

def main():
    csvfile = open("en.openfoodfacts.org.products.csv", "r")
    row = csvfile.readline()
    fieldnames = process_row(row)

    data = []

    while row != '':
        row = process_row(row)
        if check_ingredients(row) and check_not_duplicate(row):
            print(row[18] + row[10])
            brands.append(row[18].lower())
            products.append(row[10].lower())
            json_obj = create_obj(fieldnames, row)
            data.append(json_obj)
        row = csvfile.readline()

    with open("nutrition_data.json", "w") as f:
    	json.dump(data, f, indent=2)

    csvfile.close()

if __name__ == "__main__":
    main()