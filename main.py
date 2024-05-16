import requests
import pandas as pd

base_url = "https://wakeupper.com/wp-json/wc/v3/"
consumer_key = "ck_156701589f38c153ec497c6b5b4235c33c80ad24"
consumer_secret = "cs_1ccd6411f64debc6a0ed20c71aec513c224d916d"
auth = requests.auth.HTTPBasicAuth(consumer_key, consumer_secret)


def create_product(product_data):


  response = requests.post(base_url + "products", json=product_data, auth=auth)

  if response.status_code == 201:
    print("Product created successfully!")
    return response.json()
  else:
    print(f"Error creating product: {response.status_code}")
    print(response.text)
    return None


def excel_loop():
    df = pd.read_excel('products.xlsx')

    for index, row in df.iterrows():
        product = row.to_dict()

        name = product['name']
        typpe = product['type']
        description = product['description']
        short_description = product['short_description']

        categories = product['categories']
        categories_list = []
        if ',' in str(categories):
            category_ids = categories.split(',')
            category_list = [{"id": int(cat_id)} for cat_id in category_ids]
            categories_list.extend(category_list)
        else:
            categories_list.extend([{"id": int(categories)}])

        images = product['images']
        images_list = []
        if ',' in images:
            image_ids = images.split(',')
            image_list = [{"src": img_id} for img_id in image_ids]
            images_list.extend(image_list)
        else:
            images_list.extend([{"src": images}])
        
        attributes = [{"id": 6, "position": 0, "visible": False, "variation": True, "options": ["Black", "Green"]},
                   {"name": "Size", "position": 0, "visible": True, "variation": True, "options": ["S", "M"]}],
        default_attributes = [{"id": 6, "option": "Black"}, {"name": "Size", "option": "S"}]

        simple_product = {
        "name": name,
        "type": typpe,
        "description": description,
        "short_description": short_description,
        "categories": categories_list,
        "images": images_list,
        "attributes": attributes,
        "default_attributes": default_attributes
    }
    
        create_product(simple_product)

excel_loop()